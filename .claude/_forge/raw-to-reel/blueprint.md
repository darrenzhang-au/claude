# Blueprint: Raw to Reel (`raw-to-reel`)

## Frontmatter
- `name: raw-to-reel`, `version: 1.0.0`
- `description:` one paragraph containing: what it does (raw talking-head → post-ready ≤60s Premiere sequence), ≥5 natural trigger phrases from the brief, and the do-NOT boundary (long-form/podcast silence-stripping → auto-editor-class tools; no-speech; multi-cam/b-roll; in-Vyra sessions; caption-only asks).
- No `handoffs_to`/`expects_from` (struck in manifest — standalone).

## SKILL.md sections (in order)

1. **When to use / when not** — mirrors triggers + exclusions from grill.md verbatim in spirit. Include the two redirects: mechanical-silence-only → auto-editor-class; in-Vyra → Vyra skills.
2. **Prerequisites & preflight** — required: Python 3, ffmpeg/ffprobe on PATH, `faster-whisper` (`pip install faster-whisper`; first run downloads the model). Preflight steps: check deps with exact commands; refuse-with-install-guidance if missing. Probe the video: `ffprobe` for width/height/exact frame rate (keep it rational — 30000/1001, never 29.97 float) and duration. Confirm single video with speech; no speech → decline (out of scope).
3. **Workflow** — seven phases, prose where judgment lives, commands where mechanics live:
   - **P1 Transcribe** — `scripts/transcribe.py <video>` → `words.json` (word-level timestamps + segment confidence markers).
   - **P2 Cut plan (editorial pass)** — read the full transcript first, identify the core message in one sentence, then mark cuts by reason-class: `mistake` (flubbed/restarted/repeated takes — keep the LAST complete take, fall back to most complete; never keep two takes), `filler` (um/uh/like/you know — only when non-semantic), `dead-air` (pauses > ~0.7s beyond natural sentence rhythm), `false-start`. Rule: never cut a span you can't read confidently — keep it and flag ⚠ in the report.
   - **P3 Coherence gate** — read the kept transcript start-to-finish as a first-time viewer; hunt orphaned references ("as I said", "the second reason", callbacks to cut content); fix by restoring or extending cuts. Gate must pass before anything is generated.
   - **P4 Time ladder (only if >60s)** — cut in fixed order: redundancy → weakest tangent → weakest supporting point; label these `time`; core message inviolable; re-run P3 after. If ≤60s is unreachable coherently: deliver shortest coherent cut and say so in the report.
   - **P5 Hook pass** — conservative per D6: prefer cutting preamble so the natural strong line opens; reorder only when a clearly stronger hook exists AND the seam survives P3; label `hook`; state the choice + why in the report.
   - **P6 Cut hygiene** — convert kept spans to source in/out seconds with padding (~150ms before first word, ~150–200ms after last, shrink only if silence doesn't allow); merge gaps < ~120ms; never split mid-word; keep natural micro-pauses at sentence boundaries.
   - **P7 Generate & self-check** — write `cutlist.json` (schema below); run `scripts/make_sequence.py cutlist.json` → emits `sequence.xml` + `captions.srt` + structural self-check (well-formed, in<out, rates consistent, duration = Σ segments). Then write `edit-report.md` and hand over with Premiere import steps (File → Import → sequence.xml; captions: File → Import captions.srt → drag to captions track).
4. **`cutlist.json` schema** — `{ video (abs path), width, height, fps: {num, den}, segments: [{in, out}] in OUTPUT order (seconds, source-relative), words: [{w, start, end}] source-relative for kept words only }`. Script re-times everything to sequence time; sequence is 1080×1920 @ source fps; adds fill-height scale for landscape sources (D7).
5. **Integrity rules** — never cut mid-word; never cut what you can't read; core message inviolable; every cut appears in the report with timecode + reason-class; non-destructive (XML references original media; never re-encode/render); user's explicit prefs (platform, duration, "don't reorder") override all defaults; max 2 retries on tooling failures then report.
6. **Output format** — `<clip-name>-edit/` folder: `sequence.xml`, `captions.srt`, `edit-report.md`, `cutlist.json` (kept for reproducibility). Report template: final runtime + words/sec; the chosen hook decision; cut table (source TC in–out, duration, reason-class, first words, ⚠ flags); kept-transcript readout; import steps.
7. **Anti-patterns** — mechanical silence-cutting as a substitute for editorial judgment; keeping two takes of one line; reordering that breaks tense/continuity; guessing fps or using float 29.97; hand-writing XML instead of running the script; hitting exactly 60s at the cost of coherence; rendering an MP4; silently deciding anything the report doesn't mention.

## Assets
- `scripts/transcribe.py` — faster-whisper wrapper → `words.json` (word timestamps, avg logprob per segment as confidence). Graceful error if faster-whisper missing.
- `scripts/make_sequence.py` — cutlist.json → FCP7 `<xmeml version="4">` sequence (Premiere 2022-importable): rational rate + NTSC flag, 1080×1920 sequence, one V1/A1 track pair, per-clip Basic Motion scale when source aspect ≠ 9:16, `pathurl` as file URI; plus SRT generation (≤4 words/cue, ≥0.5s, re-timed to sequence); plus structural self-check; stdlib only, no deps.
- `references/examples/` — 3 golden examples from grill scenarios 1–3 (input description + output-property assertions).

## Trigger Arena plan (Verify)
Labeled set ≥12 prompts. Should-fire (6): the natural phrases from the brief + paraphrases ("edit out my bad takes", "this take is full of ums, make it postable"). Should-NOT-fire (6): 20-min podcast silence removal; "add captions to this finished video"; "compress this video for WhatsApp"; "edit this in Vyra"; "make a reel from these 10 photos" (no speech); "color grade my clip". Bar: precision ≥0.9, recall ≥0.9.

## Deviations from grill
None. All D1–D8 honored.

## Final-gate addendum (user-accepted ideation items)
- **B1 Phone preview render** — new optional P8 + `scripts/render_preview.py`: reads cutlist.json + captions.srt, shells out to ffmpeg (trim/concat filter, scale 540×960, subtitles burn-in) → `preview.mp4`. Offered at handover, rendered on request or when the user asked for a preview up front. Preview is a gut-check artifact, never the deliverable.
- **C1 Post kit** — report gains a final section: 1 social caption draft, 3 title options, 5–8 hashtags, all derived from the kept transcript only (no invented claims).
