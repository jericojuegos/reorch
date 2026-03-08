"""
REORCH Audio Processing Pipeline.

Orchestrates the full processing chain:
  canonicalize → analyze → separate → transform → normalize → render
"""
import os
import tempfile
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Awaitable

from pipeline.canonicalize import canonicalize
from pipeline.analyze import analyze, analyze_stems, AnalysisResult
from pipeline.separate import separate, SeparationResult
from pipeline.time_stretch import time_stretch_stems, remix_stems
from pipeline.stem_fx import apply_stem_fx
from pipeline.transform import transform
from pipeline.normalize import normalize
from pipeline.render import render, RenderResult


@dataclass
class PipelineResult:
    """Result of a full pipeline run."""
    analysis: AnalysisResult
    separation: SeparationResult
    wav_path: str
    mp3_path: str


async def run_pipeline(
    input_path: str,
    output_dir: str,
    preset: str = "ballad_to_rock",
    target_bpm: Optional[float] = None,
    on_progress: Optional[Callable[[int, str], Awaitable[None]]] = None,
) -> PipelineResult:
    """
    Run the full audio processing pipeline.

    Args:
        input_path: Path to the input audio file.
        output_dir: Directory to write final outputs.
        preset: Transformation preset name.
        on_progress: Async callback(percent, stage_name) for progress updates.

        target_bpm: Optional target BPM for time-stretching stems. If None,
            no tempo change is applied.

    Returns:
        PipelineResult with analysis data and output file paths.
    """

    async def _progress(pct: int, msg: str):
        if on_progress:
            await on_progress(pct, msg)

    # Use a temp directory for intermediate files
    work_dir = tempfile.mkdtemp(prefix="reorch_pipeline_")

    try:
        # Stage 1: Canonicalize (0–10%)
        await _progress(5, "Canonicalizing audio")
        canonical_path = canonicalize(input_path, work_dir)
        await _progress(10, "Canonicalization complete")

        # Stage 2: Analyze (10–20%)
        await _progress(15, "Analyzing audio")
        analysis = analyze(canonical_path)
        await _progress(20, f"Analysis complete (BPM: {analysis.bpm:.0f}, duration: {analysis.duration_seconds:.1f}s)")

        # Stage 3: Separate stems (20–50%)
        await _progress(25, "Separating stems (vocals, drums, bass, other)")
        separation = separate(canonical_path, work_dir)
        await _progress(45, "Stem separation complete — analyzing stems")

        # Enrich analysis with per-stem metadata
        stem_meta = analyze_stems(separation.stem_paths)
        analysis.stem_durations = stem_meta["durations"]
        analysis.stem_rms = stem_meta["rms"]
        await _progress(50, "Stem analysis complete")

        # Stage 3b: Time-stretch stems (50–60%)
        current_stems = dict(separation.stem_paths)
        if target_bpm is not None and abs(target_bpm - analysis.bpm) > 0.5:
            await _progress(52, f"Time-stretching stems ({analysis.bpm:.0f} → {target_bpm:.0f} BPM)")
            current_stems = time_stretch_stems(
                current_stems, analysis.bpm, target_bpm, work_dir,
            )
            await _progress(58, "Stem time-stretch complete")

        # Stage 3c: Per-stem effects (58–60%)
        await _progress(59, f"Applying per-stem FX ({preset})")
        current_stems = apply_stem_fx(current_stems, preset, work_dir)

        # Remix stems into a single mix for the transform stage
        await _progress(60, "Remixing stems")
        remix_path = remix_stems(current_stems, work_dir)
        await _progress(60, "Remix complete")

        # Stage 4: Transform (60–75%)
        await _progress(62, f"Applying {preset} transformation")
        transformed_path = transform(remix_path, work_dir, preset=preset)
        await _progress(75, "Transformation complete")

        # Stage 5: Normalize (75–90%)
        await _progress(80, "Normalizing loudness")
        normalized_path = normalize(transformed_path, work_dir)
        await _progress(90, "Normalization complete")

        # Stage 6: Render (90–100%)
        await _progress(95, "Rendering final output")
        os.makedirs(output_dir, exist_ok=True)
        result = render(normalized_path, output_dir)
        await _progress(100, "Render complete")

        return PipelineResult(
            analysis=analysis,
            separation=separation,
            wav_path=result.wav_path,
            mp3_path=result.mp3_path,
        )
    finally:
        # Clean up intermediate files
        shutil.rmtree(work_dir, ignore_errors=True)
