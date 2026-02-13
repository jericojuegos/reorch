"""
Stage 1: Canonicalize audio to WAV 44.1kHz 16-bit stereo.
"""
import os

from pydub import AudioSegment


# Canonical format parameters
SAMPLE_RATE = 44100
SAMPLE_WIDTH = 2  # 16-bit = 2 bytes
CHANNELS = 2  # stereo


def canonicalize(input_path: str, work_dir: str) -> str:
    """
    Convert any supported audio file to canonical WAV format.

    Args:
        input_path: Path to input audio (WAV, MP3, etc.)
        work_dir: Directory for intermediate files.

    Returns:
        Path to canonical WAV file.
    """
    audio = AudioSegment.from_file(input_path)

    # Convert to canonical format
    audio = (
        audio
        .set_frame_rate(SAMPLE_RATE)
        .set_sample_width(SAMPLE_WIDTH)
        .set_channels(CHANNELS)
    )

    output_path = os.path.join(work_dir, "canonical.wav")
    audio.export(output_path, format="wav")
    return output_path
