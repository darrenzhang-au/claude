# Shape: Business Model Architect  (`business-model-architect`)

## Status
Ran.

## Scope sizing
Distinct sub-goals: 1 coherent job — anchor (intake) → diverge into archetypes → pre-mortem → converge on one recommended model. Outputs: 1 (a decision-shaped recommendation in chat). Verdict lean: **A**.

The internal steps (intake / diverge / pre-mortem / converge) are *phases of one reasoning pass with one output*, not independently-triggerable or independently-useful skills. They fail the pipeline test: no stage is separately invoked, and a single `SKILL.md` follows the flow cleanly.

## Library fit
Nearest pipelines: none relevant. `skill-forge` and `full-listing` are the only orchestrators in the library; neither sequences business-strategy work. `business-model-enhancer` is a **standalone** skill (not a pipeline/orchestrator), so there is no host pipeline to join.

Could it JOIN `business-model-enhancer` as a second branch? **No.** The enhancer explicitly excludes zero-to-one in its own description and is built around an *existing-model* intake; bolting a blank-slate branch onto it would (a) blur the very boundary Novelty relied on to clear this skill, (b) bloat one SKILL.md with two opposite intake paths, and (c) make each independently un-revisable. They are better as two sharp, adjacent standalone skills that reference each other.

Could it spawn a NEW `business-model` pipeline (architect + enhancer + …)? **No** — that's over-engineering two standalone skills into an orchestrator that adds routing overhead for zero real sequencing. If a third and fourth business-strategy skill ever appear, revisit via the revise path.

## Recommendation: STANDALONE
One coherent job, one output, no host pipeline, and a deliberate decision to keep it as a sharp sibling of `business-model-enhancer` rather than a branch inside it. This preserves the clean factual boundary (no model yet → Architect; model exists → Enhancer) that both skills' descriptions will point at, and keeps each independently revisable.

### Plan
- (A) **Standalone** — no pipeline wiring. One soft cross-reference only: the description and a redirect rule name `business-model-enhancer` as the sibling for the "model already exists" case (and the enhancer already names zero-to-one as out of scope, so the boundary is mutually declared). No `handoffs_to`/`expects_from` frontmatter needed — this is a boundary cross-reference, not a data handoff, so the manifest's handoff item will be struck with that reason.

## Decision: STANDALONE (no [!REFRAME])
