# Shape Decision: Raw to Reel

## Recommendation: STANDALONE
- **Join an existing pipeline?** No candidate. The only pipeline in the library is skill-forge itself (meta, unrelated). No video/content pipeline exists to slot into.
- **Spin out as its own pipeline?** No. The phases (preflight → transcribe → cut plan → coherence gate → generate XML/SRT/report) form one artifact chain in one sitting with no independent reuse seams worth a skill boundary: nobody invokes "coherence-gate a transcript" or "emit FCP7 XML" standalone — the XML emitter is properly a *script asset inside* this skill, not a sibling skill.
- **Standalone with heavy assets** is the right shape: one SKILL.md encoding the editorial judgment (prose, where judgment lives) + `scripts/` for the deterministic mechanics (probe, XML/SRT generation) + `references/` for the cut rubric and golden examples.

## Composition edges
- `handoffs_to:` none. `expects_from:` none. Struck from manifest with reason: nothing composes with it yet.
- Future seam (noted, not built): if A3 (more NLE targets) is ever accepted, the XML emitter script grows targets — still no new skill needed.

No `[!REFRAME]` raised.
