"""
Stage 3c: Per-stem effects processing — apply preset-specific
effects to individual stems before remix.

Supports:
- Per-stem Pedalboard chains with parallel compression (drums, bass).
- Cross-stem sidechain ducking (bass ducks on drum transients).
"""
import os
from dataclasses import dataclass

import numpy as np
import soundfile as sf
from pedalboard import (
    Compressor,
    Distortion,
    HighpassFilter,
    LowShelfFilter,
    PeakFilter,
    Pedalboard,
)


# Dry/wet mix ratio for parallel compression.
# 0.0 = fully dry, 1.0 = fully wet.
PARALLEL_WET = 0.6


# Per-stem effect chains keyed by preset and stem name.
# Only stems listed here are processed; others pass through unchanged.
STEM_FX: dict[str, dict[str, Pedalboard]] = {
    "ballad_to_rock": {
        "drums": Pedalboard([
            # Remove sub-rumble before saturation
            HighpassFilter(cutoff_frequency_hz=60.0),
            # Aggressive compression for punch
            Compressor(
                threshold_db=-18.0,
                ratio=6.0,
                attack_ms=2.0,
                release_ms=80.0,
            ),
            # Heavier saturation / grit
            Distortion(drive_db=12.0),
            # Snap / attack emphasis at 5 kHz
            PeakFilter(cutoff_frequency_hz=5000.0, gain_db=3.0, q=1.4),
        ]),
        "bass": Pedalboard([
            # Remove inaudible sub-rumble
            HighpassFilter(cutoff_frequency_hz=30.0),
            # Sub-bass enhancement
            LowShelfFilter(cutoff_frequency_hz=80.0, gain_db=4.0),
            # Tighten bass dynamics
            Compressor(
                threshold_db=-22.0,
                ratio=3.0,
                attack_ms=10.0,
                release_ms=150.0,
            ),
        ]),
        "vocals": Pedalboard([
            # Remove low-end mud from vocals
            HighpassFilter(cutoff_frequency_hz=80.0),
            # Surgical EQ: cut muddiness around 200 Hz
            PeakFilter(cutoff_frequency_hz=200.0, gain_db=-2.5, q=1.5),
            # Mid-range presence boost for clarity and intelligibility
            PeakFilter(cutoff_frequency_hz=3000.0, gain_db=3.5, q=1.2),
            # De-ess: attenuate harsh sibilance around 8 kHz
            PeakFilter(cutoff_frequency_hz=8000.0, gain_db=-3.0, q=2.0),
            # Gentle dynamic control — keeps vocals even without over-compression
            Compressor(
                threshold_db=-20.0,
                ratio=2.5,
                attack_ms=8.0,
                release_ms=120.0,
            ),
        ]),
    },
}


# ---------------------------------------------------------------------------
# Sidechain ducking
# ---------------------------------------------------------------------------

@dataclass
class SidechainConfig:
    """Configuration for cross-stem sidechain ducking."""
    trigger: str       # Stem whose envelope drives the ducking (e.g. "drums")
    target: str        # Stem that gets ducked (e.g. "bass")
    depth: float       # Max attenuation (0.0 = full duck, 1.0 = no duck)
    threshold: float   # Envelope level above which ducking begins
    attack_ms: float = 5.0
    release_ms: float = 50.0


SIDECHAIN_FX: dict[str, SidechainConfig] = {
    "ballad_to_rock": SidechainConfig(
        trigger="drums",
        target="bass",
        depth=0.5,
        threshold=0.15,
    ),
}


def _compute_envelope(
    samples: np.ndarray,
    sr: int,
    attack_ms: float = 5.0,
    release_ms: float = 50.0,
) -> np.ndarray:
    """
    Compute an RMS envelope with attack/release smoothing.

    Args:
        samples: Mono audio samples.
        sr: Sample rate.
        attack_ms: Attack time in milliseconds (fast rise).
        release_ms: Release time in milliseconds (slow decay).

    Returns:
        Envelope array with same length as input.
    """
    attack_coeff = np.exp(-1.0 / (sr * attack_ms / 1000.0))
    release_coeff = np.exp(-1.0 / (sr * release_ms / 1000.0))

    rectified = np.abs(samples)
    envelope = np.zeros_like(rectified)
    prev = 0.0

    for i in range(len(rectified)):
        if rectified[i] > prev:
            prev = attack_coeff * prev + (1 - attack_coeff) * rectified[i]
        else:
            prev = release_coeff * prev + (1 - release_coeff) * rectified[i]
        envelope[i] = prev

    return envelope


