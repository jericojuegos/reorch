## UAT CHECKLIST — Audio Enhancements (Phase 2 Sprint)

> **Trigger:** All Audio Enhancements tasks complete (`[x]`).  
> **Environment:** Docker worker running locally OR staging environment with real audio file.  
> **Prerequisite:** A 3–5 min WAV/MP3 song file in the ballad/rock genre to use as test input.

---

### ENVIRONMENT SETUP

Before running any scenario:

1. `docker compose up --build worker` — rebuild worker with new Dockerfile (includes `rubberband-cli`)
2. Confirm `pyrubberband` is importable: `docker exec <worker> python -c "import pyrubberband"`
3. Have a test audio file ready (e.g. a ballad in WAV/MP3 format)
4. Have an audio player + a spectrum analyser (e.g. Audacity) to verify changes

---

### LEVEL 1 — AUTOMATED (Already verified by agent)

- [x] `TestTimeStretch` (3 tests) — no-op at ratio~1, duration changes, stems remix correctly
- [x] `TestStemFx` (6 tests) — drums processed, bass processed + ducked, vocals processed, other unchanged, unknown preset is no-op
- [x] `TestNormalize` (2 tests) — LUFS near −14, true peak stays ≤ −1.0 dBFS

---

### LEVEL 2 — UAT CHECKLIST (You execute manually)

#### 🎸 Stem Separation

- [ ] Stems are produced as individual files in S3
  - Steps: Submit a job → check S3 bucket → look for `vocals.wav`, `drums.wav`, `bass.wav`, `other.wav`
  - Pass: All 4 stem files present, each > 0 bytes

- [ ] Stem separation completes within a reasonable time
  - Steps: Submit job, observe logs
  - Pass: Separation stage finishes within ~2× the song's duration

- [ ] Per-stem metadata appears in analysis result
  - Steps: Submit job → check Redis job result payload
  - Pass: `analysis.stem_durations` and `analysis.stem_rms` both populated with 4 entries

---

#### ⏱ Time-Stretch (Stem-Aligned)

- [ ] Pipeline accepts a `target_bpm` job parameter
  - Steps: Submit job with `target_bpm: 140` on a ~100 BPM track
  - Pass: Logs show `"Time-stretching stems (100 → 140 BPM)"` progress message

- [ ] Output duration changes proportionally when BPM changes
  - Steps: Compare output WAV duration to input duration
  - Pass: `output_duration ≈ input_duration × (source_bpm / target_bpm)` (within ~2%)

- [ ] No time-stretch when target BPM is absent or very close to source
  - Steps: Submit job with no `target_bpm`, or with `target_bpm` within 0.5 BPM of source
  - Pass: No `"Time-stretching"` log message; output duration matches input

- [ ] Vocal pitch is preserved despite tempo change
  - Steps: Listen to the vocal stem at a 20% speed change
  - Pass: Vocals sound naturally pitched — no "chipmunk" or "slowed-down" artefacts

---

#### 🥁 Drum Energy (Rock Preset)

- [ ] Output drums sound punchier than input
  - Steps: Open input and output in Audacity; observe drum stem waveform peaks
  - Pass: RMS of drum region is visibly higher in output; transients are sharper

- [ ] No distortion artefacts from over-saturation
  - Steps: Listen at full volume
  - Pass: Drums sound driven/gritty, not harshly distorted or blown-out

---

#### 🎸 Bass Low-End Control

- [ ] Sub-bass is more prominent in output
  - Steps: Open output in Audacity → Analyze → Plot Spectrum → check 30–80 Hz region
  - Pass: Energy in 30–80 Hz band is higher in output than input

- [ ] Bass ducks during drum hits (sidechain effect)
  - Steps: Listen to the output mix — bass should "pump" rhythmically with kicks
  - Pass: Audible sidechain breathing effect; bass doesn't mud-mask drums

- [ ] Bass does not clip or peak above 0 dBFS
  - Steps: Check waveform in Audacity
  - Pass: No flat-top clipping visible; peaks stay below 0 dBFS

---

#### 🎤 Vocal Presence

- [ ] Vocals are clearer and more intelligible
  - Steps: Listen to vocals in the full mix vs. original
  - Pass: Vocals cut through the mix without sounding harsh or thin

- [ ] Sibilance reduced ("s", "sh" sounds are less sharp)
  - Steps: Focus on sibilant words during playback
  - Pass: "Ss" sounds are smooth, not piercing or hissy

- [ ] Low-end mud removed from vocals
  - Steps: Open output stem in Audacity → check that below 80 Hz is near-silent
  - Pass: Vocal stem has no significant energy below 80 Hz

---

#### 🎛 Mastering Chain (LUFS + True Peak)

- [ ] Output loudness is near −14 LUFS
  - Steps: Open final WAV in a LUFS meter (Audacity > Analyse > Contrast, or `ffmpeg -af ebur128`)
  - Pass: Integrated loudness is between −15.5 LUFS and −12.5 LUFS

- [ ] True peak does not exceed −1.0 dBTP
  - Steps: Check in Audacity (Effect > Amplify shows headroom) or `ffmpeg -af ebur128:peak=true`
  - Pass: True peak ≤ −1.0 dBTP — no over-limit warnings

- [ ] Silent/near-silent input does not crash the normaliser
  - Steps: Submit a nearly-silent audio file as input
  - Pass: Job completes successfully; output is a near-silent file (no divide-by-zero crash)

---

#### 🔁 Full End-to-End Pipeline

- [ ] Happy path with `target_bpm` — complete job succeeds
  - Steps: `POST /jobs { audio_url: "...", preset: "ballad_to_rock", target_bpm: 130 }`
  - Pass: Job status → `complete`; WAV + MP3 in S3; all 4 stems in S3

- [ ] Happy path without `target_bpm` — complete job succeeds
  - Steps: `POST /jobs { audio_url: "...", preset: "ballad_to_rock" }`
  - Pass: Job status → `complete`; no time-stretch log messages

- [ ] Invalid preset name handled gracefully
  - Steps: `POST /jobs { audio_url: "...", preset: "nonexistent_preset" }`
  - Pass: Job fails with clear error message, not an unhandled exception

- [ ] Corrupted / unreadable audio file
  - Steps: Upload a text file with a `.mp3` extension
  - Pass: Job fails at `canonicalize` stage with a clear error; no worker crash

- [ ] Progress updates are emitted throughout the pipeline
  - Steps: Subscribe to job progress channel during processing
  - Pass: Progress ticks seen at each stage (0 → 10 → 20 → ... → 100%)

---

### LEVEL 3 — USER JUDGMENT (Subjective listening test)

These are for you to evaluate — no "pass/fail" — just a gut check:

- [ ] 🎧 Does the output feel like a credible rock transformation of the input ballad?
- [ ] 🎧 Is the drum kit energetic but not fatiguing?
- [ ] 🎧 Does the bass feel tight and punchy, not muddy?
- [ ] 🎧 Do the vocals sit comfortably in the mix?
- [ ] 🎧 Does the final master feel appropriately loud (not quiet, not ear-splitting)?
- [ ] 🎧 Would you share this output with someone as a demo?
