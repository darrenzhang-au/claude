# Shape: Business Model Enhancer  (`business-model-enhancer`)

## Status
Ran.

## Scope sizing
Distinct sub-goals: **1** coherent job (anchor → diverge-by-lens → per-candidate pre-mortem → converge to
one recommendation). Outputs: **1** decision artifact. The 7 accepted Ideate additions (flip-assumptions,
first-test, anchor-integrity, zero-to-one guard, lens-N/A, scored table, devil's-advocate) are all *steps
within* that single job — they enrich it, they don't split it into independent phases. Verdict lean: **A**.

## Library fit
Nearest pipelines: only the Skill Forge meta-pipeline exists (`skill-forge` + forge stages) — it sequences
*skill authoring*, an unrelated domain. There is **no business-strategy orchestrator** to join. Fit: **none**.

## Recommendation: STANDALONE
This is a focused single-output generator. Applying the pipeline test for C: it does NOT have ≥3
independently-triggerable stages, the sub-steps are not independently useful outside the run, and one
`SKILL.md` can carry the workflow cleanly (the lens set lives in a `references/` file, not separate skills).
A pipeline here would be pure overhead and would over-fragment one coherent decision process. There is also
no host pipeline for a B (join) verdict. Ship it standalone; it can always grow later via the revise path.

### Plan
- (A) standalone — no library wiring. Ships with one `references/` asset (the strategic lens set). No
  `handoffs_to`/`expects_from`.

## Decision: STANDALONE (no [!REFRAME])
