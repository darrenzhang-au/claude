# Skill Brief: Business Model Architect  (`business-model-architect`)

## §0 Coverage Manifest
- [ ] `name` matches folder slug (kebab-case)
- [ ] `version:` set in frontmatter (semver)
- [ ] Sharp `description` with ≥3 natural trigger phrases + a "do NOT use when" boundary
- [ ] Cleared the novelty gate (wedge stated; nearest neighbors + overlap scores listed)
- [ ] Structure decision recorded (standalone / join / new-pipeline)
- [ ] "When to use" section
- [ ] Concrete workflow steps (not abstract)
- [ ] Integrity rules / non-negotiables
- [ ] Output format defined
- [ ] Anti-patterns section
- [ ] ≥2 golden examples present and passing
- [ ] Assets present if needed (else struck with reason)
- [ ] `handoffs_to:`/`expects_from:` declared if it composes (else struck)
- [ ] Passed forge-6-verify

**Skill-specific items:**
- [ ] Draws a **hard boundary vs `business-model-enhancer`** (new/zero-to-one model design vs enhancing an existing one) — stated in the description AND enforced with a redirect
- [ ] Resolves the **"perfect" trap** — defines what "perfect/right" means operationally (a decision under constraints, not a fantasy) and whether it converges on ONE model or presents ranked candidate archetypes
- [ ] Names the **components of a business model** it actually reasons about (who pays, value prop, monetization/pricing structure, GTM motion, cost drivers, moat/defensibility, unit-economics sanity check) — so it isn't a generic "fill the canvas" wrapper
- [ ] Handles **thin input** — a one-line idea — with a tight intake before generating (does not hallucinate a market)
- [ ] Distinguishes itself from **financial modeling** (no projections/spreadsheets) and **business-plan/pitch-deck authoring** (no document ghost-writing)

## 1. Purpose
This skill designs a viable, defensible **business model for a brand-new idea from scratch** — deciding how it makes money, who pays, and why it wins — so the user leaves with one recommended model (plus the strongest alternative) rather than a blank canvas.

## 2. Profile
- Category: generator (with an evaluative/convergence core)
- Invoked by: user on demand
- Complexity: complex (branching, judgment, multi-component reasoning)
- External deps: none

## 3. Triggers
**Fires when:** the user has a **new/early idea** (product, service, concept, or a "I want to start X") and needs to work out how to turn it into a money-making, defensible business — the monetization structure, who pays, pricing shape, go-to-market, and the moat.

**Does NOT fire when:**
- There's already an **existing business model** and the user wants to add to / stress-test it → that's `business-model-enhancer`.
- The ask is **financial modeling** — projections, unit-economics spreadsheets, cap tables.
- The ask is to **write a business plan or pitch deck** (document authoring).
- The ask is **market research** only ("how big is the TAM for X").
- The ask is to **build/implement** the product, or to do **naming/branding/copy**.

**Natural phrases:** "help me figure out the business model for my idea", "how would I make money from this?", "I have an idea for an app — what's the best way to monetize it?", "design a business model for a [X] startup", "what's the right revenue model for this?", "turn this idea into a viable business — how should it actually work?"

## 4. Inputs → Output
- **Inputs (required to anchor):** the core idea/what it does, the intended customer/user, and the problem it solves. If missing → tight intake (a few questions, only the gaps) before generating.
- **Output:** a structured recommendation delivered in chat (not a file, unless asked): the recommended business model across its key components, *why* this one, the strongest runner-up and its tradeoff, the riskiest assumption, and the cheapest way to validate it before committing.

## 5. Unique wedge (draft — to be tested in stage 2)
It builds a business model **from a blank slate** for a new idea (who-pays / monetization / GTM / moat), whereas the only neighbor, `business-model-enhancer`, requires an *existing* model and only enhances/stress-tests additions to it.

## 6. Open questions / assumptions
- **The "perfect" question (biggest one for Grill):** does it converge on ONE recommended model, or present 2-3 candidate *model archetypes* (e.g. subscription vs marketplace vs freemium-to-enterprise) with tradeoffs and then a pick? Leaning: present ranked candidates → converge on one, mirroring the enhancer's diverge→converge discipline but starting from zero.
- **Overlap-of-engine risk:** the enhancer already uses a diverge→pre-mortem→converge engine. This skill should share that *rigor* but must stay clearly separated by its zero-to-one starting point — Grill/Shape to confirm it's a standalone skill, not a second branch of the enhancer. (Raise `[!OVERLAP]` for Novelty/Shape.)
- **Assumption:** output is chat-based structured reasoning, not a filled Business Model Canvas file — unless the user asks for the canvas. To confirm in Grill.
- **Assumption:** single-shot generative reasoning, no external market-data lookups (no web scraping / TAM databases).

**Annotations for downstream:** `[!OVERLAP]` — shares the diverge→converge engine and the "business model" domain with `business-model-enhancer`; boundary is new-vs-existing model. Novelty must score this and Shape must confirm standalone.
