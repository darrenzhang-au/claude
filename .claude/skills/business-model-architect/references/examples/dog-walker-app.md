# Golden Example 1 — Thin input, intake required

## Input
> "I want to build an app for dog walkers."

(No customer specified, no problem stated, no ambition, no payer.)

## A great output asserts
- **Runs intake BEFORE generating** — asks the missing anchors (who pays: walkers or owners? what's broken about how they do it today? bootstrapped or venture-scale? main cost driver?), in one short batch. Does NOT emit a model on the first turn.
- After anchors are supplied, **converges on exactly ONE recommended model** (e.g., a take-rate marketplace charging owners, vs. a subscription for walkers) — not a list.
- **Names who pays explicitly** and flags it as a decision (walkers are usually price-sensitive; owners are the likelier payer).
- Includes **all five decision elements**: recommended model + why it beats the alternatives + runner-up & tradeoff + riskiest assumption + cheapest validation.
- **Riskiest assumption is concrete** (e.g., "walkers won't pay a monthly SaaS fee, so revenue must come from owners") with a **cheap test** sized to it (e.g., pre-sell 10 owners a booking, or a landing page).
- **No invented statistics** presented as fact; any unverified market claim sits in an "Assumptions (unverified)" ledger.

## A bad output has
- A filled canvas or three near-identical subscription options with no pick.
- A confident model generated with zero intake, inventing the payer and the market.
- Missing runner-up / riskiest-assumption / validation.

**Why:** this is the core case — thin input that must trigger intake, then a real convergence. It exercises the "never invent a market" guard and the decision contract.
