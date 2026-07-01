# Skill Brief: Business Model Enhancer  (`business-model-enhancer`)

## §0 Coverage Manifest
- [ ] `name` matches folder slug (kebab-case)
- [ ] `version:` set in frontmatter (semver)
- [ ] Sharp `description` with ≥3 trigger phrases + a "do NOT use when" boundary
- [ ] Cleared the novelty gate (wedge stated; nearest neighbors + overlap scores)
- [ ] Structure decision recorded (standalone / join / new-pipeline) [Full only]
- [ ] "When to use" section
- [ ] Concrete workflow steps (the diverge → stress-test → converge loop, not abstract)
- [ ] Integrity rules / non-negotiables
- [ ] Output format defined
- [ ] Anti-patterns section
- [ ] ≥2 golden examples present and passing
- [ ] Assets present if needed (else struck with reason)
- [ ] `handoffs_to:`/`expects_from:` declared if it composes (else struck)
- [ ] Passed forge-6-verify
<!-- skill-specific -->
- [ ] Defines the divergence engine — HOW it generates *different* suggestions, not one obvious one
- [ ] Every suggestion paired with concrete issues/risks (no unpaired ideas)
- [ ] Convergence rule defined — how it picks/synthesizes the single "perfect solution"
- [ ] Anchors to the *existing* model's constraints (customers, revenue mechanics, moat) — not generic advice
- [ ] Decide: does it require the business model as input, or elicit it? (prompt-for-context behavior)

## 1. Purpose
This skill takes an existing business model plus a proposed enhancement, **diverges** into a spread of
distinct suggestions, **stress-tests** each for issues and risks, then **converges** on a single
recommended "best-fit" solution — so the user can decide whether and how to add the enhancement.

## 2. Profile
- Category: **generator** (with a built-in reviewer/critic phase)
- Invoked by: **user, on demand**
- Complexity: **medium** (multi-phase reasoning, branching, judgment — not a single transform)
- External deps: none required. *(Open: optional web research for market/competitor validation.)*

## 3. Triggers
**Fires when:** the user has an *existing* business/product and wants to explore adding something to it —
a feature, revenue stream, segment, channel, pricing change — and wants both ideas AND the holes poked in
them, ending in a recommended direction.

**Does NOT fire when:**
- There's no existing model yet — building a business/idea from a blank slate (that's zero-to-one, not
  enhance-an-existing-thing).
- Pure financial modeling / spreadsheet math / unit-economics computation.
- "Write my business plan / pitch deck" (document authoring, not idea stress-testing).
- Generic, non-business brainstorming (naming, creative writing, product copy).
- A concrete engineering/build task ("implement the feature").

**Natural phrases:**
- "Help me improve my business model — what could I add?"
- "I want to add [X] to my product. Is it a good idea, and what could go wrong?"
- "Brainstorm enhancements to my subscription and tell me the risks of each."
- "Stress-test this new feature idea for my business and give me the ideal version."
- "What's the best way to add a new revenue stream to my existing model?"
- "Poke holes in this idea and tell me what the perfect version looks like."

## 4. Inputs → Output
- **Inputs:** a description of the existing business model (what it sells, to whom, how it makes money) and
  either a specific proposed enhancement OR a request to generate candidate enhancements. If the model
  isn't supplied, the skill should elicit the minimum it needs before diverging *(assumption — confirm)*.
- **Output:** a structured markdown artifact (chat by default; offer a file) with three parts —
  (1) a spread of distinct **suggestions/variations**, (2) **issues & risks** paired to each,
  (3) a converged **recommended "perfect solution"** with the reasoning for the pick.

## 5. Unique wedge (draft — to be tested in stage 2)
Unlike a plain "brainstorm ideas" prompt or a generic strategy chat, this skill runs a disciplined
**diverge → stress-test → converge** loop *anchored to an existing model's constraints*, pairing every
suggestion with its failure modes and ending in **one defensible recommended solution** rather than a flat
idea list.

## 6. Open questions / assumptions
- **Generate vs evaluate:** does the user usually bring one idea to stress-test, or want ideas generated
  from scratch? The raw idea implies *both* — needs a clear branch. (grill)
- **"Perfect solution" = one pick or a ranked shortlist?** "Product would be the perfect solution" reads as
  a single synthesized recommendation, but a top-3 may be more honest. (grill)
- **Context intake:** require the business model up front, or elicit it interactively? (grill)
- **Research depth:** pure reasoning, or optional web validation of market/competitors? (ideate)
- **Frameworks:** lean on named lenses (Jobs-to-be-Done, Business Model Canvas, SWOT, pre-mortem) or stay
  framework-light? (ideate)
- **Divergence quality:** biggest failure risk is suggestions that are near-duplicates or generic — the
  skill needs a real mechanism to force genuinely *different* angles. (grill + blueprint)
