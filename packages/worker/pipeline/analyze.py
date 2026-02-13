"""
Stage 2: Basic audio analysis — duration and BPM estimation.
"""
from dataclasses import dataclass

import numpy as np
import soundfile as sf


@dataclass
class AnalysisResult:
    """Result of audio analysis."""
    duration_seconds: float
    bpm: float


def _estimate_bpm(samples: np.ndarray, sample_rate: int) -> float:
    """
    Simple onset-based BPM estimation.

    Uses energy envelope peak detection. This is a rough estimate
    suitable for MVP — Phase 2 can use librosa for better accuracy.
    """
    # Mix to mono for analysis
    if samples.ndim > 1:
        mono = np.mean(samples, axis=1)
    else:
        mono = samples

    # Compute energy envelope with short windows
    hop = int(sample_rate * 0.01)  # 10ms hops
    window = int(sample_rate * 0.02)  # 20ms window
    n_frames = (len(mono) - window) // hop

    if n_frames < 10:
        return 120.0  # Default for very short audio

    energy = np.array([
        np.sum(mono[i * hop : i * hop + window] ** 2)
        for i in range(n_frames)
    ])

    # Normalize
    energy = energy / (np.max(energy) + 1e-10)

    # Detect onsets (energy rises above threshold)
    threshold = 0.3
    diff = np.diff(energy)
    onsets = np.where((diff[:-1] > 0) & (diff[1:] < 0) & (energy[1:-1] > threshold))[0]

    if len(onsets) < 2:
        return 120.0  # Default

    # Calculate average inter-onset interval
    intervals = np.diff(onsets) * hop / sample_rate  # in seconds
    # Filter out very short and very long intervals (30-300 BPM range)
    valid = intervals[(intervals > 0.2) & (intervals < 2.0)]

    if len(valid) < 2:
        return 120.0

    avg_interval = np.median(valid)
    bpm = 60.0 / avg_interval

    # Clamp to reasonable range
    return float(np.clip(bpm, 40, 240))


def analyze(canonical_path: str) -> AnalysisResult:
    """
    Analyze a canonical WAV file.

    Args:
        canonical_path: Path to canonical WAV (44.1kHz 16-bit).

    Returns:
        AnalysisResult with duration and estimated BPM.
    """
    samples, sample_rate = sf.read(canonical_path, dtype="float32")
    duration = len(samples) / sample_rate
    bpm = _estimate_bpm(samples, sample_rate)

    return AnalysisResult(
        duration_seconds=round(duration, 2),
        bpm=round(bpm, 1),
    )
