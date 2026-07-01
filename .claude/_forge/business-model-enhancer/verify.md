# Verify Report: Business Model Enhancer

## Trigger Arena
Set sizes: should-fire 9 · near-miss 9 · neighbor 6 · ambiguous 4. Router given ONLY descriptions
(candidate + forge neighbors), no workflow body.

| Prompt | Label (expected) | Router fired | Hit? | Notes |
|--------|------------------|--------------|------|-------|
| "Help me improve my business model, what could I add?" | this | this | ✓ | |
| "I want to add a referral program to my SaaS — good idea? what could go wrong?" | this | this | ✓ | |
| "Brainstorm enhancements to my subscription box and stress-test each" | this | this | ✓ | |
| "What new revenue stream should I add to my coffee shop?" | this | this | ✓ | |
| "Poke holes in my plan to add a marketplace and give the best version" | this | this | ✓ | |
| "Should my gym add corporate memberships? give me the ideal approach" | this | this | ✓ | |
| "Smartest thing to add to my existing app to grow revenue?" | this | this | ✓ | |
| "Stress-test adding an enterprise tier to my product" | this | this | ✓ | |
| "Evaluate adding AI to my invoicing tool and what could fail" | this | this | ✓ | |
| "Help me come up with a business idea" | none (zero-to-one) | none | ✓ | boundary holds |
| "Build me a financial model for my startup" | none | none | ✓ | |
| "Write my pitch deck" | none | none | ✓ | |
| "Brainstorm names for my product" | none | none | ✓ | |
| "Implement the new checkout feature in React" | none | none | ✓ | |
| "Write a business plan for a bakery" | none | none | ✓ | |
| "Give me landing-page marketing copy" | none | none | ✓ | |
| "Do a SWOT analysis of Tesla" | none | none | ✓ | softest near-miss; "enhance YOUR model" framing holds it out |
| "What should I name my company?" | none | none | ✓ | |
| "Suggest extra ideas for this skill I'm building" | forge-3b-ideate | forge-3b-ideate | ✓ | domain separation clean |
| "What else could my skill do?" | forge-3b-ideate | forge-3b-ideate | ✓ | |
| "Forge a new skill for X" | skill-forge | skill-forge | ✓ | |
| "Grill this skill brief" | forge-3-grill | forge-3-grill | ✓ | |
| "Is this skill idea unique?" | forge-2-novelty | forge-2-novelty | ✓ | |
| "Blueprint the SKILL.md" | forge-4-blueprint | forge-4-blueprint | ✓ | |

**Scores:** precision 1.0 · recall 1.0 · F1 1.0 · misfires: none. (bar: recall ≥0.8, 0 neighbor/near-miss fires — met.)
Ambiguous set: "improve my product/subscription/model to grow" → this-skill correctly wins when business
context present; noted one genuine ambiguity — bare "improve my model" could mean an ML model, but that
lacks business framing and routes to none, which is acceptable.
Self-repair applied? No — arena passed first run.

## Golden-example replay
- example-1 (evaluate / AI feature) → **passed** — workflow 1-8 produces intake, ≥4 distinct lens variants,
  per-candidate pre-mortems, scored table, one recommendation + hardening. All assertions satisfiable.
- example-2 (generate / gym revenue) → **passed** — one-candidate-per-lens + N/A handling + capacity-anchored
  pre-mortems + one testable pick.
- example-3 (thin-context guard + zero-to-one) → **passed** — workflow 1 runs intake-first and declines
  zero-to-one; both integrity rules present.
Total: **3/3.**

## Regression
N/A — intent: create.

## Usefulness
Wedge expressed in the build? **Yes** — diverge-by-lens (Workflow 3 + `strategic-lenses.md`), independent
per-candidate pre-mortem (Workflow 5, explicitly "not one shared paragraph"), scored convergence (6-7),
anchoring (2 + 4 integrity). Generic risk: **none** — the built workflow encodes the four novelty
commitments; it is not a "do the obvious thing" wrapper. `[!OVERLAP]` from Novelty resolved: the description
and workflow stay firmly in "enhance an existing model" and never contest the skill-authoring neighbors.

## Convention & completeness
- Frontmatter: `name` == folder slug (kebab) ✓; `version: 1.0.0` ✓; description has ≥5 trigger phrases + a
  "Do NOT use" boundary ✓.
- All blueprint sections present, filled, concrete; no placeholders/TODOs ✓.
- Integrity rules + anti-patterns are skill-specific (anchoring, per-candidate pre-mortem, one-decision,
  zero-to-one refusal, no invented financials) ✓.
- Output format: fenced template present ✓. Asset `references/strategic-lenses.md` exists and is invoked in
  Workflow 3 ✓.
- Voice matches toolkit (imperative, sectioned) ✓.

## Would-it-work dry run
Input: "local gym, $40/mo, want a new revenue stream." → intake fills cost/capacity/goal → snapshot →
6 lenses (corporate segment, online-class channel, premium tier, PT product, physio partnership, class-pack
model-shift; forces ≥1 N/A if unfit) → per-candidate pre-mortems → scored table → one pick + why over
runner-up + devil's-advocate + flip-assumptions + cheapest first-test. Every step has its inputs. No gaps.

## Coverage Manifest: clean
All §0 items `[x]`: name/slug, version, sharp description+boundary, novelty cleared, structure recorded
(standalone), when-to-use, concrete workflow, integrity rules, output format, anti-patterns, 3 golden
examples passing, asset present & invoked, no composition handoffs needed (struck: standalone),
passed verify.

## Consensus
Skipped — medium complexity, not high-stakes, and domain separation from all neighbors is unambiguous
(business-strategy vs skill-authoring). Single adversarial pass sufficient.

## VERDICT: PASS
Trigger Arena perfect (1.0/1.0), 3/3 golden examples replay clean, wedge is genuinely in the build (not
just claimed), conventions met, manifest clean. Recommend the install gate.
