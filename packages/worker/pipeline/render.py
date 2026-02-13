"""
Stage 5: Final render — export to WAV and MP3.
"""
import os
from dataclasses import dataclass

import soundfile as sf
from pydub import AudioSegment


@dataclass
class RenderResult:
    """Paths to rendered output files."""
    wav_path: str
    mp3_path: str


def render(normalized_path: str, output_dir: str) -> RenderResult:
    """
    Render the final output to WAV and MP3 formats.

    Args:
        normalized_path: Path to loudness-normalized WAV.
        output_dir: Directory to write final output files.

    Returns:
        RenderResult with paths to WAV and MP3 outputs.
    """
    wav_path = os.path.join(output_dir, "result.wav")
    mp3_path = os.path.join(output_dir, "result.mp3")

    # WAV — copy the normalized file (already in final format)
    audio = AudioSegment.from_wav(normalized_path)
    audio.export(wav_path, format="wav")

    # MP3 — 320kbps for highest quality
    audio.export(mp3_path, format="mp3", bitrate="320k")

    return RenderResult(wav_path=wav_path, mp3_path=mp3_path)
