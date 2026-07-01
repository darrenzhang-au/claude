# Novelty Check: Business Model Enhancer

## Nearest neighbors (from library model — LLM-judged)
The library currently holds only the 9 Skill Forge (meta / skill-authoring) skills. None operate in the
business-strategy domain, so local overlap is near-zero:

1. `forge-3b-ideate` — generates *idea menus*, but for **skills being forged**, not business models. It's a
   divergence engine in a totally different domain. Overlap: **8/100**. Neighbor-shift risk: none (its
   triggers are all skill-pipeline phrasing).
2. `forge-3-grill` — Socratic interrogation to harden a spec; shares the "surface what's missing" instinct
   but targets a skill brief, not a business idea. Overlap: **6/100**. Neighbor-shift: none.
3. `skill-forge` / others — orchestration & authoring. Overlap: **<5/100**.

**maxScore: 8/100** (local). No `[!DUPLICATE]`, no `[!COLLISION]` — nothing in the toolkit contests these
triggers.

## Ecosystem prior art (the real pressure)
- **Business Model Stress Testing** — an academic/consulting method: structured model description × trends
  and uncertainties (PESTLE), test robustness. (fact) — https://www.sciencedirect.com/science/article/pii/S001632871630341X
- **Pre-mortem analysis** (Gary Klein) — imagine the initiative has already failed, work backward; crucially
  each person forms failure hypotheses **independently** to avoid anchoring. Raises failure-spotting ~30%.
  (fact) — https://newoon.com/the-hidden-power-of-pre-mortem-analysis-in-business-development/
- **"Use AI to stress-test your startup idea"** — mainstream how-to: feed the model your one-liner, ask it
  to find holes, name competitors, argue why a buyer walks. (fact) — https://www.inc.com/diana-bocco/ai-claude-chatgpt-stress-test-startup-idea/91363659
- **Assessment (judgment):** the *concept* — brainstorm + poke holes + recommend — is common and a competent
  person would reach for a plain prompt. So the naive version is **[!GENERIC]**. What is NOT commonly
  packaged is a *repeatable, disciplined method* that (a) anchors strictly to the user's **existing** model's
  economics, (b) runs an **independent, unanchored** pre-mortem per candidate (the thing the research says
  people get wrong), and (c) applies an explicit **scored convergence** rule to synthesize one recommendation
  rather than dumping a list. That encoded process is the wedge.

## Wedge test
Wedge: "Unlike a plain 'brainstorm ideas and list pros/cons' prompt (or the generic AI stress-test pattern),
this skill encodes a repeatable **diverge → independent-per-candidate pre-mortem → scored convergence**
method **anchored to the user's existing model's economics**, which matters because the naive prompt
reliably produces near-duplicate ideas, anchored/soft critique, and a flat list instead of a decision."

- **Real difference vs reskin?** Real *if* the process is genuinely encoded (forced-distinct divergence,
  per-candidate independent risk pass, scored pick). If Build lets it collapse into "here are 5 ideas and
  some cons," the wedge evaporates. This is a conditional PROCEED — the structure must survive to Verify.
- **Could a one-line prompt do it?** A one-liner produces *a* version, but not reliably the disciplined,
  anchored, decision-producing version. The skill's value is consistency + method, not novelty of concept.
- **Durable?** Yes — it's a process/quality wedge, not a "for my niche" reskin. No existing skill contests it.

## Verdict: DIFFERENTIATE → PROCEED with a mandated boundary
Local collision is negligible; the idea survives. But it clears the `[!GENERIC]` risk **only** by committing
to encoded structure. Boundary the description + workflow MUST draw:

1. **Anchored, not generic** — always ground suggestions in the *stated existing model's* customers, revenue
   mechanics, cost structure, and moat. Refuse to hand out generic "add a subscription tier" advice.
2. **Forced divergence** — a mechanism that guarantees genuinely *different* angles (not 5 rewordings of one).
3. **Independent per-candidate pre-mortem** — each option gets its own unanchored failure pass, not one shared
   critique paragraph.
4. **Scored convergence to a decision** — an explicit rule for synthesizing/selecting the single recommended
   "perfect solution," with the reasoning shown.

Carry `[!OVERLAP]` (vs the generic ecosystem pattern, not a local skill) forward: Grill and Blueprint must
keep the four commitments above concrete, and Verify must confirm the built skill actually does them and
isn't a dressed-up one-liner.
