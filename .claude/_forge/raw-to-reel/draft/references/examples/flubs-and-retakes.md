# Golden Example 1 — Flubs & retakes (the core job)

## Input
One 3-minute 16:9 clip (3840×2160, 30000/1001 fps). The creator:
- restarts one sentence three times ("So the first thing— So the— So the first thing you need to know is…"),
- says "um" / "like" throughout,
- leaves ~4s of dead air twice while checking notes.
Ask: "turn this into a reel".

## A great output asserts
- [ ] The transcript was read fully and the core message stated in one sentence before any cut was marked.
- [ ] Only the LAST complete take of the restarted sentence survives; both earlier attempts are cut as `mistake`.
- [ ] Non-semantic "um"/"like" cut as `filler`; a semantic "like" (comparison) is untouched.
- [ ] Dead-air spans cut as `dead-air`, but natural micro-pauses at sentence boundaries remain (no robotic pacing).
- [ ] Final runtime ≤60s.
- [ ] `sequence.xml`: 1080×1920, timebase 30 + NTSC TRUE (never float 29.97), fill-height scale on clips, passes the script self-check.
- [ ] `captions.srt` cues are ≤4 words and re-timed to the edited sequence, not source time.
- [ ] `edit-report.md` lists every cut with source timecode + reason-class, includes the kept transcript, and gives Premiere import steps.
- [ ] Source file untouched; no deliverable MP4 rendered (the optional `preview.mp4` gut-check is offered, not forced).
- [ ] Report ends with a post kit — caption, 3 titles, hashtags — grounded strictly in the kept transcript.

## A bad output
Keeps the first take because it came first; strips every pause flat; cuts a garbled span it couldn't read; report omits cuts.
