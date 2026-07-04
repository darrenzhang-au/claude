# Refined Brief: Raw to Reel

Auto mode — open questions resolved with recommended defaults, each logged to the decision ledger (flippable at the final gate).

## Resolved in grilling
- Retake handling → **Keep the LAST complete take** of any restarted/repeated line (creators re-record until they nail it). If the last take is itself incomplete or garbled, fall back to the most complete earlier take. Never keep two takes of the same line. (D4)
- Cut hygiene → **Never cut mid-word.** Cuts snap to frame boundaries with breathing padding: ~150ms before the first kept word and ~150–200ms after the last, shrunk only when silence doesn't allow. Straight jump-cuts are the accepted short-form aesthetic — no dissolves, no b-roll patching. (D5)
- Hook pass → **Conservative reorder.** Only move a line to the front when (a) a clearly stronger hook exists later in the clip, and (b) the move survives the coherence gate — no dangling connectives ("so that's why…", "the second reason…") at the new seam. When in doubt, keep chronological order and instead cut preamble so the natural hook arrives fast. Never fabricate or imply re-recorded audio. (D6)
- 9:16 framing → Sequence is **1080×1920 at the source's exact frame rate**; 16:9/4K sources get scale-to-fill-height (center crop) as the default clip transform; report tells the user framing is one drag to adjust in Premiere. (D7)
- Captions → **SRT with short cues (≤4 words, ≥0.5s)** built from kept-content word timestamps, re-timed to the edited sequence. Premiere 2022 imports SRT onto a captions track where the user applies their style — burned-in styling is deliberately left to Premiere. (D8)
- Inputs missing at call time → transcriber/ffprobe absent → preflight check with exact install commands, then stop (don't guess timestamps). Video path ambiguous → ask. No speech detected → refuse with reason (out of scope).

## Exclusions (explicitly out of scope)
- Multi-camera, b-roll, montage, or music-driven edits — single talking-head clip only.
- Long-form (target > ~90s output) — this is a short-form finisher, not a podcast/YouTube editor. Mechanical silence-stripping of long content → point at auto-editor-class tools.
- Multiple speakers / interviews (retake logic and hook logic assume one voice).
- Color, audio sweetening (denoise/EQ/music), motion graphics — Premiere's job after import.
- Rendering a final MP4 — the deliverable is the Premiere sequence, not a render (non-destructive by design).
- Editing inside a connected Vyra session — Vyra's own skills apply there.

## Failure modes & guards
- Failure: transcriber mishears or hallucinates a segment → Guard: **never cut what you can't read confidently** — garbled/low-confidence spans are kept, not cut, and flagged in the report for human review.
- Failure: wrong take kept (last take trails off) → Guard: completeness check on the chosen take; fall back to the most complete take and note it.
- Failure: cuts orphan a reference ("like I said earlier", "reason number two" after reason one was cut) → Guard: **coherence gate** — read the full kept transcript start-to-finish as the audience would; fix orphans by restoring or extending cuts before finalizing.
- Failure: frame-math drift (29.97 NTSC, variable fps) → Guard: exact fps + duration from ffprobe; NTSC rational timebase in the XML; all edits in integer frames.
- Failure: XML won't import into Premiere 2022 → Guard: generator script emits the known-good FCP7 `<xmeml version="4">` shape; structural self-check (well-formed, in<out, tracks non-empty, rate consistent) before handover; report includes import steps + fallback (EDL) guidance.
- Failure: 60s ladder guts the message → Guard: ladder order is fixed (mistakes → filler/dead air → redundancy → weakest tangent → weakest supporting point) and the **core message is inviolable**; if ≤60s is unreachable coherently, deliver the shortest coherent cut over 60s and say so explicitly in the report.
- Failure: over-tightening produces robotic pacing → Guard: padding rules in D5 plus "leave natural micro-pauses at sentence boundaries" rule; report the final words-per-second as a sanity signal.

## Quality bar
- A great output: zero flubs/restarts/filler survive; the kept transcript reads as one coherent message a first-time viewer follows; speech starts on a hook within ~2s; runtime ≤60s; every cut lands on clean audio (no clipped syllables); `sequence.xml` imports into Premiere 2022 first try at correct fps/resolution; captions sync to the edited timeline; the report accounts for every cut with timecode + reason.
- A bad output: mid-word cuts; orphaned references; the best take deleted; a technically clean edit of an incoherent message; >60s with no explanation; XML import errors; silent judgment calls the report never mentions.

## Golden scenarios (seed Build's examples + Verify's replay)
1. **Flubs & retakes.** Input: one 3-min 16:9 clip; creator restarts one sentence three times, says "um/like" throughout, long dead air while checking notes; asks "turn this into a reel". Great output asserts: last complete take of the restarted sentence kept, earlier attempts cut; filler and dead air gone with natural pauses preserved; ≤60s; XML sequence is 1080×1920 at source fps; report lists every cut with timecode + reason; kept transcript reads coherently.
2. **Cut for time without breaking sense.** Input: after mistake-removal the clip is ~75s and contains a mid-clip tangent plus a callback to it near the end. Great output asserts: tangent cut *for time* (labeled as such, distinct from mistake cuts); the later callback line also cut or trimmed so nothing orphaned survives; final ≤60s; core message intact.
3. **Hook decision — both directions.** Input: strongest line ("nobody tells you this about…") sits at 0:40; opening 8s is throat-clearing ("hey guys, so today…"). Great output asserts: either the line is moved to the front *and* the seam survives the coherence gate, or the preamble is cut so the natural strong line opens — and the report states which was chosen and why; captions re-timed either way.
4. **Boundary (must NOT fully fire).** Input: "remove the silences from my 20-minute podcast recording." Great output asserts: skill declines the full pipeline, explains it's a short-form finisher, and points at a mechanical silence-cutter (auto-editor-class) instead.

## Updated triggers / I/O / wedge
- Triggers unchanged from brief.md; exclusion boundary now explicit (long-form redirect, no-speech refusal, Vyra-session boundary).
- I/O sharpened: output folder `<clip-name>-edit/` = `sequence.xml` + `captions.srt` + `edit-report.md`; report gains kept-transcript readout, cut table (timecode, duration, reason-class: mistake | filler | dead-air | time | hook), final runtime, words-per-second.
- Wedge unchanged from novelty.md.

## Deferred (user chose not to decide now)
- None — auto mode; all defaults logged as D4–D8 and flippable at the final gate.
