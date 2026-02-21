"use client";

import { useEffect, useState } from "react";
import { Loader2, CheckCircle2, AlertCircle, FileAudio, Download } from "lucide-react";

type JobStatus = "queued" | "running" | "succeeded" | "failed";

export interface Job {
    id: string;
    track_id: string;
    preset: string;
    status: JobStatus;
    progress: number;
    error_message?: string;
    output_path?: string;
}

interface JobProgressProps {
    jobId: string;
    onComplete?: (job: Job) => void;
    onError?: (error: string) => void;
}

export function JobProgress({ jobId, onComplete, onError }: JobProgressProps) {
    const [job, setJob] = useState<Job | null>(null);
    const [isPolling, setIsPolling] = useState(true);

    useEffect(() => {
        if (!jobId || !isPolling) return;

        let intervalId: NodeJS.Timeout;

        const pollJobStatus = async () => {
            try {
                const res = await fetch(`/api/jobs/${jobId}`);
                if (!res.ok) throw new Error("Failed to fetch job status");

                const data: Job = await res.json();
                setJob(data);

                if (data.status === "succeeded") {
                    setIsPolling(false);
                    if (onComplete) onComplete(data);
                } else if (data.status === "failed") {
                    setIsPolling(false);
                    if (onError) onError(data.error_message || "Job failed");
                }
            } catch (err) {
                console.error("Polling error:", err);
                setIsPolling(false);
                if (onError) onError("Failed to communicate with processing server");
            }
        };

        // Poll immediately, then every 2 seconds
        pollJobStatus();
        intervalId = setInterval(pollJobStatus, 2000);

        return () => clearInterval(intervalId);
    }, [jobId, isPolling, onComplete, onError]);

    if (!job) {
        return (
            <div className="glass-card p-8 rounded-xl border border-creamy-white/10 flex flex-col items-center justify-center text-center">
                <Loader2 className="animate-spin text-primary mb-4" size={32} />
                <p className="text-creamy-white/70 font-medium">Initializing processing...</p>
            </div>
        );
    }

    const getStageName = (progress: number) => {
        if (progress < 20) return "Analyzing Track Structure...";
        if (progress < 50) return "Isolating Stems...";
        if (progress < 80) return "Applying Genre Transformation...";
        if (progress < 100) return "Mixing & Mastering...";
        return "Finalizing...";
    };

    return (
        <div className="glass-card p-8 rounded-xl border border-creamy-white/10">
            <div className="flex items-start justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className={`w-10 h-10 rounded-lg flex items-center justify-center
                        ${job.status === "succeeded" ? "bg-primary/20 text-primary" :
                            job.status === "failed" ? "bg-red-500/20 text-red-500" :
                                "bg-accent/20 text-accent"}
                    `}>
                        {job.status === "succeeded" ? <CheckCircle2 size={24} /> :
                            job.status === "failed" ? <AlertCircle size={24} /> :
                                <Loader2 size={24} className="animate-spin" />}
                    </div>
                    <div>
                        <h4 className="font-bold text-creamy-white">
                            {job.status === "queued" && "Job Queued"}
                            {job.status === "running" && "Processing Track"}
                            {job.status === "succeeded" && "Transformation Complete"}
                            {job.status === "failed" && "Processing Failed"}
                        </h4>
                        <p className="text-xs font-mono text-creamy-white/50 lowercase">
                            id: {job.id.substring(0, 8)} • preset: {job.preset}
                        </p>
                    </div>
                </div>

                {job.status === "running" && (
                    <div className="text-2xl font-display font-bold text-transparent bg-clip-text bg-gradient-to-r from-accent to-primary">
                        {job.progress}%
                    </div>
                )}
            </div>

            {/* Progress Bar */}
            {(job.status === "running" || job.status === "queued") && (
                <div className="space-y-2 mb-6">
                    <div className="flex justify-between text-xs font-mono text-creamy-white/50">
                        <span>{job.status === "queued" ? "Waiting for worker..." : getStageName(job.progress)}</span>
                    </div>
                    <div className="h-2 w-full bg-white/5 rounded-full overflow-hidden">
                        <div
                            className="h-full bg-gradient-to-r from-accent to-primary rounded-full transition-all duration-500 ease-out"
                            style={{ width: `${Math.max(job.progress, 2)}%` }} // Minimum visible width
                        />
                    </div>
                </div>
            )}

            {/* Error State */}
            {job.status === "failed" && (
                <div className="p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm mt-4">
                    <strong>Error:</strong> {job.error_message || "An unknown error occurred during processing."}
                </div>
            )}

            {/* Success State (Download UI Placeholder) */}
            {job.status === "succeeded" && (
                <div className="mt-6 pt-6 border-t border-white/5 flex flex-col sm:flex-row gap-4">
                    <button className="flex-1 bg-primary hover:bg-primary/90 text-creamy-white px-4 py-3 rounded-lg font-semibold text-sm transition-all shadow-lg shadow-primary/30 flex items-center justify-center gap-2 cursor-pointer">
                        <Download size={18} /> Download WAV
                    </button>
                    <button className="flex-1 glass-card border border-white/10 hover:bg-white/5 text-creamy-white px-4 py-3 rounded-lg font-medium text-sm transition-all flex items-center justify-center gap-2 cursor-pointer">
                        <FileAudio size={18} /> Download MP3
                    </button>
                </div>
            )}
        </div>
    );
}
