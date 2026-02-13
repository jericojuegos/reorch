"""
REORCH Audio Processing Pipeline.

Orchestrates the full processing chain:
  canonicalize → analyze → transform → normalize → render
"""
import os
import tempfile
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Awaitable

from pipeline.canonicalize import canonicalize
from pipeline.analyze import analyze, AnalysisResult
from pipeline.transform import transform
from pipeline.normalize import normalize
from pipeline.render import render, RenderResult


@dataclass
class PipelineResult:
    """Result of a full pipeline run."""
    analysis: AnalysisResult
    wav_path: str
    mp3_path: str


async def run_pipeline(
    input_path: str,
    output_dir: str,
    preset: str = "ballad_to_rock",
    on_progress: Optional[Callable[[int, str], Awaitable[None]]] = None,
) -> PipelineResult:
    """
    Run the full audio processing pipeline.

    Args:
        input_path: Path to the input audio file.
        output_dir: Directory to write final outputs.
        preset: Transformation preset name.
        on_progress: Async callback(percent, stage_name) for progress updates.

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

        # Stage 2: Analyze (10–25%)
        await _progress(15, "Analyzing audio")
        analysis = analyze(canonical_path)
        await _progress(25, f"Analysis complete (BPM: {analysis.bpm:.0f}, duration: {analysis.duration_seconds:.1f}s)")

        # Stage 3: Transform (25–60%)
        await _progress(30, f"Applying {preset} transformation")
        transformed_path = transform(canonical_path, work_dir, preset=preset)
        await _progress(60, "Transformation complete")

        # Stage 4: Normalize (60–85%)
        await _progress(65, "Normalizing loudness")
        normalized_path = normalize(transformed_path, work_dir)
        await _progress(85, "Normalization complete")

        # Stage 5: Render (85–100%)
        await _progress(90, "Rendering final output")
        os.makedirs(output_dir, exist_ok=True)
        result = render(normalized_path, output_dir)
        await _progress(100, "Render complete")

        return PipelineResult(
            analysis=analysis,
            wav_path=result.wav_path,
            mp3_path=result.mp3_path,
        )
    finally:
        # Clean up intermediate files
        shutil.rmtree(work_dir, ignore_errors=True)
