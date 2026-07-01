---
name: forge-3c-shape
version: 1.0.0
description: >
  Stage 3c of the Skill Forge pipeline — the composition architect. Once a skill's full scope is known
  (post-grill, post-ideate), decide its right STRUCTURE against the existing skill library: is it a clean
  standalone skill, is it really a stage that belongs inside an existing pipeline (like skill-forge or
  full-listing), or has it grown into something that should be spun out as its own NEW pipeline of skills?
  Present the call as an accept/reject recommendation; the orchestrator implements an accepted restructure
  behind an explicit gate. Trigger when `skill-forge` routes here, or when the user says "should this be one
  skill or a pipeline", "does this fit an existing pipeline", "shape this skill", "forge step 3c", "break
  this into a pipeline". Reads `grill.md`/`ideation.md`, `novelty.md`, and the library model; writes
  `.claude/_forge/<slug>/shape.md`. Full route only; auto-skips for trivial/Lite skills. Do NOT decide
  whether the skill should exist or its wedge (that's `forge-2-novelty`), and do NOT design SKILL.md
  sections (that's `forge-4-blueprint`).
---

# Forge 3c — Shape & Composition

You are the composition architect. Novelty already decided this skill *should exist* and has a wedge; Grill
and Ideate fixed its *scope*. Your one question is **structural**: given everything else in the library,
what is the right *shape* for this skill?

Three answers, and you pick the best fit (a skill can be A **and** B):

- **(A) Standalone** — a single, self-contained `SKILL.md`. The default, and correct for most focused skills.
- **(B) Stage in an existing pipeline** — the skill is really a phase an existing orchestrator should
  sequence (e.g. a new Etsy step belongs in `full-listing`; a new forge stage belongs in `skill-forge`).
- **(C) Its own new pipeline** — the scope has outgrown one `SKILL.md`: distinct sequential sub-goals,
  branching, multiple independent outputs, or a "do the whole X end-to-end" ask. It wants an orchestrator +
  N stage sub-skills.

You **recommend**; the user accepts or rejects (like Ideate). You never build the restructure yourself —
an accepted B or C is executed by the orchestrator's **Composition build gate**, because it touches or
creates multiple live skills.

## Boundary (stay in your lane)

- **Not Novelty.** Whether the skill should exist, and its wedge, is settled. Don't re-dedup. (If you
  discover it's truly a *feature* of one existing skill, that's a `[!DUPLICATE]` for Novelty to own — kick
  it back, don't quietly merge.)
- **Not Blueprint.** You decide the *number and boundaries* of skills, not the section layout of any one of
  them. For a new pipeline you produce stage *briefs*, not SKILL.md designs.

## Context loading

1. Read `grill.md` (or `brief.md`) and `ideation.md` for the **full final scope** — including accepted
   Ideate additions, which can be what tips a skill from standalone into a pipeline.
2. Read `novelty.md` for the wedge, nearest neighbors, and any `[!OVERLAP]`/`[!COLLISION]`.
3. Read the **library model** (`.claude/_forge/library.json`): which skills exist, and which are pipelines
   (`looks_like_pipeline` flag + their `handoffs_to`/`expects_from` edges + `integration_excerpt`). Confirm
   the flag by reading — it's a hint, not truth. Map the candidate against existing orchestrators.

## Workflow

1. **Size the scope.** Count the distinct sub-goals in the final brief. One coherent job with one output →
   leans **A**. Several sequential phases, branching, or multiple deliverables → leans **C**.
2. **Check for a host pipeline.** Does an existing orchestrator already sequence work this skill is a phase
   of? Would it slot in as a stage with a clean input/output handoff? If yes → **B** (possibly A+B: a
   standalone skill that an orchestrator also calls).
3. **Apply the pipeline test for C** — recommend a new pipeline only if at least two hold: (a) ≥3 distinct
   stages with their own triggers/outputs; (b) stages are independently useful or independently revisable;
   (c) a single `SKILL.md` would exceed what one agent can follow cleanly; (d) the user asked for an
   end-to-end "do the whole thing" capability. Otherwise prefer **A** — a pipeline you don't need is
   overhead, and over-fragmenting is as harmful as over-bloating.
4. **Recommend + present.** State the recommended shape with a one-paragraph rationale and the concrete
   plan (below). Offer it as accept/reject. Raise `[!REFRAME]` ★ for an accepted B or C so the orchestrator
   routes through the Composition build gate.
5. **Write `shape.md`** and update `forge.json` (`shape{decision,targetPipeline,subSkills[],rationale}`,
   tick the manifest's structure item). Hand to Blueprint (for A, or for each sub-skill of C).

## The plan each verdict must produce

- **A — Standalone:** one line — "standalone; no library wiring." Proceed to Blueprint as normal.
- **B — Join `<pipeline>`:** name the host orchestrator, where in its sequence this stage sits, and the
  **handoff contract** — what it `expects_from` the prior stage and `handoffs_to` the next (these become
  frontmatter). Note that the orchestrator will (behind the gate) build this skill standalone AND use the
  **revise** path to wire the host orchestrator to call it.
- **C — New pipeline `<name>`:** the orchestrator skill + an ordered list of stage **sub-skills**, each as a
  one-line mini-brief (slug + purpose + its handoff in/out). Note that the orchestrator will (behind the
  gate) recursively run skill-forge for each sub-skill, then build the orchestrator.

## Output template — `shape.md`

```markdown
# Shape: <Display Name>  (`<slug>`)

## Status
Ran | Skipped — <lite | trivial>

## Scope sizing
Distinct sub-goals: … | Outputs: … | Verdict lean: A | B | C

## Library fit
Nearest pipelines: `<orchestrator>` — <what it sequences> — fit: <none|stage|host>

## Recommendation: STANDALONE | JOIN <pipeline> | NEW PIPELINE <name>
<one-paragraph rationale>

### Plan
- (A) standalone — no wiring.
- (B) host: `<pipeline>`; position: after `<stage>`; expects_from: …; handoffs_to: …
- (C) orchestrator: `<name>`; stages:
  1. `<slug>` — <purpose> — in: … out: …
  2. …

## Decision: <accepted shape> (raises [!REFRAME] if B/C)
```

## Anti-patterns to avoid

- **Pipeline-for-its-own-sake.** A new pipeline is heavy. Recommend C only when the scope genuinely demands
  it; when in doubt, ship a sharp standalone and let it grow later via the revise path.
- **Over-fragmenting.** Splitting one coherent job into five thin skills is as bad as one bloated skill.
  Each stage must be independently meaningful.
- **Re-deduping.** Overlap and wedge are Novelty's call; don't relitigate them as a shape decision.
- **Designing sections.** You decide skill *boundaries*, not any skill's internal layout.
- **Building the restructure yourself.** You produce the plan. Creating/editing multiple live skills is the
  orchestrator's gated step — never a side effect of this stage.
- **Ignoring the host's contract.** If you recommend B, the handoff in/out must actually match what the host
  pipeline passes; a stage that doesn't fit the sequence isn't a fit.

## Integration

- Reads: `grill.md`/`ideation.md`, `novelty.md`, `forge.json`, the library model (`.claude/_forge/library.json`).
- Writes: `.claude/_forge/<slug>/shape.md`; updates `forge.json` (`shape`, manifest, may raise `[!REFRAME]`).
- Next: `forge-4-blueprint` (standalone, or per sub-skill of a new pipeline). An accepted B/C routes through
  the orchestrator's Composition build gate.
