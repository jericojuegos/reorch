"""
Integration test for the audio processing pipeline.

Tests each stage independently and the full pipeline end-to-end
using a synthetic WAV file (no S3/Redis/Postgres required).
"""
import os
import sys
import tempfile
import asyncio

import numpy as np
import soundfile as sf

# Add worker root to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.canonicalize import canonicalize
from pipeline.analyze import analyze
from pipeline.normalize import normalize
from pipeline.transform import transform
from pipeline.render import render
from pipeline import run_pipeline


def create_test_wav(path: str, duration: float = 5.0, sr: int = 44100) -> str:
    """Create a synthetic stereo WAV with a 440Hz sine wave."""
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    sine = 0.5 * np.sin(2 * np.pi * 440 * t)
    stereo = np.column_stack([sine, sine])
    sf.write(path, stereo, sr, subtype="PCM_16")
    return path


class TestCanonicalize:
    def test_converts_to_canonical_format(self, tmp_path):
        src = create_test_wav(str(tmp_path / "input.wav"), duration=2.0, sr=22050)
        result = canonicalize(src, str(tmp_path))
        info = sf.info(result)
        assert info.samplerate == 44100
        assert info.channels == 2
        assert info.subtype == "PCM_16"


class TestAnalyze:
    def test_returns_positive_duration(self, tmp_path):
        src = create_test_wav(str(tmp_path / "input.wav"), duration=3.0)
        result = analyze(src)
        assert result.duration_seconds > 2.5
        assert result.duration_seconds < 3.5
        assert result.bpm > 0


class TestTransform:
    def test_applies_preset(self, tmp_path):
        src = create_test_wav(str(tmp_path / "input.wav"), duration=2.0)
        result = transform(src, str(tmp_path), preset="ballad_to_rock")
        assert os.path.exists(result)
        info = sf.info(result)
        assert info.samplerate == 44100

    def test_rejects_unknown_preset(self, tmp_path):
        src = create_test_wav(str(tmp_path / "input.wav"), duration=1.0)
        try:
            transform(src, str(tmp_path), preset="nonexistent")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass


class TestNormalize:
    def test_normalizes_loudness(self, tmp_path):
        import pyloudnorm as pyln

        src = create_test_wav(str(tmp_path / "input.wav"), duration=3.0)
        result = normalize(src, str(tmp_path), target_lufs=-14.0)
        assert os.path.exists(result)

        # Verify LUFS is close to target
        samples, sr = sf.read(result, dtype="float64")
        meter = pyln.Meter(sr)
        measured = meter.integrated_loudness(samples)
        assert abs(measured - (-14.0)) < 1.5, f"LUFS {measured} not close to -14"


class TestRender:
    def test_produces_wav_and_mp3(self, tmp_path):
        src = create_test_wav(str(tmp_path / "input.wav"), duration=2.0)
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        result = render(src, str(output_dir))
        assert os.path.exists(result.wav_path)
        assert os.path.exists(result.mp3_path)
        assert result.wav_path.endswith(".wav")
        assert result.mp3_path.endswith(".mp3")


class TestFullPipeline:
    def test_end_to_end(self, tmp_path):
        src = create_test_wav(str(tmp_path / "input.wav"), duration=3.0)
        output_dir = str(tmp_path / "final")

        progress_log = []

        async def on_progress(pct, msg):
            progress_log.append((pct, msg))

        result = asyncio.get_event_loop().run_until_complete(
            run_pipeline(
                input_path=src,
                output_dir=output_dir,
                preset="ballad_to_rock",
                on_progress=on_progress,
            )
        )

        # Check outputs exist
        assert os.path.exists(result.wav_path)
        assert os.path.exists(result.mp3_path)

        # Check analysis was performed
        assert result.analysis.duration_seconds > 2.5
        assert result.analysis.bpm > 0

        # Check progress callbacks fired
        assert len(progress_log) > 0
        assert progress_log[-1][0] == 100
