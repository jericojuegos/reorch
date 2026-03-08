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
from pipeline.time_stretch import time_stretch_stems, remix_stems
from pipeline.stem_fx import apply_stem_fx
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


class TestStemFx:
    """Tests for per-stem effects processing."""

    def test_drum_stem_is_processed(self, tmp_path):
        """ballad_to_rock should process the drum stem into a new file."""
        separation = _make_mock_separation(str(tmp_path))
        result = apply_stem_fx(separation.stem_paths, "ballad_to_rock", str(tmp_path))
        # Drum path should be different (processed)
        assert result["drums"] != separation.stem_paths["drums"]
        assert os.path.exists(result["drums"])
        info = sf.info(result["drums"])
        assert info.samplerate == 44100
        assert info.channels == 2

    def test_non_drum_stems_unchanged(self, tmp_path):
        """Vocals, bass, other should pass through unchanged for ballad_to_rock."""
        separation = _make_mock_separation(str(tmp_path))
        result = apply_stem_fx(separation.stem_paths, "ballad_to_rock", str(tmp_path))
        for name in ["vocals", "bass", "other"]:
            assert result[name] == separation.stem_paths[name]

    def test_unknown_preset_no_op(self, tmp_path):
        """A preset with no stem FX returns all paths unchanged."""
        separation = _make_mock_separation(str(tmp_path))
        result = apply_stem_fx(separation.stem_paths, "nonexistent_preset", str(tmp_path))
        for name in separation.stem_paths:
            assert result[name] == separation.stem_paths[name]


class TestTimeStretch:
    """Tests for the time-stretch stage."""

    def test_no_op_when_ratio_near_one(self, tmp_path):
        """When original_bpm ≈ target_bpm, stem paths are returned unchanged."""
        separation = _make_mock_separation(str(tmp_path))
        result = time_stretch_stems(
            separation.stem_paths,
            original_bpm=120.0,
            target_bpm=120.3,  # within 0.5% tolerance
            work_dir=str(tmp_path),
        )
        # Paths should be identical (no stretching occurred)
        for name in separation.stem_paths:
            assert result[name] == separation.stem_paths[name]

    @patch("pipeline.time_stretch.pyrb")
    def test_stretch_changes_duration(self, mock_pyrb, tmp_path):
        """Stretching from 120→60 BPM should call pyrb with ratio 0.5."""
        separation = _make_mock_separation(str(tmp_path), duration=2.0)

        # Make pyrb.time_stretch return a doubled-length array
        def fake_stretch(samples, sr, ratio, rbargs=None):
            new_len = int(len(samples) / ratio)
            if samples.ndim > 1:
                return np.zeros((new_len, samples.shape[1]), dtype="float32")
            return np.zeros(new_len, dtype="float32")

        mock_pyrb.time_stretch.side_effect = fake_stretch

        result = time_stretch_stems(
            separation.stem_paths,
            original_bpm=120.0,
            target_bpm=60.0,
            work_dir=str(tmp_path),
        )

        # All 4 stems should have been stretched
        assert mock_pyrb.time_stretch.call_count == 4
        for stem_path in result.values():
            assert os.path.exists(stem_path)
            info = sf.info(stem_path)
            # 2s original at 2x stretch → ~4s
            assert info.duration > 3.5

    def test_remix_sums_stems(self, tmp_path):
        """remix_stems produces a single WAV matching the longest stem."""
        separation = _make_mock_separation(str(tmp_path), duration=2.0)
        remixed = remix_stems(separation.stem_paths, str(tmp_path))
        assert os.path.exists(remixed)
        info = sf.info(remixed)
        assert info.samplerate == 44100
        assert info.channels == 2
        assert abs(info.duration - 2.0) < 0.1


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

    @patch("pipeline.time_stretch.pyrb")
    @patch("pipeline.separate")
    def test_end_to_end_with_target_bpm(self, mock_separate_fn, mock_pyrb, tmp_path):
        """Full pipeline with target_bpm triggers time-stretch."""
        src = create_test_wav(str(tmp_path / "input.wav"), duration=3.0)
        output_dir = str(tmp_path / "final_bpm")

        mock_separation = _make_mock_separation(str(tmp_path))
        mock_separate_fn.return_value = mock_separation

        # pyrb.time_stretch returns same-length array (ratio ≈ 1 in practice)
        def fake_stretch(samples, sr, ratio, rbargs=None):
            return samples

        mock_pyrb.time_stretch.side_effect = fake_stretch

        progress_log = []

        async def on_progress(pct, msg):
            progress_log.append((pct, msg))

        result = asyncio.get_event_loop().run_until_complete(
            run_pipeline(
                input_path=src,
                output_dir=output_dir,
                preset="ballad_to_rock",
                target_bpm=90.0,
                on_progress=on_progress,
            )
        )

        assert os.path.exists(result.wav_path)
        assert os.path.exists(result.mp3_path)
        assert mock_pyrb.time_stretch.call_count == 4
        # Progress should include time-stretch messages
        stretch_msgs = [msg for _, msg in progress_log if "Time-stretch" in msg or "stretch" in msg.lower()]
        assert len(stretch_msgs) > 0

