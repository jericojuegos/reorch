"""
Stage 3: Audio transformation — apply genre preset effects.

Currently supports one preset: ballad_to_rock.
"""
import os

import numpy as np
import soundfile as sf
from pedalboard import (
    Compressor,
    Distortion,
    HighpassFilter,
    LowShelfFilter,
    HighShelfFilter,
    PeakFilter,
    Pedalboard,
)


# === Preset Definitions ===

PRESETS = {
    "ballad_to_rock": Pedalboard([
        # Tighten low end — remove rumble below 80 Hz
        HighpassFilter(cutoff_frequency_hz=80.0),
        # Punch — boost low shelf at 100 Hz
        LowShelfFilter(cutoff_frequency_hz=100.0, gain_db=3.0),
        # Presence — boost mids at 3kHz for aggression
        PeakFilter(cutoff_frequency_hz=3000.0, gain_db=4.0, q=1.0),
        # Compression — glue and sustain
        Compressor(
            threshold_db=-20.0,
            ratio=4.0,
            attack_ms=5.0,
            release_ms=100.0,
        ),
        # Saturation — subtle grit/drive
        Distortion(drive_db=8.0),
        # Air — brightness on top end
        HighShelfFilter(cutoff_frequency_hz=8000.0, gain_db=2.0),
    ]),
}


def transform(
    canonical_path: str,
    work_dir: str,
    preset: str = "ballad_to_rock",
) -> str:
    """
    Apply a transformation preset to a canonical WAV file.

    Args:
        canonical_path: Path to canonical WAV (44.1kHz 16-bit stereo).
        work_dir: Directory for intermediate files.
        preset: Name of the preset to apply.

    Returns:
        Path to transformed WAV file.

    Raises:
        ValueError: If preset is not recognized.
    """
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset: '{preset}'. Available: {list(PRESETS.keys())}")

    board = PRESETS[preset]

    # Read audio
    samples, sample_rate = sf.read(canonical_path, dtype="float32")

    # pedalboard expects shape (channels, samples) for multi-channel
    if samples.ndim > 1:
        samples = samples.T  # (samples, channels) → (channels, samples)

    # Apply effects chain
    processed = board(samples, sample_rate)

    # Transpose back for soundfile
    if processed.ndim > 1:
        processed = processed.T  # (channels, samples) → (samples, channels)

    # Write output
    output_path = os.path.join(work_dir, "transformed.wav")
    sf.write(output_path, processed, sample_rate, subtype="PCM_16")
    return output_path
