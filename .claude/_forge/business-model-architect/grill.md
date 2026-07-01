# Refined Brief: Business Model Architect

## Resolved in grilling
- **Output shape** → **Converge to ONE.** Generate 2-3 distinct model archetypes internally, pre-mortem each, then commit to ONE recommended model with the runner-up + its tradeoff, the riskiest assumption, and the cheapest validation. It ends in a decision, not a menu or a canvas. *(user-chosen)*
- **Thin input** → **Tight intake first.** If the anchors are missing, ask a short batch (max ~5, only the gaps) before generating. Never invent a market. *(user-chosen)*
- **Ambition axis** → **Ask ambition, then steer.** Ambition is a first-class intake dimension: bootstrapped/lifestyle → optimize margin, speed-to-cash, low burn; venture-scale → optimize moat, TAM, defensibility. The model AND the pre-mortem lens adapt to it. *(default — recommended option, auto mode; flippable at final gate)*
- **Boundary vs `business-model-enhancer`** → **Redirect on existing model.** If the user already has a running business model and wants to add/stress-test, the skill declines and points to `business-model-enhancer`. The disambiguator is factual: *does a revenue model already exist?* *(design rule)*
- **Output medium** → chat-based structured reasoning by default; write a file only if the user asks. *(assumption carried from brief)*

## Exclusions (explicitly out of scope)
- Enhancing / stress-testing an **existing** business model → `business-model-enhancer`.
- **Financial modeling** — projections, unit-economics spreadsheets, cap tables, DCF. (It sanity-checks whether the economics *can* work; it does not build the numbers.)
- **Business-plan / pitch-deck authoring** — no document ghost-writing.
- **Market sizing / TAM research** as a standalone deliverable (it reasons about market shape from what the user provides; it does not run external market research).
- **Building/implementing** the product; **naming / branding / copywriting**.
- Validating a model the user has already committed to (that's testing, not designing).

## Failure modes & guards
- **Failure: hallucinating a market** (inventing customers, willingness-to-pay, competitors that weren't given). → **Guard:** tight intake first; label every unverified assumption explicitly; never present a guessed number as fact.
- **Failure: generic canvas dump** (nine filled boxes, no decision — the `[!GENERIC]` risk). → **Guard:** the output contract forbids stopping at a layout; it MUST converge to one recommended model with a *why*.
- **Failure: stealing the enhancer's prompts** (gray-zone "what revenue model should I use?" when a business already exists). → **Guard:** the "does a model already exist?" check up front; redirect when yes.
- **Failure: one-size ambition** (pushing venture-scale moat advice at someone building a $5k/mo lifestyle business). → **Guard:** ambition is an intake dimension that steers the optimization target and the pre-mortem lens.
- **Failure: false confidence** (presenting the recommended model as certain). → **Guard:** always name the riskiest assumption and the cheapest way to invalidate it before committing money.

## Quality bar
- **A great output:** anchors on the user's actual idea/customer/ambition; presents ONE clearly-recommended model across its real components (who pays · value prop · monetization & pricing shape · GTM motion · cost drivers · moat/defensibility); explains *why this beats the alternatives it considered*; names the strongest runner-up and its tradeoff; surfaces the single riskiest assumption; and gives the cheapest concrete test to de-risk it before committing. Assumptions are labeled, not smuggled.
- **A bad output:** a filled canvas with no pick; generic advice that would fit any idea; invented market facts stated as truth; venture-scale dogma applied to a lifestyle business (or vice versa); no runner-up, no riskiest-assumption, no validation step; or silently accepting an idea that already has a model (should have redirected).

## Golden scenarios (seed Build's examples + Verify's replay)
1. **Input:** "I want to build an app for dog walkers." (thin, no ambition stated) → **A great output asserts:** it runs a tight intake first (who pays, problem, ambition) rather than generating blind; then converges on ONE model (e.g., take-rate marketplace vs. subscription for walkers) with a clear pick + why; names a runner-up + tradeoff; flags the riskiest assumption (e.g., "walkers won't pay a SaaS fee — owners must be the payer"); ends with a cheap validation. No invented market stats presented as fact.
2. **Input:** "I've got a newsletter with 5k subscribers making $0 — what's the best way to make money from it?" (idea exists, but NO model yet — this is in-scope zero-to-one) → **A great output asserts:** it recognizes there's an audience but no revenue model, so it's Architect territory (not Enhancer); converges on one monetization model (e.g., paid tier vs sponsorship vs product) matched to the ambition; runner-up + riskiest assumption + cheapest test.
3. **Input (boundary/negative):** "I run a $30k/mo SaaS on seat-based pricing — should I add a usage-based tier?" (existing, working model) → **A great output asserts:** it declines and redirects to `business-model-enhancer`, because a model already exists and the ask is an enhancement, not a design-from-scratch. (This is the `[!COLLISION]` guard.)

## Updated triggers / I/O / wedge
- **Triggers unchanged** from brief §3, with the boundary sharpened: fires on new/early idea with **no revenue model yet**; does NOT fire when a model exists (→ Enhancer).
- **Inputs:** idea + customer + problem + **ambition** (bootstrapped vs venture) — intake fills gaps.
- **Output:** chat-based, decision-shaped (one recommended model + runner-up + riskiest assumption + cheapest validation). File only on request.
- **Wedge:** unchanged from novelty (zero-to-one design vs existing-model enhancement).

## Deferred (user chose not to decide now)
- None. Ambition question was auto-defaulted (recommended option) under auto mode; flippable at the final gate.
