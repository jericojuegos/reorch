"""
Stage 3: Stem separation — isolate vocals, drums, bass, and other.

Uses Facebook's Demucs (Hybrid Transformer) model via the official Python API.
"""
import os
from dataclasses import dataclass, field
from pathlib import Path

import torch
from demucs.api import Separator, save_audio

from config import settings

# Stem names expected from htdemucs
STEM_NAMES = ("vocals", "drums", "bass", "other")


@dataclass
class SeparationResult:
    """Result of stem separation."""
    vocals_path: str = ""
    drums_path: str = ""
    bass_path: str = ""
    other_path: str = ""
    stem_paths: dict[str, str] = field(default_factory=dict)


def _resolve_device(device_setting: str) -> str:
    """Resolve 'auto' device setting to actual device string."""
    if device_setting == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    return device_setting


def separate(canonical_path: str, work_dir: str) -> SeparationResult:
    """
    Separate a canonical WAV file into individual stems.

    Uses the Demucs htdemucs model to produce 4 stems:
    vocals, drums, bass, other.

    Args:
        canonical_path: Path to canonical WAV (44.1kHz 16-bit stereo).
        work_dir: Directory for intermediate files.

    Returns:
        SeparationResult with paths to each separated stem WAV file.
    """
    device = _resolve_device(settings.demucs_device)

    separator = Separator(
        model=settings.demucs_model,
        device=device,
        shifts=settings.demucs_shifts,
        progress=False,
    )

    # Run separation
    origin, separated = separator.separate_audio_file(Path(canonical_path))

    # Save each stem to disk
    stems_dir = os.path.join(work_dir, "stems")
    os.makedirs(stems_dir, exist_ok=True)

    stem_paths: dict[str, str] = {}
    for stem_name, stem_tensor in separated.items():
        stem_path = os.path.join(stems_dir, f"{stem_name}.wav")
        save_audio(stem_tensor, stem_path, samplerate=separator.samplerate)
        stem_paths[stem_name] = stem_path

    return SeparationResult(
        vocals_path=stem_paths.get("vocals", ""),
        drums_path=stem_paths.get("drums", ""),
        bass_path=stem_paths.get("bass", ""),
        other_path=stem_paths.get("other", ""),
        stem_paths=stem_paths,
    )
