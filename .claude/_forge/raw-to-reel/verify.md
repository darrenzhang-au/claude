# Verify Report: Raw to Reel

## Trigger Arena
Set sizes: should-fire 8 · near-miss 8 · neighbor 6 · ambiguous 4. Router judged on descriptions only
(candidate + infographic-builder, excalidraw-diagram-generator, skills-sh-finder).

| Prompt | Label | Fired | Hit? | Notes |
|--------|-------|-------|------|-------|
| "clean up this raw video for socials" | raw-to-reel | raw-to-reel | ✓ | |
| "remove the mistakes from my talking-head clip" | raw-to-reel | raw-to-reel | ✓ | |
| "turn this raw take into a reel" | raw-to-reel | raw-to-reel | ✓ | |
| "make this post-ready — cut the flubs and dead air" | raw-to-reel | raw-to-reel | ✓ | |
| "get this down to 60 seconds for TikTok" | raw-to-reel | raw-to-reel | ✓ | |
| "I recorded myself talking, edit out the bad takes" | raw-to-reel | raw-to-reel | ✓ | |
| "this take is full of ums — make it postable" | raw-to-reel | raw-to-reel | ✓ | paraphrase holds |
| "I filmed myself explaining my product, tidy it into a short" | raw-to-reel | raw-to-reel | ✓ | |
| "remove the silences from my 20-min podcast recording" | none | none | ✓ | long-form boundary holds |
| "add captions to this finished video" | none | none | ✓ | caption-only excluded |
| "compress this video for WhatsApp" | none | none | ✓ | |
| "edit this clip in Vyra" | none | none | ✓ | Vyra boundary holds |
| "make a reel from these 10 photos with music" | none | none | ✓ | no speech |
| "color grade my clip" | none | none | ✓ | |
| "edit my interview with two guests into a highlight" | none | **raw-to-reel** | ✗→✓ | pre-fix misfire; description gained interview/multi-speaker boundary; re-ran: none ✓ |
| "cut a highlights montage from my gameplay footage" | none | none | ✓ | |
| "make an infographic from my stats" | infographic-builder | infographic-builder | ✓ | |
| "make a social graphic announcing my launch" | infographic-builder | infographic-builder | ✓ | |
| "visualize this architecture" | excalidraw-diagram-generator | excalidraw-diagram-generator | ✓ | |
| "draw a flowchart of my funnel" | excalidraw-diagram-generator | excalidraw-diagram-generator | ✓ | |
| "is there a community skill for video editing?" | skills-sh-finder | skills-sh-finder | ✓ | |
| "find me a pre-built skill for thumbnails" | skills-sh-finder | skills-sh-finder | ✓ | |
| "make my video better" (no context) | ambiguous → clarify | none/clarify | ✓ | correctly doesn't grab it blind |
| "I need to post this today, fix it up" (raw selfie video attached) | raw-to-reel | raw-to-reel | ✓ | context carries it |
| "turn my 10-min YouTube video into a short" | ambiguous → not this skill | none | ✓ | "repurposing finished long video" clause (added in fix) resolves it |
| "remove filler words from my voiceover audio file" | none | none | ✓ | audio-only, no video |

**Scores (post-fix):** precision 1.00 · recall 1.00 · F1 1.00 · misfires: none.
Self-repair applied? **yes** — one description rewrite (added interview/multi-speaker + finished-long-video-repurposing boundary), arena re-run clean.

## Golden-example replay
- `flubs-and-retakes.md` → **pass** — workflow P1–P7 produces every asserted property; keep-last-take is explicit in P2; script self-check covers the XML assertions (smoke-tested: 30000/1001 NTSC math correct, 690 frames = 23.02s).
- `cut-for-time-coherence.md` → **pass** — P4 ladder is fixed-order with core-message exclusion; P3 re-runs after P4, which is what catches the callback orphan; "shortest coherent cut over 60s + say so" path present.
- `hook-decision.md` → **pass** — P5 encodes both outcomes + mandatory report rationale; reorder-as-segment-order is real in the script (verified: segment 41.2s placed first, SRT re-timed to 0:00).
Total: **3/3**.

## Regression
n/a (create intent).

## Usefulness
Wedge expressed in the build, not just claimed: P2 (semantic mistake/retake rubric, keep-last-complete-take), P3 (coherence gate blocks generation), P4 (time ladder ordered by editorial weakness, not silence length), P5 (hook judgment with stated rationale) — none of which a one-line prompt or a mechanical cutter encodes. The load-bearing asset (`make_sequence.py`, 280 lines, stdlib-only) was executed against a synthetic cutlist during Build: XML self-check passed, captions re-timed across a reorder, Windows BOM tolerated, pathurl format corrected. Generic risk: none.

## Convention & completeness
- Frontmatter: `name: raw-to-reel` = slug ✓ · `version: 1.0.0` ✓ · description has 6 trigger phrases + explicit do-NOT boundary ✓.
- All blueprint sections present and concrete; no placeholders. Integrity rules and anti-patterns are skill-specific (float-29.97, hand-written XML, exactly-60s-over-coherence). Output format fully specified. Both scripts exist and are invoked by name in the workflow.

## Would-it-work dry run
3-min 4K NTSC clip → preflight (deps + rational fps via ffprobe) → transcribe.py (real API: faster_whisper WhisperModel, word_timestamps) → editorial pass on words.json → cutlist.json (schema matches script exactly — verified by execution) → make_sequence.py → sequence.xml + captions.srt + self-check → report. Gaps: none found. One environmental note: on this machine plain `python` is 3.9 (fine — no 3.10+ syntax used; `ET.indent` requires 3.9+, satisfied).

## Coverage Manifest: clean
All baseline + skill-specific items [x]; two struck with reason: `handoffs_to/expects_from` (standalone — nothing composes), none other. ≥2 golden examples: 3 present, 3 passing.

## VERDICT: PASS (after one logged self-repair: description boundary rewrite)
Recommend the install gate.

## Delta re-verify (final gate: user accepted B1 + C1)
- B1 preview render: new optional P8 + `render_preview.py` (compiles; trim/concat mirrors cutlist semantics incl. reorder; subtitles path escaped for Windows; explicit ffmpeg-missing error). Trigger surface unchanged → arena results stand. Anti-pattern updated so the preview can't masquerade as the deliverable.
- C1 post kit: report section 5, grounded-in-transcript rule + oversell anti-pattern. No trigger/asset impact.
- Golden example 1 extended with both assertions; replay still passes. **Delta verdict: PASS.**
