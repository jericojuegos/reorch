"""
Stage 3b: Stem-aligned time-stretch — adjust tempo per-stem with pitch preservation.

Uses pyrubberband (Rubber Band Library) for high-quality time-stretching.
Vocal stems use formant-preserving mode; transient-heavy stems use standard mode.
"""
import os
from typing import Optional

import numpy as np
import soundfile as sf
import pyrubberband as pyrb


# If the BPM ratio is within this tolerance, skip stretching (no-op).
_RATIO_TOLERANCE = 0.005  # 0.5%


def time_stretch_stems(
    stem_paths: dict[str, str],
    original_bpm: float,
    target_bpm: float,
    work_dir: str,
) -> dict[str, str]:
    """
    Time-stretch each stem to match a target BPM.

    - Vocal stems use Rubber Band's formant-preserving mode (-F).
    - Non-vocal stems (drums, bass, other) use standard mode for better transients.

    Args:
        stem_paths: Dict mapping stem name → WAV file path.
        original_bpm: Detected BPM of the original audio.
        target_bpm: Desired BPM after stretching.
        work_dir: Directory for intermediate files.

    Returns:
        Dict mapping stem name → path to stretched WAV (or original if no-op).
    """
    ratio = target_bpm / original_bpm

    # No-op optimisation: if ratio ≈ 1.0, return paths unchanged
    if abs(ratio - 1.0) < _RATIO_TOLERANCE:
        return dict(stem_paths)

    stretched_dir = os.path.join(work_dir, "stretched")
    os.makedirs(stretched_dir, exist_ok=True)

    result: dict[str, str] = {}

    for stem_name, stem_path in stem_paths.items():
        samples, sr = sf.read(stem_path, dtype="float32")

        # Vocal stem: preserve formants/pitch with the -F flag
        if stem_name == "vocals":
            stretched = pyrb.time_stretch(samples, sr, ratio, rbargs={"-F": ""})
        else:
            stretched = pyrb.time_stretch(samples, sr, ratio)

        out_path = os.path.join(stretched_dir, f"{stem_name}.wav")
        sf.write(out_path, stretched, sr, subtype="PCM_16")
        result[stem_name] = out_path

    return result


def remix_stems(stem_paths: dict[str, str], work_dir: str) -> str:
    """
    Sum all stems into a single stereo mix.

    Args:
        stem_paths: Dict mapping stem name → WAV file path.
        work_dir: Directory for intermediate files.

    Returns:
        Path to the remixed WAV file.
    """
    mixed: Optional[np.ndarray] = None
    out_sr: int = 44100

    for stem_path in stem_paths.values():
        samples, sr = sf.read(stem_path, dtype="float32")
        out_sr = sr
        if mixed is None:
            mixed = samples.copy()
        else:
            # Pad or truncate to match the longest stem
            if len(samples) > len(mixed):
                pad = np.zeros((len(samples) - len(mixed), mixed.shape[1] if mixed.ndim > 1 else 1), dtype="float32")
                if mixed.ndim == 1:
                    pad = pad.squeeze()
                mixed = np.concatenate([mixed, pad])
            elif len(samples) < len(mixed):
                pad = np.zeros((len(mixed) - len(samples), samples.shape[1] if samples.ndim > 1 else 1), dtype="float32")
                if samples.ndim == 1:
                    pad = pad.squeeze()
                samples = np.concatenate([samples, pad])
            mixed = mixed + samples

    if mixed is None:
        raise ValueError("No stems provided to remix")

    # Prevent clipping
    peak = np.max(np.abs(mixed))
    if peak > 1.0:
        mixed = mixed / peak

    output_path = os.path.join(work_dir, "remixed.wav")
    sf.write(output_path, mixed, out_sr, subtype="PCM_16")
    return output_path