def _apply_sidechain_duck(
    target: np.ndarray,
    trigger_envelope: np.ndarray,
    depth: float,
    threshold: float,
) -> np.ndarray:
    """
    Reduce target gain where trigger envelope exceeds threshold.

    Args:
        target: Audio samples to duck (mono or stereo).
        trigger_envelope: Mono envelope of the trigger signal.
        depth: Minimum gain during ducking (0.5 = reduce to 50%).
        threshold: Envelope level above which ducking begins.

    Returns:
        Ducked audio samples.
    """
    # Compute gain reduction: 1.0 when below threshold, ramps to `depth` above
    gain = np.ones_like(trigger_envelope)
    above = trigger_envelope > threshold
    if np.any(above):
        # Normalise the portion above threshold to [0, 1]
        overshoot = (trigger_envelope[above] - threshold) / (trigger_envelope[above].max() - threshold + 1e-10)
        gain[above] = 1.0 - (1.0 - depth) * overshoot

    # Apply gain to target (broadcast for stereo)
    if target.ndim > 1:
        return target * gain[:, np.newaxis]
    return target * gain


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def apply_stem_fx(
    stem_paths: dict[str, str],
    preset: str,
    work_dir: str,
) -> dict[str, str]:
    """
    Apply per-stem effects and cross-stem sidechain ducking.

    Processing order:
    1. Per-stem Pedalboard chains (with parallel compression).
    2. Sidechain ducking (target stem reacts to trigger stem envelope).

    Args:
        stem_paths: Dict mapping stem name → WAV file path.
        preset: Transformation preset name.
        work_dir: Directory for intermediate files.

    Returns:
        Dict mapping stem name → path to processed (or original) WAV.
    """
    chains = STEM_FX.get(preset, {})
    sc_cfg = SIDECHAIN_FX.get(preset)

    if not chains and sc_cfg is None:
        return dict(stem_paths)

    fx_dir = os.path.join(work_dir, "stem_fx")
    os.makedirs(fx_dir, exist_ok=True)

    result: dict[str, str] = {}

    # --- Phase 1: per-stem Pedalboard chains ---
    for stem_name, stem_path in stem_paths.items():
        board = chains.get(stem_name)
        if board is None:
            result[stem_name] = stem_path
            continue

        samples, sr = sf.read(stem_path, dtype="float32")

        # pedalboard expects (channels, samples) for multi-channel
        if samples.ndim > 1:
            samples_t = samples.T
        else:
            samples_t = samples

        wet = board(samples_t, sr)

        if wet.ndim > 1:
            wet = wet.T

        # Parallel compression: blend dry + wet
        blended = (1.0 - PARALLEL_WET) * samples + PARALLEL_WET * wet

        peak = np.max(np.abs(blended))
        if peak > 1.0:
            blended = blended / peak

        out_path = os.path.join(fx_dir, f"{stem_name}.wav")
        sf.write(out_path, blended, sr, subtype="PCM_16")
        result[stem_name] = out_path

    # --- Phase 2: sidechain ducking ---
    if sc_cfg and sc_cfg.trigger in result and sc_cfg.target in result:
        trigger_samples, trigger_sr = sf.read(result[sc_cfg.trigger], dtype="float32")
        target_samples, target_sr = sf.read(result[sc_cfg.target], dtype="float32")

        # Mix trigger to mono for envelope detection
        if trigger_samples.ndim > 1:
            trigger_mono = np.mean(trigger_samples, axis=1)
        else:
            trigger_mono = trigger_samples

        envelope = _compute_envelope(
            trigger_mono, trigger_sr,
            attack_ms=sc_cfg.attack_ms,
            release_ms=sc_cfg.release_ms,
        )

        # Match lengths (pad envelope if target is longer)
        if len(envelope) < len(target_samples):
            envelope = np.pad(envelope, (0, len(target_samples) - len(envelope)))
        elif len(envelope) > len(target_samples):
            envelope = envelope[:len(target_samples)]

        ducked = _apply_sidechain_duck(
            target_samples, envelope,
            depth=sc_cfg.depth,
            threshold=sc_cfg.threshold,
        )

        peak = np.max(np.abs(ducked))
        if peak > 1.0:
            ducked = ducked / peak

        duck_path = os.path.join(fx_dir, f"{sc_cfg.target}_ducked.wav")
        sf.write(duck_path, ducked, target_sr, subtype="PCM_16")
        result[sc_cfg.target] = duck_path

    return result
