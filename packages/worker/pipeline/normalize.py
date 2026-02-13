"""
Stage 4: Loudness normalization — target LUFS for streaming.
"""
import os

import numpy as np
import soundfile as sf
import pyloudnorm as pyln


# Target loudness for streaming platforms (Spotify, Apple Music, YouTube)
TARGET_LUFS = -14.0


def normalize(
    input_path: str,
    work_dir: str,
    target_lufs: float = TARGET_LUFS,
) -> str:
    """
    Normalize audio loudness to a target LUFS level.

    Args:
        input_path: Path to WAV file to normalize.
        work_dir: Directory for intermediate files.
        target_lufs: Target integrated loudness in LUFS.

    Returns:
        Path to loudness-normalized WAV file.
    """
    samples, sample_rate = sf.read(input_path, dtype="float64")

    # Measure current loudness
    meter = pyln.Meter(sample_rate)
    current_lufs = meter.integrated_loudness(samples)

    # Normalize to target
    normalized = pyln.normalize.loudness(samples, current_lufs, target_lufs)

    # Prevent clipping — clamp to [-1.0, 1.0]
    peak = np.max(np.abs(normalized))
    if peak > 1.0:
        normalized = normalized / peak

    # Write output
    output_path = os.path.join(work_dir, "normalized.wav")
    sf.write(output_path, normalized, sample_rate, subtype="PCM_16")
    return output_path
