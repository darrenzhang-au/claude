# Blueprint: Business Model Architect (`business-model-architect`)

## Frontmatter
- name: `business-model-architect`
- version: `1.0.0`
- description (draft): >
  "Design the business model for a brand-new / zero-to-one idea from scratch — decide who pays, the
  monetization & pricing shape, the go-to-market motion, and the moat, then converge on ONE recommended
  model with the strongest runner-up, the riskiest assumption, and the cheapest way to validate it. Trigger
  when the user says 'help me figure out the business model for my idea', 'how would I make money from
  this?', 'I have an idea for an app — what's the best way to monetize it?', 'what's the right revenue model
  for this?', or 'turn this idea into a viable business — how should it actually work?'. Runs a tight intake
  first when the idea is thin; never invents a market. Do NOT use when a business/revenue model already
  exists and you want to add to or stress-test it (use `business-model-enhancer`), nor for financial
  modeling/projections, business-plan or pitch-deck writing, standalone market sizing, or building/naming
  the product."
- handoffs_to / expects_from: **none** (boundary cross-reference to `business-model-enhancer`, not a data handoff → manifest handoff item struck with this reason)

## Section plan
- **# Business Model Architect** — purpose: "Turn a raw, early idea into one recommended, defensible business model — decided, not just described."
- **## When to use** — 5-6 natural fire phrases (from grill/brief); explicit "does NOT fire" list with the factual disambiguator *"does a revenue model already exist yet?"* (No → here; Yes → enhancer) plus the financial-modeling / plan-writing / market-research / build exclusions.
- **## Workflow** — numbered phases:
  1. **Check the boundary.** Does a revenue model already exist? If yes → stop and redirect to `business-model-enhancer`. (B1)
  2. **Anchor (tight intake).** Confirm the 4 anchors — what it does · who the customer is · what problem · **ambition (bootstrapped vs venture)** + rough cost driver. Ask only the missing ones (max ~5, one batch). Never generate blind. (D2)
  3. **Diverge.** Generate 2-3 *distinct* candidate model archetypes for the idea, drawn from a named palette (marketplace/take-rate · usage-based · seat SaaS · freemium→enterprise · transactional · subscription/membership · ads · licensing · services-productized). Each spans: who pays · value prop · pricing shape · GTM motion · cost drivers · moat.
  4. **Pre-mortem each.** Assume each has failed in 18 months; name why. Lens is steered by ambition (bootstrapped → margin/burn/speed-to-cash/CAC; venture → moat/TAM/defensibility). Write unverified inputs to an **Assumptions (unverified)** ledger. (B2)
  5. **Converge.** Commit to ONE recommended model; explain why it beats the alternatives it was weighed against; name the strongest runner-up + its tradeoff.
  6. **De-risk.** Surface the single riskiest assumption and the cheapest concrete test to invalidate it before committing money. (C1)
- **## Integrity rules** — the non-negotiables: always run the boundary check first; never present an unverified market fact as truth (label it); always converge to exactly one pick (never stop at a menu or a bare canvas); always give runner-up + riskiest-assumption + cheapest-test; steer by ambition, never apply one-size dogma; stay out of spreadsheet-grade financial modeling.
- **## Output format** — inline chat template (below), not a file unless asked.
- **## Anti-patterns to avoid** — 6 named failure modes.

## Assets
- **scripts/**: none (pure reasoning skill; no deterministic logic to execute).
- **references/**: none as a separate lookup file — the archetype palette is short enough to inline in the Workflow (ideation A1's standalone reference file was NOT accepted; inlining keeps it load-bearing without asset debt).
- **references/examples/**: **3 golden examples** (from grill.md):
  1. `dog-walker-app.md` — Input: "app for dog walkers" (thin, no ambition). Assert: runs intake first (payer/problem/ambition) instead of generating blind; converges on ONE model with why; names runner-up + tradeoff; flags riskiest assumption (walkers vs owners as payer); ends with a cheap validation; no invented stats stated as fact.
  2. `newsletter-monetization.md` — Input: "newsletter, 5k subs, $0, how do I make money?" (audience but NO model → in-scope). Assert: recognizes it's Architect (not Enhancer) territory; one converged monetization model matched to ambition; runner-up + riskiest assumption + cheapest test.
  3. `existing-saas-boundary.md` — Input: "$30k/mo seat-based SaaS, should I add usage-based?" (existing working model). Assert: declines and redirects to `business-model-enhancer` (the `[!COLLISION]` guard); does NOT design a model.

## Output format (template Build will author)
```
RECOMMENDED MODEL: <name of archetype, one line>
  • Who pays: …            • Value prop: …
  • Monetization/pricing: …• GTM motion: …
  • Cost drivers: …        • Moat/defensibility: …

WHY THIS (beats the alternatives): …
RUNNER-UP: <model> — tradeoff: <why it lost / when it'd win instead>
RISKIEST ASSUMPTION: <the one that most threatens the model>
CHEAPEST VALIDATION: <concrete test sized to that assumption>

ASSUMPTIONS (unverified): <bulleted — anything not supplied by the user>
```

## Trigger Arena expectation (for Verify)
- **should-fire phrasings:** "help me figure out the business model for my idea"; "how would I make money from this app idea?"; "what's the right revenue model for my new thing?"; "I've got an audience but no revenue — how do I monetize?"; "turn this idea into a viable business."
- **should-NOT-fire (boundary):** "should I add a usage-based tier to my existing SaaS?" (→ enhancer); "build me a revenue projection spreadsheet" (→ financial modeling); "write my pitch deck" (→ authoring); "how big is the market for X?" (→ research).
- **nearest neighbor the boundary must beat:** `business-model-enhancer` (overlap 62/100) — the disambiguator is "does a model already exist?"

## Manifest → section map
- name matches slug → frontmatter
- version set → frontmatter (1.0.0)
- sharp description + ≥3 phrases + boundary → description (draft above)
- cleared novelty → done (novelty.md)
- structure decision → shape.md (standalone)
- when-to-use → ## When to use
- concrete workflow → ## Workflow (6 phases)
- integrity rules → ## Integrity rules
- output format → ## Output format (template)
- anti-patterns → ## Anti-patterns to avoid
- ≥2 golden examples → references/examples/ (3 planned)
- assets if needed → struck: none load-bearing (archetypes inlined)
- handoffs declared if composes → struck: boundary cross-reference, not a data handoff
- boundary vs enhancer → description + Workflow step 1 (redirect)
- "perfect" trap resolved → converge-to-one (Workflow 5) + integrity rule
- names BM components → Workflow step 3 (who-pays/value/pricing/GTM/cost/moat)
- handles thin input → Workflow step 2 (tight intake)
- distinct from financial modeling / plan authoring → exclusions in description + When-to-use + integrity rule
- passed verify → forge-6
