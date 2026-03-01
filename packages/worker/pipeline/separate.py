"""
Stage 3: Stem separation — isolate vocals, drums, bass, and other.

Uses Facebook's Demucs (Hybrid Transformer) model via the pretrained + apply API.
"""
import os
from dataclasses import dataclass, field
from pathlib import Path

import torch
import torchaudio
from demucs.pretrained import get_model
from demucs.apply import apply_model
from demucs.audio import save_audio

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

    # Load the pretrained model
    model = get_model(settings.demucs_model)
    model.to(device)

    # Load audio and convert to model's expected format
    wav, sr = torchaudio.load(canonical_path)

    # Resample if needed
    if sr != model.samplerate:
        wav = torchaudio.transforms.Resample(sr, model.samplerate)(wav)

    # Normalize reference for stable separation
    ref = wav.mean(0)
    wav = (wav - ref.mean()) / (ref.std() + 1e-8)

    # Apply the model — returns tensor of shape (sources, channels, samples)
    sources = apply_model(
        model,
        wav[None].to(device),
        shifts=settings.demucs_shifts,
        split=True,
        overlap=0.25,
        progress=False,
    )

    # Denormalize
    sources = sources * ref.std() + ref.mean()
    sources = sources.squeeze(0)  # Remove batch dim → (sources, channels, samples)

    # Save each stem to disk
    stems_dir = os.path.join(work_dir, "stems")
    os.makedirs(stems_dir, exist_ok=True)

    stem_paths: dict[str, str] = {}
    for i, stem_name in enumerate(model.sources):
        stem_path = os.path.join(stems_dir, f"{stem_name}.wav")
        save_audio(sources[i], stem_path, samplerate=model.samplerate)
        stem_paths[stem_name] = stem_path

    return SeparationResult(
        vocals_path=stem_paths.get("vocals", ""),
        drums_path=stem_paths.get("drums", ""),
        bass_path=stem_paths.get("bass", ""),
        other_path=stem_paths.get("other", ""),
        stem_paths=stem_paths,
    )
