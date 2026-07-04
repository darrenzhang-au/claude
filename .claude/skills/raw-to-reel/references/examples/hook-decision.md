# Golden Example 3 — The hook decision (both directions must be possible)

## Input
The strongest line ("nobody tells you this about hiring…") sits at 0:40. The opening 8s is throat-clearing
("hey guys, so, um, today I want to talk about something…").

## A great output asserts
- [ ] One of two valid outcomes, chosen deliberately:
  - the 0:40 line is moved to the front (`hook` reorder) AND the seam survives the coherence gate — no dangling connective at the join, no tense break; or
  - the throat-clearing is cut so the natural strong line opens within ~2s of speech, order unchanged.
- [ ] The report states which was chosen and why (this is the judgment call — silence here is a failure).
- [ ] If reordered: `segments` order in `cutlist.json` reflects the new order and the SRT cues follow sequence time, so captions still sync.
- [ ] If the user had said "keep it chronological", no reorder is attempted regardless of hook strength.

## A bad output
Reorders because it can, leaving "…so that's why" as the video's first words; or leaves 8s of preamble because reordering felt risky and cutting wasn't considered.
