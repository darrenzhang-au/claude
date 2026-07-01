# Ideation: Business Model Architect  (`business-model-architect`)

## Status
Ran (proposed 3×4). Auto mode → all default-rejected; surfaced for opt-in at the final gate.

## Proposed menu

### Set A — Scope extensions
- **A1. Model-archetype library** — a reference file of ~10 named archetypes (marketplace/take-rate, usage-based, seat SaaS, freemium→enterprise, transactional, ads, licensing, services-productized, community/membership, hardware+consumable) with when-each-wins cues, so convergence is anchored to real patterns instead of improvised each time · cost: M · wedge: strengthens
- **A2. "Steelman my pick" handoff** — after converging, offer to pipe the recommended model into the existing `steelman` skill for a deeper adversarial pass · cost: S · wedge: strengthens
- **A3. Napkin unit-economics sanity check** — a lightweight order-of-magnitude margin/CAC-vs-LTV gut-check on the recommended model (NOT full financial modeling — stays on the right side of the exclusion) · cost: M · wedge: neutral
- **A4. Canvas export on request** — if the user explicitly asks, render the converged model as a Lean Canvas artifact as a *secondary* output, never the default · cost: S · wedge: risks-dilution

### Set B — Robustness & safety
- **B1. Existing-model detector + redirect** — an explicit up-front check ("does a revenue model already exist?") that hard-redirects to `business-model-enhancer` when yes; resolves the `[!COLLISION]` flag · cost: S · wedge: strengthens
- **B2. Assumption ledger** — every market fact the user didn't supply is written to a visible "Assumptions (unverified)" list, so nothing invented is ever presented as fact · cost: S · wedge: strengthens
- **B3. Regulated/constrained-market guard** — flag when the idea sits in a space where the model is constrained by law/platform rules (health, finance, kids, app-store take) before recommending a monetization shape · cost: M · wedge: neutral
- **B4. "Not enough to model" refusal path** — if intake answers are still too thin after one round, say what's missing rather than fabricating a model · cost: S · wedge: strengthens

### Set C — Delight & leverage
- **C1. Riskiest-assumption → cheapest-test map** — always end with a concrete, named validation experiment (landing page, 5 customer calls, pre-sale) sized to the riskiest assumption · cost: S · wedge: strengthens
- **C2. Ambition-preset defaults** — "bootstrapped" vs "venture" presets that pre-set the optimization target and pre-mortem lens, so the user picks one word and the whole analysis re-aims · cost: M · wedge: strengthens
- **C3. Analogous-company anchors** — name 1-2 real companies that run the recommended model, as concrete reference points (labeled as analogies, not proof) · cost: S · wedge: neutral
- **C4. "Why not the others" ledger** — briefly record why each rejected archetype lost, so the user can revisit if an assumption changes · cost: S · wedge: strengthens

## Verdicts
- Accepted: *(none — auto mode default-reject)*
- Rejected: A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C4
- Flagged stretch / low-value: A4 (risks-dilution — canvas export tempts the generic-wrapper failure mode)

## Note for the final gate
Several of these are arguably *core*, not extensions — in particular **B1 (existing-model redirect)**, **B2 (assumption ledger)**, and **C1 (riskiest-assumption→cheapest-test)** already fall out of the grill decisions and the quality bar, so Blueprint will fold them in as baseline behavior regardless of acceptance. The genuinely *optional* additions the user might opt into are: **A1** (archetype reference file), **A2** (steelman handoff), **A3** (napkin unit-economics), **C2** (ambition presets), **C3** (analogous-company anchors), **C4** (why-not ledger).

## Integrated additions (carried into Blueprint)
- None accepted in auto mode. (B1/B2/C1 enter as baseline via the grill quality bar, not as ideation additions.)

## Manifest additions
- None (no accepted ideas).
