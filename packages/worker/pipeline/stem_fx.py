"""
Stage 3c: Per-stem effects processing — apply preset-specific
effects to individual stems before remix.

Currently supports drum enhancement for the ballad_to_rock preset
with parallel compression for added punch.
"""
import os

import numpy as np
import soundfile as sf
from pedalboard import (
    Compressor,
    Distortion,
    HighpassFilter,
    PeakFilter,
    Pedalboard,
)


# Dry/wet mix ratio for parallel compression.
# 0.0 = fully dry, 1.0 = fully wet.
PARALLEL_WET = 0.6


# Per-stem effect chains keyed by preset and stem name.
# Only stems listed here are processed; others pass through unchanged.
STEM_FX: dict[str, dict[str, Pedalboard]] = {
    "ballad_to_rock": {
        "drums": Pedalboard([
            # Remove sub-rumble before saturation
            HighpassFilter(cutoff_frequency_hz=60.0),
            # Aggressive compression for punch
            Compressor(
                threshold_db=-18.0,
                ratio=6.0,
                attack_ms=2.0,
                release_ms=80.0,
            ),
            # Heavier saturation / grit
            Distortion(drive_db=12.0),
            # Snap / attack emphasis at 5 kHz
            PeakFilter(cutoff_frequency_hz=5000.0, gain_db=3.0, q=1.4),
        ]),
    },
}


def apply_stem_fx(
    stem_paths: dict[str, str],
    preset: str,
    work_dir: str,
) -> dict[str, str]:
    """
    Apply per-stem effects based on the preset.

    Uses parallel compression for processed stems: the final output is
    a mix of the dry (original) signal and the wet (processed) signal,
    controlled by PARALLEL_WET.

    Args:
        stem_paths: Dict mapping stem name → WAV file path.
        preset: Transformation preset name.
        work_dir: Directory for intermediate files.

    Returns:
        Dict mapping stem name → path to processed (or original) WAV.
    """
    chains = STEM_FX.get(preset)
    if not chains:
        # No stem FX defined for this preset — pass through
        return dict(stem_paths)

    fx_dir = os.path.join(work_dir, "stem_fx")
    os.makedirs(fx_dir, exist_ok=True)

    result: dict[str, str] = {}

    for stem_name, stem_path in stem_paths.items():
        board = chains.get(stem_name)
        if board is None:
            # No FX for this stem — pass through
            result[stem_name] = stem_path
            continue

        # Read the dry signal
        samples, sr = sf.read(stem_path, dtype="float32")

        # pedalboard expects (channels, samples) for multi-channel
        if samples.ndim > 1:
            samples_t = samples.T
        else:
            samples_t = samples

        # Apply the effects chain (wet signal)
        wet = board(samples_t, sr)

        # Transpose back to (samples, channels)
        if wet.ndim > 1:
            wet = wet.T

        # Parallel compression: blend dry + wet
        blended = (1.0 - PARALLEL_WET) * samples + PARALLEL_WET * wet

        # Prevent clipping
        peak = np.max(np.abs(blended))
        if peak > 1.0:
            blended = blended / peak

        out_path = os.path.join(fx_dir, f"{stem_name}.wav")
        sf.write(out_path, blended, sr, subtype="PCM_16")
        result[stem_name] = out_path

    return result
