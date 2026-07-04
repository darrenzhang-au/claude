# Changelog — raw-to-reel

## v1.0.0 — 2026-07-03
- Initial release, forged via skill-forge (full route, auto mode).
- Editorial pipeline: word-level transcription (faster-whisper) → mistake/retake/filler/dead-air cuts
  (keep-last-complete-take) → coherence gate → ≤60s time ladder → conservative hook pass → cut hygiene.
- Deliverables: FCP7 XML sequence (Premiere Pro 2022-importable, 1080x1920 @ source fps, non-destructive),
  re-timed SRT captions, edit report (cut table + kept transcript + import steps + post kit).
- Scripts: transcribe.py, make_sequence.py (with structural self-check; smoke-tested), render_preview.py
  (optional 540x960 gut-check render, captions burned in).
- Final-gate opt-ins integrated: B1 phone preview render, C1 post kit.
