"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, Music, AlertCircle, X, FileAudio } from "lucide-react";

export function UploadTrack() {
    const [file, setFile] = useState<File | null>(null);
    const [error, setError] = useState<string | null>(null);

    const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
        setError(null);
        if (rejectedFiles.length > 0) {
            setError("Please upload a valid audio file (mp3 or wav) under 50MB.");
            return;
        }

        if (acceptedFiles.length > 0) {
            setFile(acceptedFiles[0]);
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            "audio/mpeg": [".mp3"],
            "audio/wav": [".wav"],
            "audio/x-wav": [".wav"]
        },
        maxSize: 50 * 1024 * 1024, // 50MB limit
        maxFiles: 1,
    });

    const clearFile = (e: React.MouseEvent) => {
        e.stopPropagation();
        setFile(null);
        setError(null);
    };

    return (
        <div className="w-full max-w-2xl mx-auto">
            <div
                {...getRootProps()}
                className={`glass-card relative overflow-hidden rounded-2xl border-2 border-dashed transition-all duration-200 cursor-pointer flex flex-col items-center justify-center p-12 text-center
          ${isDragActive ? 'border-primary bg-primary/5' : 'border-creamy-white/10 hover:border-primary/50 hover:bg-surface/40'}
          ${file ? 'border-solid border-primary/30 bg-background-dark' : ''}
        `}
            >
                <input {...getInputProps()} />

                {file ? (
                    <div className="flex flex-col items-center gap-4 w-full">
                        <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center text-primary mb-2 shadow-[0_0_15px_rgba(46,125,50,0.3)]">
                            <FileAudio size={32} />
                        </div>

                        <div className="space-y-1 w-full px-4">
                            <p className="text-lg font-bold text-creamy-white truncate">
                                {file.name}
                            </p>
                            <p className="text-sm font-mono text-creamy-white/50">
                                {(file.size / (1024 * 1024)).toFixed(2)} MB
                            </p>
                        </div>

                        <div className="mt-4 flex gap-3 z-10">
                            <button
                                onClick={clearFile}
                                className="px-4 py-2 rounded font-medium text-sm text-creamy-white/70 hover:text-creamy-white hover:bg-creamy-white/10 transition-colors flex items-center gap-2 cursor-pointer"
                            >
                                <X size={16} /> Remove
                            </button>
                            <button
                                onClick={(e) => { e.stopPropagation(); /* TODO: upload to /api/tracks */ }}
                                className="bg-primary hover:bg-primary/90 text-creamy-white px-6 py-2 rounded font-semibold text-sm transition-all shadow-lg shadow-primary/30 flex items-center gap-2 cursor-pointer"
                            >
                                <Upload size={16} /> Process Track
                            </button>
                        </div>
                    </div>
                ) : (
                    <>
                        <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-6 transition-colors duration-200
              ${isDragActive ? 'bg-primary/20 text-primary' : 'bg-surface text-creamy-white/50'}
            `}>
                            {isDragActive ? <Upload size={32} /> : <Music size={32} />}
                        </div>

                        <h3 className="text-xl font-bold text-creamy-white mb-2">
                            {isDragActive ? "Drop audio file here" : "Upload your track"}
                        </h3>

                        <p className="text-sm text-creamy-white/50 max-w-sm mx-auto mb-6 leading-relaxed">
                            Drag and drop an audio file here, or click to browse.
                            Supported formats: MP3, WAV. Max size: 50MB.
                        </p>

                        <div className="inline-flex items-center gap-2 bg-creamy-white/5 px-4 py-2 rounded-lg text-sm font-medium text-creamy-white/80 border border-creamy-white/10">
                            Browse Files
                        </div>
                    </>
                )}
            </div>

            {error && (
                <div className="mt-4 p-4 rounded-lg bg-red-500/10 border border-red-500/20 flex items-start gap-3 text-red-400">
                    <AlertCircle size={20} className="shrink-0 mt-0.5" />
                    <p className="text-sm leading-relaxed">{error}</p>
                </div>
            )}
        </div>
    );
}
