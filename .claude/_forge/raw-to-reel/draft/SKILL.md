---
name: raw-to-reel
version: 1.0.0
description: >
  Turn one raw talking-to-camera video into a post-ready ≤60-second short-form edit, delivered as a
  Premiere Pro-importable sequence (FCP7 XML, 9:16) plus SRT captions and a cut report. Transcribes with
  word-level timestamps, then makes EDITORIAL cuts — flubbed/repeated takes (keeps the last complete one),
  filler words, dead air, false starts — tightens for time through a coherence gate so the surviving
  message still makes sense, and leads with the hook. Trigger when the user says "clean up this raw video
  for socials", "remove the mistakes from my talking-head clip", "turn this raw take into a reel",
  "make this post-ready — cut the flubs and dead air", "get this down to 60 seconds for TikTok/Shorts",
  or "I recorded myself talking, edit out the bad takes". Do NOT use for long-form content or mechanical
  silence-stripping of podcasts/lectures (point at auto-editor-class tools), videos without speech,
  multi-cam / b-roll-driven / interview or multi-speaker edits, repurposing an already-finished long video
  into clips, editing inside a connected Vyra session (use Vyra's own skills), or caption-only /
  format-conversion-only asks.
---

# Raw to Reel

You are the editor. The user hands you a raw talking-head recording — restarts, ums, dead air, tangents —
and you hand back an edit they can post: every mistake gone, the message intact, the strongest line up
front, under 60 seconds, as a sequence they open in Premiere Pro with all cuts already made. The mechanical
work (transcription, XML generation) is scripted; the editorial judgment — what to cut, what must survive,
whether the result still makes sense — is yours, and it is the whole point of this skill.

## When to use

- The user points at a raw talking-to-camera / selfie-style video with speech and wants it made postable:
  mistakes, retakes, filler, or awkwardness removed for Reels / TikTok / Shorts.
- Output target is short-form (≤60s by default; honor an explicit different cap).

**When NOT to use** (decline and redirect):
- Long-form (podcast, lecture, >~90s target) or "just strip the silences" — that's a mechanical job;
  point at auto-editor-class tools.
- No speech (montage/music content) — the entire engine is transcript-driven.
- Multi-cam, b-roll-driven, or interview/multi-speaker edits.
- The user is editing inside a connected Vyra session — Vyra's own skills apply there.
- Caption-only, thumbnail, compression, or format-conversion asks.

## Prerequisites & preflight

Required: Python 3, `ffprobe` (ffmpeg) on PATH, `faster-whisper` (`pip install faster-whisper`; first run
downloads a model). Before any editing:

1. Check dependencies (`ffprobe -version`, `python -c "import faster_whisper"`). If missing, stop and give
   the exact install command — never guess timestamps without them.
2. Probe the source:
   `ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,duration -of json <video>`
   Keep the frame rate **rational** (e.g. `30000/1001`) — never a rounded float.
3. Confirm exactly one input video and that it contains speech. No speech → decline (out of scope).
4. Create the output folder `<clip-name>-edit/` next to the source.

## Workflow

### P1 — Transcribe
Run `python scripts/transcribe.py <video> <clip-name>-edit/words.json`. This produces word-level timestamps
plus a per-segment confidence signal. Read the full transcript before deciding anything.

### P2 — Cut plan (the editorial pass)
First write down the **core message in one sentence** — it is inviolable for the rest of the run. Then mark
cuts, each with a reason-class:

- `mistake` — flubbed, restarted, or repeated takes. Detect near-duplicate lines; **keep the LAST complete
  take** (creators re-record until they nail it). If the last is incomplete or garbled, fall back to the
  most complete take and note it. Never keep two takes of the same line.
- `false-start` — sentence fragments abandoned mid-thought.
- `filler` — um / uh / like / you know / sort of — only where non-semantic ("I like this" keeps its "like").
- `dead-air` — pauses beyond natural sentence rhythm (roughly >0.7s), keeping micro-pauses at sentence
  boundaries so the pacing breathes.

Hard rule: **never cut a span you can't read confidently.** Garbled or low-confidence segments are kept,
not cut, and flagged ⚠ in the report for human review.

### P3 — Coherence gate
Read the kept transcript start-to-finish as a first-time viewer. Hunt orphans: "as I said earlier",
"the second reason" whose first was cut, callbacks to removed content, tense breaks at seams. Fix each by
restoring or extending cuts. Nothing is generated until this gate passes.

### P4 — Time ladder (only if still >60s)
Cut in this fixed order, labeling cuts `time`: redundant restatements → weakest tangent → weakest
supporting point. The core message is never on the ladder. Re-run P3 after. If ≤60s is unreachable without
breaking coherence, deliver the shortest coherent cut over 60s and say so plainly in the report.

### P5 — Hook pass
Prefer **cutting preamble** ("hey guys, so today…") so the natural strongest line opens within ~2s of
speech. Reorder a later line to the front only when it is clearly stronger AND the seam survives the
coherence gate — no dangling connectives at the join, no implied re-recording. Label `hook`; state the
choice and why in the report. If the user said "don't reorder", don't.

### P6 — Cut hygiene
Convert kept spans to source in/out seconds: pad ~150ms before the first word and ~150–200ms after the
last (shrink only when neighboring speech doesn't allow); merge kept spans separated by <120ms; never split
mid-word. Cuts are straight jump-cuts — the accepted short-form aesthetic; no dissolves, no b-roll.

### P7 — Generate & self-check
Write `cutlist.json` into the output folder:

```json
{
  "video": "<absolute path>",
  "width": 3840, "height": 2160,
  "fps": { "num": 30000, "den": 1001 },
  "segments": [ { "in": 12.48, "out": 19.02 } ],
  "words": [ { "w": "Here's", "start": 12.61, "end": 12.90 } ]
}
```
`segments` are source-relative seconds **in output order** (a hook reorder is just segment order); `words`
are the kept words only, source-relative — the script re-times them to the sequence.

Run `python scripts/make_sequence.py <clip-name>-edit/cutlist.json`. It emits `sequence.xml` (FCP7 XML:
1080×1920 sequence at the source's exact frame rate, fill-height scale for landscape sources) and
`captions.srt` (≤4-word cues re-timed to the edit), and runs a structural self-check (parses, in<out,
rates consistent, sequence duration = Σ segments). A failed self-check is a stop — fix, don't hand over.

Then write `edit-report.md` (format below) and hand over with import steps.

### P8 — Phone preview (optional)
Offer it at handover (render immediately if the user asked for a preview up front):
`python scripts/render_preview.py <clip-name>-edit/cutlist.json` renders `preview.mp4` — 540×960, the
exact edit with captions burned in — for a pacing gut-check on a phone before opening Premiere. It is a
scratch render, never the deliverable; the deliverable remains the non-destructive sequence.

## Integrity rules

- Never cut mid-word; never cut what you can't read; the core message is inviolable.
- Every cut appears in the report with source timecode and reason-class — no silent judgment calls.
- Non-destructive: the XML references the original media; never re-encode, render, or modify the source.
- The user's explicit preferences (platform, duration cap, "keep it chronological") override every default.
- Max 2 retries on a failing tool step, then report what failed and what you tried.

## Output

`<clip-name>-edit/` containing `sequence.xml`, `captions.srt`, `edit-report.md`, `cutlist.json`
(kept for reproducibility), `words.json`. The report contains, in order:

1. **Result** — final runtime, words/sec, hook decision (moved / preamble-cut / unchanged) and why.
2. **Cut table** — source TC in–out, duration, reason-class (`mistake | false-start | filler | dead-air |
   time | hook`), first words of the cut span, ⚠ on any low-confidence call.
3. **Kept transcript** — the surviving message, readable top to bottom.
4. **Import steps** — Premiere Pro 2022: File → Import → `sequence.xml` (sequence appears in Project
   panel, cuts applied); File → Import → `captions.srt`, drag onto the sequence's captions track and apply
   a style; adjust the fill-height framing with one Position drag if the crop needs it.
5. **Post kit** — drafted from the kept transcript only (never invent claims the video doesn't make):
   one social caption, three title options, and 5–8 relevant hashtags, ready to paste when posting.

## Anti-patterns

- Mechanical silence-cutting as a substitute for editorial judgment — that's auto-editor's job, not yours.
- Keeping two takes of the same line, or keeping the first take because it came first.
- A reorder that breaks tense or continuity — a technically clean edit of an incoherent message is a bad output.
- Guessing the frame rate, or writing 29.97 as a float — use the rational from ffprobe.
- Hand-writing the XML instead of running `make_sequence.py`.
- Hitting exactly 60s at the cost of coherence, or over-tightening into robotic pacing.
- Treating the preview render as the deliverable — `preview.mp4` is a low-res gut-check; the user
  finishes and exports from Premiere.
- A post kit that oversells — captions/titles must be grounded in what the kept transcript actually says.
