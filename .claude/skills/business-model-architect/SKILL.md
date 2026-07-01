---
name: business-model-architect
version: 1.0.0
description: >
  Design the business model for a brand-new / zero-to-one idea from scratch — decide who pays, the
  monetization & pricing shape, the go-to-market motion, and the moat, then converge on ONE recommended
  model with the strongest runner-up, the riskiest assumption, and the cheapest way to validate it. Trigger
  when the user says "help me figure out the business model for my idea", "how would I make money from
  this?", "I have an idea for an app — what's the best way to monetize it?", "what's the right revenue model
  for this?", or "turn this idea into a viable business — how should it actually work?". Runs a tight intake
  first when the idea is thin; never invents a market. Do NOT use when a business/revenue model already
  exists and you want to add to or stress-test it (use `business-model-enhancer`), nor for financial
  modeling / projections, business-plan or pitch-deck writing, standalone market sizing, or building /
  naming the product.
---

# Business Model Architect

Turn a raw, early idea into one recommended, defensible business model — **decided, not just described**.
This skill does not hand you a filled canvas or a menu of options; it runs a disciplined
**diverge → pre-mortem → converge** process from a blank slate and ends in a single pick with its risks named.

## When to use

Fires when the user has a **new or early idea with no revenue model yet** and needs to work out how it
should actually make money. Both of these are in scope:

- "Help me figure out the business model for my idea."
- "How would I make money from this app idea?"
- "I have an idea for a [X] — what's the best way to monetize it?"
- "What's the right revenue model for my new thing?"
- "I've built an audience but earn $0 — how do I turn it into a business?"
- "Turn this idea into a viable business — how should it actually work?"

Do **NOT** use when:
- A **business/revenue model already exists** and the user wants to add to or stress-test it. The
  disambiguator is factual — *does a revenue model already exist yet?* If **yes → `business-model-enhancer`**.
- The ask is **financial modeling** — projections, unit-economics spreadsheets, cap tables, DCF.
- The ask is to **write a business plan or pitch deck** (document authoring).
- The ask is **standalone market sizing / TAM research**.
- The ask is to **build / implement** the product, or do **naming / branding / copy**.

## Workflow

### 1. Check the boundary first
Before anything else, establish: **does a revenue model already exist?** If the user already has a running
model and wants to add a tier / channel / feature, stop and redirect: *"You already have a working model —
that's a job for `business-model-enhancer`, which stress-tests additions to an existing model. I design one
from scratch."* Only continue if this is genuinely zero-to-one (no model yet, even if a product or audience
exists).

### 2. Anchor (tight intake)
You need five anchors before generating anything:
- **What it does** — the idea in one line.
- **Who the customer is** — and, critically, **who pays** (they're often different).
- **What problem** it solves, and how they solve it today.
- **Ambition** — bootstrapped/lifestyle (optimize for margin, low burn, speed to cash) **or** venture-scale
  (optimize for moat, TAM, defensibility). This single answer re-aims the whole analysis.
- **Rough cost driver** — the main thing that costs money to deliver.

Ask only the **missing** anchors, in one short batch (max ~5, never re-ask what was given). **Never generate
a model blind** — if you don't know who pays and at what ambition, you'll invent a market.

### 3. Diverge — generate distinct archetypes
Produce **2-3 genuinely distinct** candidate models for the idea, drawn from a real palette rather than
improvised: **marketplace / take-rate · usage-based · seat-based SaaS · freemium → enterprise ·
transactional · subscription / membership · advertising · licensing · productized services**. For each
candidate, sketch the six components: **who pays · value prop · pricing shape · GTM motion · cost drivers ·
moat / defensibility.** Make them meaningfully different bets, not three flavors of the same one.

### 4. Pre-mortem each
Assume each candidate has failed 18 months from now — name *why*. Steer the lens by ambition:
- **Bootstrapped** → margin, burn, speed-to-first-revenue, CAC vs. cash cycle, founder-sustainability.
- **Venture** → defensibility, TAM ceiling, winner-take-most dynamics, capital intensity.

Any market fact the user did **not** supply (willingness-to-pay, competitor behavior, conversion rates)
goes into an explicit **Assumptions (unverified)** ledger. Never present a guessed number as fact.

### 5. Converge — commit to one
Pick **exactly one** recommended model. State plainly **why it beats the alternatives you weighed**, and
name the **strongest runner-up and its tradeoff** (what it would take for the runner-up to win instead). Do
not stop at a menu; the whole point is a decision.

### 6. De-risk
End with the **single riskiest assumption** the recommended model rests on, and the **cheapest concrete
test** to invalidate it before real money goes in (a landing-page smoke test, 5-10 customer conversations, a
manual concierge pre-sale). Size the test to the assumption.

## Integrity rules

- **Always run the boundary check first.** An existing model → redirect to `business-model-enhancer`; don't design over it.
- **Never invent a market.** Intake before generation; label every unverified input in the Assumptions ledger; never state a guessed figure as fact.
- **Always converge to exactly one model.** No bare menu, no filled-canvas-without-a-pick. A layout is not a decision.
- **Always deliver the full decision:** recommended model + why-it-wins + runner-up & tradeoff + riskiest assumption + cheapest validation. Missing any of these is an incomplete output.
- **Steer by ambition, never one-size dogma.** Don't push venture-scale moat advice at a lifestyle business, or vice versa.
- **Stay out of the spreadsheet.** Sanity-check whether the economics *can* work at an order-of-magnitude level; do not produce financial projections — that's a different job.

## Output format

Deliver in chat (write a file only if the user asks):

```
RECOMMENDED MODEL: <archetype, one line>
  • Who pays: …              • Value prop: …
  • Monetization / pricing: …• GTM motion: …
  • Cost drivers: …          • Moat / defensibility: …

WHY THIS (beats the alternatives): …
RUNNER-UP: <model> — tradeoff: <why it lost / when it would win instead>
RISKIEST ASSUMPTION: <the one that most threatens the model>
CHEAPEST VALIDATION: <concrete test sized to that assumption>

ASSUMPTIONS (unverified): <bullets — anything the user didn't supply>
```

## Anti-patterns to avoid

- **The generic canvas dump.** Nine filled boxes with no pick. If it would fit any idea, it's filler — converge.
- **Hallucinating the market.** Inventing customers, willingness-to-pay, or competitors that weren't given, and stating them as fact. Intake, then label assumptions.
- **Stealing the enhancer's job.** Designing over an existing, working model instead of redirecting. Run the boundary check.
- **One-size ambition.** Moat-and-TAM sermons for a $5k/mo lifestyle business (or "just charge a subscription" for a venture bet).
- **False confidence.** Presenting the recommended model as certain, with no riskiest-assumption and no way to test it.
- **Three flavors of one bet.** "Diverging" into three near-identical subscription variants. Candidates must be genuinely different models.
