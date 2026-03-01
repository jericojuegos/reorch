"""
Integration test for the audio processing pipeline.

Tests each stage independently and the full pipeline end-to-end
using a synthetic WAV file (no S3/Redis/Postgres required).

Note: Stem separation (Demucs) is mocked in tests to avoid
downloading the ~1.2GB model in CI.
"""
import os
import sys
import tempfile
import asyncio
from unittest.mock import patch, MagicMock

import numpy as np
import soundfile as sf

# Add worker root to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.canonicalize import canonicalize
from pipeline.analyze import analyze, analyze_stems
from pipeline.separate import SeparationResult
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


def _make_mock_separation(work_dir: str, duration: float = 2.0, sr: int = 44100) -> SeparationResult:
    """Create a fake SeparationResult with synthetic stem WAVs."""
    stems_dir = os.path.join(work_dir, "stems")
    os.makedirs(stems_dir, exist_ok=True)

    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    stem_paths = {}
    for i, name in enumerate(["vocals", "drums", "bass", "other"]):
        freq = 440 * (i + 1)
        sine = 0.3 * np.sin(2 * np.pi * freq * t)
        stereo = np.column_stack([sine, sine])
        path = os.path.join(stems_dir, f"{name}.wav")
        sf.write(path, stereo, sr, subtype="PCM_16")
        stem_paths[name] = path

    return SeparationResult(
        vocals_path=stem_paths["vocals"],
        drums_path=stem_paths["drums"],
        bass_path=stem_paths["bass"],
        other_path=stem_paths["other"],
        stem_paths=stem_paths,
    )


class TestSeparate:
    """Mock-based tests for the separation stage (no real Demucs model)."""

    def test_separation_result_has_four_stems(self, tmp_path):
        result = _make_mock_separation(str(tmp_path))
        assert len(result.stem_paths) == 4
        for name in ["vocals", "drums", "bass", "other"]:
            assert name in result.stem_paths
            assert os.path.exists(result.stem_paths[name])

    def test_stem_files_are_valid_wav(self, tmp_path):
        result = _make_mock_separation(str(tmp_path))
        for path in result.stem_paths.values():
            info = sf.info(path)
            assert info.samplerate == 44100
            assert info.channels == 2


class TestAnalyzeStems:
    def test_returns_durations_and_rms(self, tmp_path):
        result = _make_mock_separation(str(tmp_path))
        meta = analyze_stems(result.stem_paths)
        assert "durations" in meta
        assert "rms" in meta
        for name in ["vocals", "drums", "bass", "other"]:
            assert name in meta["durations"]
            assert meta["durations"][name] > 0
            assert name in meta["rms"]
            assert meta["rms"][name] > 0


class TestFullPipeline:
    @patch("pipeline.separate")
    def test_end_to_end(self, mock_separate_fn, tmp_path):
        src = create_test_wav(str(tmp_path / "input.wav"), duration=3.0)
        output_dir = str(tmp_path / "final")

        # Mock the separate function to return synthetic stems
        mock_separation = _make_mock_separation(str(tmp_path))
        mock_separate_fn.return_value = mock_separation

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

        # Check separation result is present
        assert result.separation is not None
        assert len(result.separation.stem_paths) == 4

        # Check per-stem metadata was enriched
        assert result.analysis.stem_durations is not None
        assert result.analysis.stem_rms is not None

        # Check progress callbacks fired
        assert len(progress_log) > 0
        assert progress_log[-1][0] == 100

