# Blueprint: Business Model Enhancer (`business-model-enhancer`)

## Frontmatter
- name: `business-model-enhancer`
- version: `1.0.0`
- description (draft):
  > "Stress-test and enhance an EXISTING business model: generate distinct candidate improvements (one per
  > strategic lens), run an independent pre-mortem on each, and converge on one recommended solution with the
  > runner-up tradeoff. Trigger when the user says 'help me improve my business model', 'I want to add X to my
  > product — is it a good idea and what could go wrong', 'brainstorm enhancements and stress-test them',
  > 'what new revenue stream should I add', or 'poke holes in this idea and give me the ideal version'. Runs a
  > short intake first if the model isn't described. Do NOT use for zero-to-one/blank-slate business creation,
  > financial modeling/projections, business-plan or pitch-deck writing, or implementing the chosen change."
- handoffs_to / expects_from: **none** (standalone)

## Section plan
- **# Business Model Enhancer** — purpose: "Turn a proposed enhancement (or a growth goal) for an existing
  business model into one anchored, stress-tested, recommended solution."
- **## When to use** — 5-6 natural fire phrases (both the evaluate and generate branches) + explicit NOT-use
  boundary (zero-to-one, financial modeling, plan/deck authoring, implementation, generic brainstorming).
- **## Workflow** — numbered phases (this is a multi-phase judgment skill):
  1. **Detect branch & intake** — decide evaluate (specific idea) vs generate (goal only). If the model's
     economics aren't described, run a **tight intake** (what you sell · to whom · how you make money · main
     cost driver · current goal); skip questions already answered. Detect **zero-to-one** → decline+redirect (B2).
  2. **Anchor** — restate a compact model snapshot (customers · revenue mechanics · cost structure · moat).
     Everything downstream must tie back to this.
  3. **Diverge by lens** — generate one candidate per strategic lens from `references/strategic-lenses.md`;
     a lens that doesn't fit → mark **N/A + reason** (B3). Evaluate-branch: frame the user's idea through
     the lenses to produce genuinely distinct *variants*.
  4. **Anchor-integrity check** — for each candidate, verify it's tied to the snapshot's economics; rewrite
     any that drift into generic advice (B1).
  5. **Pre-mortem each candidate independently** — "assume this specific option failed 12 months out — why?"
     Name concrete causes tied to the model; do NOT share one risk paragraph across candidates.
  6. **Score & tabulate** — a table: candidate × (upside · effort · risk · fit) (C1).
  7. **Converge** — pick one recommendation; show **why it beats the runner-up** + the tradeoff.
  8. **Harden the winner** — run one **devil's-advocate** pre-mortem specifically on the pick (C4); state the
     **flip-assumptions** ("what would change my mind", A1); append the **cheapest first-test** to validate
     it before building (A4).
- **## Integrity rules** — anchor everything to the stated model; every candidate distinct (one per lens);
  every candidate independently pre-mortemed; never emit a generic listicle; always end in ONE decision;
  refuse zero-to-one; qualitative economics only (no invented financial projections).
- **## Output format** — a template: **Model snapshot → Candidates (one per lens, w/ pre-mortem) → Scored
  table → Recommendation (why over runner-up · flip-assumptions · cheapest first-test)**. Chat by default;
  offer to save as a file.
- **## Anti-patterns to avoid** — near-duplicate options; generic un-anchored advice; shared soft critique;
  a flat list with no decision; forcing a lens that doesn't fit; inventing precise financials.

## Assets
- scripts/: **none** (pure reasoning; no deterministic execution needed).
- references/: **`strategic-lenses.md`** — the divergence engine. A table of ~6 lenses (New pricing/packaging ·
  New segment · New channel/distribution · Product/feature depth · Partnership/ecosystem · Business-model
  shift), each with: what it asks, an example move, and "when this lens is N/A". Load-bearing (guarantees
  forced divergence — novelty commitment #2).
- references/examples/: **3 golden examples** (below).

## Golden examples (Build writes to references/examples/)
1. **evaluate-ai-feature.md** — Input: freelancer-invoicing SaaS, flat $15/mo, "should I add an AI feature?"
   Assertions: intake confirmed/filled; ≥4 *distinct* lens variants (not 4 chatbots); each has its own
   pre-mortem tied to freelancer price-sensitivity/churn; scored table present; ONE recommendation naming the
   runner-up tradeoff + flip-assumptions + a cheapest first-test.
2. **generate-gym-revenue.md** — Input: local gym, $40/mo, "new revenue stream", no specific idea.
   Assertions: intake gaps filled; one candidate per lens (with ≥1 lens marked N/A + reason if it doesn't
   fit); pre-mortems tied to gym fixed-cost/capacity; scored table; one recommendation + first-test.
3. **thin-context-guard.md** — Input: "give me ideas to improve my business" (no detail). Assertions: does
   NOT emit a generic listicle; runs the tight intake first; (bonus) zero-to-one variant → graceful decline.

## Trigger Arena expectation (for Verify)
- **should-fire:** "help me improve my business model"; "should I add X to my product, what could go wrong";
  "brainstorm enhancements to my subscription and stress-test them"; "what new revenue stream should I add";
  "poke holes in this idea and give me the ideal version".
- **should-NOT-fire:** "help me come up with a business idea" (zero-to-one); "build me a financial model";
  "write my pitch deck"; "brainstorm names for my product".
- **nearest neighbor the boundary must beat:** `forge-3b-ideate` (overlap 8/100 — different domain; low risk).

## Manifest → section map
- diverge→pre-mortem→converge loop → Workflow phases 3/5/7
- divergence engine forces distinct suggestions → Workflow 3 + `references/strategic-lenses.md`
- every suggestion paired with issues/risks → Workflow 5
- convergence rule picks one solution → Workflow 7 + Output format
- context-intake behavior → Workflow 1
- flip-assumptions (A1) → Workflow 8 + Output
- cheapest first-test (A4) → Workflow 8 + Output
- anchor-integrity self-check (B1) → Workflow 4 + Integrity rules
- zero-to-one declined (B2) → Workflow 1 + Integrity rules + description boundary
- lens N/A handling (B3) → Workflow 3 + `strategic-lenses.md`
- scored table (C1) → Workflow 6 + Output
- devil's-advocate on winner (C4) → Workflow 8
- sharp description w/ ≥3 phrases + boundary → Frontmatter/description
- ≥2 golden examples → references/examples/ (3 planned)
