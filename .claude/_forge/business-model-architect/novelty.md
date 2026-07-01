# Novelty Check: Business Model Architect

## Nearest neighbors (from library model — LLM-judged)
1. `business-model-enhancer` — runs diverge→pre-mortem→converge on additions to an **existing** business model; stops hard at zero-to-one (explicitly excludes blank-slate creation). Overlap: **62/100**. Neighbor-shift risk: **yes** — gray-zone prompts like "what's the best revenue model for this?" could fire either skill depending on whether a business already exists. → `[!COLLISION]` for the Trigger Arena.
2. `expand-and-contract` — sorts a fuzzy idea into scope buckets (Core/Nice/Later/Out). Adjacent (idea-shaping) but not about monetization/model structure. Overlap: **24/100**.
3. `steelman` — stress-tests a position by finding the strongest counter-arguments. Shares "poke holes" DNA with the pre-mortem step but is domain-agnostic and produces no model. Overlap: **14/100**.
4. `business-model-enhancer`'s pre-mortem engine (as a pattern) — a *method* overlap, not a trigger overlap.

maxScore: **62/100** → DIFFERENTIATE band (60–85).

## Ecosystem prior art
- **Business Model Canvas / Lean Canvas** — the standard 9-block / 1-page frameworks for laying out a model. Ubiquitous; a bare "fill in the canvas" prompt is a generic wrapper. (fact)
- **"AI for zero-to-one" stage-gating** (Discovery→Exploration→Viability, unit economics defined at Viability) — a known framework structure. [link](https://www.fishmanafnewsletter.com/p/a-stage-gating-process-for-new-products-how-to-build-zero-to-one-with-ai) (fact)
- **AI-startup monetization guides** (usage-based, value-metric, workflow, data-centric models) — plentiful article content, not a packaged decision process. [link](https://adcel.org/en/content/ai-startup-business-models-monetization-strategy-guide) (fact)
- **Assessment:** prior art is *reference material and canvases*, not a disciplined generate-candidates → pre-mortem → converge-to-one-recommended-model process that starts from a raw idea. A competent person would reach for a canvas + ad-hoc thinking; they would NOT have a repeatable convergence engine. The wedge is the **process + convergence to a decision**, not the vocabulary of business models. (judgment)

## Wedge test
Wedge: "Unlike `business-model-enhancer`, which requires an existing model and only stress-tests additions to it, Business Model Architect designs the model for a brand-new idea from a blank slate — picking the who-pays / monetization structure / GTM motion / moat and converging on one recommended model — which matters because the highest-leverage, hardest-to-reverse modeling decisions happen *before* any model exists, exactly where the enhancer refuses to operate."

- **Real difference vs reskin?** Real. Opposite starting state (no model vs existing model). The enhancer literally declines this input.
- **Could a one-line prompt do it?** No — a prompt yields a generic canvas. The value is the encoded process: anchor from thin input → generate distinct *model archetypes* → pre-mortem each → converge on one with runner-up + riskiest assumption + cheapest validation. That's non-obvious structure, not a sentence.
- **Durable?** Yes. The boundary is a factual state (does a business/model already exist?), not a stylistic preference the enhancer could erase by adding a trigger phrase.

## Verdict: DIFFERENTIATE
A defensible wedge survives, but the domain overlap and gray-zone triggers with `business-model-enhancer` are real, so this proceeds as DIFFERENTIATE, not a clean PROCEED.

**Boundary the description MUST draw (both directions):**
- Architect fires when **no business model exists yet** — a new/early idea needing its model designed.
- Enhancer fires when a **model already exists** and the user wants to add to / stress-test it.
- The disambiguating question is factual: *"Does a business/revenue model already exist?"* No → Architect. Yes → Enhancer. The two skills should reference each other's boundary so neither steals the other's prompts.

Blockers raised: `[!OVERLAP]` (boundary stated above), `[!COLLISION]` (gray-zone monetization prompts — Verify's Trigger Arena must confirm the boundary holds). No `[!DUPLICATE]`, no `[!GENERIC]`.
