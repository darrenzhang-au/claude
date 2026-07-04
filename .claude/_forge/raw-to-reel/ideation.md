# Ideation Menu: Raw to Reel

Auto mode: all 12 proposals **default-rejected** — none are built unless accepted at the final gate.
Starred (☆) = strongest opt-in candidates in my judgment.

## Set A — Scope extensions
- **A1. Multi-file input.** Accept a folder of takes/clips, treat them as one candidate pool, assemble the best material into the single reel. (Brief currently assumes one file per run.)
- **A2. Platform presets.** `--platform tiktok|reels|shorts` adjusts the duration cap (60/90s), notes title-safe zones for captions in the report.
- **A3. More NLE targets.** Same cut list → FCPXML (Final Cut) or EDL (Resolve) alongside the Premiere XML.
- **A4. A/B cuts.** Deliver two sequences in one XML — hook-reordered vs chronological — so you pick in Premiere.

## Set B — Robustness & safety
- **B1. ☆ Phone preview render.** Optional low-res ffmpeg render of the edited cut (burned-in captions) so you can gut-check pacing on your phone before opening Premiere.
- **B2. ☆ Confidence-flagged cuts.** Every cut in the report carries a confidence marker; low-confidence cuts get a ⚠ and a one-line "check this seam" note — extends the existing garbled-span guard to all editorial calls.
- **B3. Restore appendix.** The report ends with an appendix of every removed segment (source timecodes + first words) so re-adding one in Premiere is a lookup, not a hunt.
- **B4. Dry-run mode.** "Show me the cut plan first": kept transcript + cut table only, generate XML/SRT after approval.

## Set C — Delight & leverage
- **C1. ☆ Post kit.** Auto-draft the social caption, 3 title options, and hashtags from the kept transcript, appended to the report.
- **C2. Hook overlay suggestions.** 3 text-overlay lines for the opening 2 seconds (you add them in Premiere).
- **C3. Retention notes.** Pacing observations — where a viewer might swipe away, which sentence could be tightened further by hand.
- **C4. Batch mode.** Point at a folder of raw clips → one reel per clip, one summary report.

## Verdicts (auto mode)
| Idea | Verdict | Note |
|------|---------|------|
| A1–A4 | rejected (default) | scope growth; v1 stays one-clip, one-Premiere-XML |
| B1 | **ACCEPTED at final gate** | integrated as optional P8 + render_preview.py |
| B2 | rejected (default) | ☆ near-free extension of an existing guard |
| B3 | rejected (default) | useful, report grows |
| B4 | rejected (default) | conflicts with hands-off flow unless asked for |
| C1 | **ACCEPTED at final gate** | integrated as report Post kit section |
| C2–C4 | rejected (default) | nice-to-have; dilute v1 focus |

Nothing above is integrated into the blueprint. Accepting any at the final gate re-enters at Blueprint.
