# Refined Brief: Business Model Enhancer

## Resolved in grilling
- **Generate vs evaluate?** → **Both, with a detected branch.** At the top the skill decides: user brought a
  *specific enhancement* → diverge it into variants, then stress-test; user brought only a *goal* → generate
  candidates first, then stress-test. Both funnel into the same convergence.
- **Context intake when the model isn't described?** → **Tight intake first.** Ask 3-5 targeted questions
  (what you sell, to whom, how you make money, main cost driver, current goal) before diverging. Skip any the
  user already answered; don't re-ask.
- **Convergence shape?** → **One pick + why it beat the rest.** A single recommended "perfect solution", plus
  a short rationale naming the runner-up(s) and the key tradeoff. Decisive but transparent.
- **How is divergence forced?** → **Distinct strategic lenses.** Generate one candidate per fixed lens
  (new pricing/packaging · new segment · new channel · product/feature · partnership/ecosystem ·
  business-model shift). Structurally guarantees genuinely different options. The lens set is a **reference
  asset** the skill ships with.

## Exclusions (explicitly out of scope)
- **Zero-to-one / blank-slate** business creation — this skill enhances an *existing* model only.
- **Financial modeling** — no spreadsheets, projections, or precise unit-economics computation. It reasons
  qualitatively about economics; it does not compute the numbers.
- **Business plan / pitch deck authoring** — it produces a decision artifact, not a document deliverable.
- **Market-research reports / primary data gathering** as the main output (optional light validation only).
- **Implementation/build** of the chosen enhancement.
- **Non-business brainstorming** (naming, creative copy, general ideation).

## Failure modes & guards
- **Near-duplicate options** (5 rewordings of one idea) → Guard: fixed strategic lenses, one candidate per lens.
- **Generic, un-anchored advice** ("add a subscription tier") → Guard: mandatory intake; every suggestion
  tied to the *stated* customers / revenue mechanics / cost structure / moat.
- **Soft, anchored critique** (one shared "there are risks" paragraph) → Guard: an **independent pre-mortem
  per candidate** — imagine *this specific option* failed, name the concrete cause.
- **Indecision** (a flat list, no answer) → Guard: scored convergence to one recommendation + runner-up tradeoff.
- **Thin context** (user gives almost nothing) → Guard: run the tight intake before generating anything;
  refuse to emit a generic listicle.

## Quality bar
- **A great output:** anchored to the user's actual model's economics; options genuinely span distinct lenses;
  each candidate has its own specific pre-mortem (named failure causes, not "there are risks"); ends in one
  clear recommendation with the runner-up tradeoff shown; runs intake when context is thin.
- **A bad output:** advice that could apply to any business; near-duplicate options; a single vague shared
  risk note; a flat list with no decision; ignores or contradicts the stated model.

## Golden scenarios (seed Build's examples + Verify's replay)
1. **Evaluate branch.** Input: B2B SaaS invoicing tool for freelancers, flat $15/mo — "I want to add an AI
   feature, should I?" → A great output asserts: confirms/fills intake; diverges "AI feature" across
   *distinct lenses* (not 5 chatbot flavors); each candidate gets an independent pre-mortem anchored to
   freelancer price-sensitivity & churn; converges on ONE recommendation naming the runner-up tradeoff.
2. **Generate branch.** Input: local gym, $40/mo membership, "I want a new revenue stream" (no specific
   idea). → A great output asserts: fills intake gaps; one candidate per lens (corporate segment, online-class
   channel, premium tier packaging, physio/nutrition partnership, supplements product); each pre-mortemed
   against gym fixed-cost/capacity reality; one recommendation + why over runner-up.
3. **Thin-context guard.** Input: "Give me ideas to improve my business" with zero detail. → A great output
   asserts: does NOT dump a generic listicle; runs the tight intake first, then proceeds. A bad output:
   "improve your marketing, start a newsletter…" with no anchoring.

## Updated triggers / I/O / wedge
- **Trigger branch added:** fires for both "test my idea" and "give me ideas for [goal]" phrasings, as long as
  an *existing* model is (or can be) established. Still does NOT fire for blank-slate/zero-to-one.
- **Input:** existing model (elicited via intake if absent) + optional specific enhancement.
- **Output:** structured markdown — Anchored model snapshot → candidates (one per lens) → per-candidate
  pre-mortem → single recommendation + runner-up tradeoff. Chat by default; offer a file.
- **Wedge:** unchanged from novelty (diverge-by-lens → independent per-candidate pre-mortem → scored
  convergence, anchored to the existing model's economics).
- **Assets:** needs a `references/` file — the **strategic lens set** (+ likely a pre-mortem prompt structure).
  No scripts.

## Deferred (routed to Ideate)
- Optional **web research** / competitor validation as an enrichment.
- Named **frameworks** (Jobs-to-be-Done, Business Model Canvas, PESTLE) as optional lenses or scoring aids.
