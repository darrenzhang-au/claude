---
name: business-model-enhancer
version: 1.0.0
description: >
  Stress-test and enhance an EXISTING business model. Generates distinct candidate improvements (one per
  strategic lens), runs an independent pre-mortem on each, and converges on a single recommended solution
  with the runner-up tradeoff, a "what would change my mind" line, and the cheapest way to validate it.
  Trigger when the user says "help me improve my business model", "I want to add X to my product — is it a
  good idea and what could go wrong", "brainstorm enhancements to my subscription and stress-test them",
  "what new revenue stream should I add", or "poke holes in this idea and tell me the perfect version". Runs
  a short intake first if the model isn't described. Do NOT use for zero-to-one / blank-slate business
  creation, financial modeling or projections, business-plan / pitch-deck writing, or implementing the
  chosen change.
---

# Business Model Enhancer

Turn a proposed enhancement — or a growth goal — for an **existing** business model into one anchored,
stress-tested, recommended solution. This skill does not hand you a flat idea list; it runs a disciplined
**diverge → pre-mortem → converge** process and ends in a decision.

## When to use

Fires when the user has an existing business/product and wants to explore adding something to it, with the
holes poked in each option and a recommended direction. Both branches are in scope:

- "Help me improve my business model — what could I add?" *(generate)*
- "I want to add [feature/tier/channel] to my product. Good idea? What could go wrong?" *(evaluate)*
- "Brainstorm enhancements to my subscription and stress-test each one."
- "What's the best new revenue stream to add to my existing model?"
- "Poke holes in this idea and tell me what the perfect version looks like."

Do **NOT** use when:
- There is no business yet — blank-slate / zero-to-one idea generation. (Decline and redirect; see Workflow 1.)
- The ask is **financial modeling** — projections, unit-economics math, spreadsheets.
- The ask is to **write a business plan or pitch deck** (document authoring).
- It's **generic non-business brainstorming** (names, taglines, creative copy).
- The ask is to **implement/build** the chosen enhancement.

## Workflow

### 1. Detect branch & intake
Decide which branch the user is on:
- **Evaluate** — they named a specific enhancement → you will diverge it into distinct *variants*.
- **Generate** — they gave only a goal/problem → you will generate candidates from scratch.

Then check you have enough to anchor. You need: **what they sell · who the customer is · how they make
money · the main cost driver · the current goal.** If any are missing, ask a **tight intake** (max 5
questions, only the missing ones — never re-ask what they already told you) before generating anything.

**Zero-to-one guard:** if there is no existing business ("I have an idea for a startup", "I want to start a
company"), do not fake an enhancement. Say plainly this skill enhances an existing model, and offer to
proceed once they describe even a running pilot, or redirect them to plain brainstorming.

### 2. Anchor
Write a compact **Model snapshot**: customers · revenue mechanics · cost structure · moat/advantage · goal.
Every candidate and every risk downstream must tie back to this snapshot. This is the anchor that keeps the
output specific to *their* business instead of generic advice.

### 3. Diverge by lens
Open `references/strategic-lenses.md`. Generate **one candidate per lens**:
New pricing/packaging · New segment · New channel/distribution · Product/feature depth · Partnership/
ecosystem · Business-model shift.
- On the **evaluate** branch, express the user's idea through each lens to produce genuinely different
  variants (e.g. their "AI feature" as: a premium tier vs. a new-segment wedge vs. a partnership play).
- If a lens genuinely does not fit this model, mark it **N/A — <reason>** rather than forcing a weak
  candidate. Never pad to hit six.

### 4. Anchor-integrity check
Re-read each candidate against the Model snapshot. If any reads like advice you could give *any* business
("add a subscription tier", "do more marketing"), it has drifted — rewrite it to name this model's specific
customers, price points, or cost levers, or drop it.

### 5. Pre-mortem each candidate — independently
For **each** candidate separately: *"Assume we shipped this and it failed 12 months later. What killed it?"*
Name concrete causes tied to this model's economics (price sensitivity, capacity limits, churn, CAC,
channel conflict, cannibalization). Do **not** write one shared "here are some risks" paragraph — each
option gets its own independent failure analysis. This is where most of the value is.

### 6. Score & tabulate
Build a comparison table so the pick is visibly earned:

| Candidate (lens) | Upside | Effort | Risk | Fit to model |
|---|---|---|---|---|
| … | H/M/L + one phrase | H/M/L | H/M/L + top risk | H/M/L |

### 7. Converge
Pick **one** recommended solution. State **why it beats the runner-up** — name the runner-up and the
tradeoff that decided it. Don't hedge into a tie; commit.

### 8. Harden the winner
Before presenting, pressure-test the recommendation itself:
- **Devil's-advocate pre-mortem** — run one more independent failure analysis on the *winner* specifically
  (it's the option most exposed to optimism bias). If it survives, say why; if it doesn't, revise the pick.
- **Flip-assumptions** — state the 1-2 assumptions that, if false, would change the recommendation ("what
  would change my mind").
- **Cheapest first-test** — the smallest, fastest experiment to validate it before committing to build
  (a smoke test, a landing page, a concierge/manual version, a price probe on 10 customers).

## Integrity rules
- **Always anchor** every candidate and every risk to the stated Model snapshot. Generic, model-agnostic
  advice is a failure.
- **Every candidate must be distinct** — one per lens; no two options that are the same bet reworded.
- **Every candidate gets its own independent pre-mortem** — never one shared risk note.
- **Always end in exactly one recommendation** with the runner-up tradeoff. This skill produces a decision,
  not a menu.
- **Refuse zero-to-one** gracefully — it enhances an existing model only.
- **Qualitative economics only** — reason about price/cost/margin directionally; never invent precise
  financial projections or fabricated numbers.
- **Run the intake** when context is thin rather than emitting a generic listicle.

## Output format

```
## Model snapshot
- Customers: … | Revenue: … | Cost driver: … | Moat: … | Goal: …

## Candidates
### 1. <Lens> — <candidate title>
<what it is, anchored to the snapshot>
Pre-mortem: <assume it failed — the concrete cause(s) tied to this model>
### 2. <Lens> — … (repeat per lens; mark lenses N/A with a reason)

## Scored comparison
<the upside/effort/risk/fit table>

## Recommendation: <the pick>
- Why this over <runner-up>: <the deciding tradeoff>
- Devil's advocate: <the strongest case it still fails, and why it survives / revised>
- What would change my mind: <the 1-2 flip assumptions>
- Cheapest first test: <the smallest experiment to validate before building>
```

Deliver in chat by default; offer to save it as a dated markdown decision record if the user wants one.

## Anti-patterns to avoid
- **Near-duplicate options** — five rewordings of one idea. The lenses exist to prevent this; use them.
- **Generic, un-anchored advice** — anything that could apply to any business means you skipped the anchor.
- **One shared risk paragraph** — pre-mortems must be per-candidate and independent, or the critique is theatre.
- **A flat list with no decision** — "here are six ideas, good luck" fails the whole purpose. Converge.
- **Forcing a lens that doesn't fit** — mark it N/A; a weak candidate dilutes the set.
- **Inventing financials** — fabricated ARR/CAC/margin numbers read as false precision. Stay qualitative.
- **Faking an enhancement for a non-existent business** — that's zero-to-one; decline and redirect.
