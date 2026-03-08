"""
Stage 5: Mastering — LUFS normalization and true peak limiting.

Processing chain:
1. Measure integrated loudness (pyloudnorm).
2. Normalize to TARGET_LUFS (-14 LUFS for streaming platforms).
3. Apply a brickwall true peak ceiling clamp at TRUE_PEAK_LIMIT_DBFS
   (-1.0 dBTP) to ensure streaming platform compliance.
"""
import os
import math

import numpy as np
import soundfile as sf
import pyloudnorm as pyln


# Target integrated loudness (Spotify, Apple Music, YouTube standard)
TARGET_LUFS = -14.0

# True peak ceiling — -1.0 dBTP leaves 1 dB headroom for inter-sample peaks
TRUE_PEAK_LIMIT_DBFS = -1.0


def _apply_true_peak_ceiling(
    samples: np.ndarray,
    ceiling_db: float = TRUE_PEAK_LIMIT_DBFS,
) -> np.ndarray:
    """
    Apply a brickwall ceiling clamp to audio samples.

    If the peak sample amplitude exceeds the ceiling, the entire signal is
    scaled down proportionally so the peak lands exactly at the ceiling.
    This is gain-reduction only — it never adds gain.

    Args:
        samples: Audio samples (mono or stereo, any float dtype).
        ceiling_db: Maximum allowable peak level in dBFS.

    Returns:
        Gain-reduced audio (same shape and dtype as input).
    """
    ceiling_linear = 10 ** (ceiling_db / 20.0)
    peak = np.max(np.abs(samples))
    if peak > ceiling_linear:
        samples = samples * (ceiling_linear / peak)
    return samples


def normalize(
    input_path: str,
    work_dir: str,
    target_lufs: float = TARGET_LUFS,
    true_peak_limit_db: float = TRUE_PEAK_LIMIT_DBFS,
) -> str:
    """
    Normalize audio loudness and apply a true peak ceiling.

    Args:
        input_path: Path to WAV file to master.
        work_dir: Directory for intermediate files.
        target_lufs: Target integrated loudness in LUFS.
        true_peak_limit_db: Maximum true peak level in dBFS.

    Returns:
        Path to mastered WAV file.
    """
    samples, sample_rate = sf.read(input_path, dtype="float64")

    # --- Pass 1: LUFS normalization ---
    meter = pyln.Meter(sample_rate)
    current_lufs = meter.integrated_loudness(samples)

    # pyloudnorm returns -inf for silent/near-silent audio; skip in that case
    if not np.isinf(current_lufs):
        samples = pyln.normalize.loudness(samples, current_lufs, target_lufs)

    # --- Pass 2: True peak ceiling ---
    samples = _apply_true_peak_ceiling(samples, ceiling_db=true_peak_limit_db)

    # Write output
    output_path = os.path.join(work_dir, "normalized.wav")
    sf.write(output_path, samples, sample_rate, subtype="PCM_16")
    return output_path


