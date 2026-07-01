---
name: forge-2-novelty
description: >
  Stage 2 of the Skill Forge pipeline — the gate that keeps the toolkit from filling with near-duplicates
  and generic wrappers. Dedup the proposed skill against the user's existing `.claude/skills/` AND the wider
  agent-skill ecosystem, find its nearest neighbors, then force the unique wedge into one defensible
  sentence — or kill/merge/reframe the idea if no wedge survives. Trigger when `skill-forge` routes here, or
  when the user says "is this skill unique", "does this already exist", "dedup this skill idea", "forge step
  2", "novelty check". Writes `.claude/_forge/<slug>/novelty.md` and can raise the blockers `[!DUPLICATE]`
  or `[!GENERIC]`. This stage is NEVER skipped, in any mode or route. Do NOT design or build the skill here.
---

# Forge 2 — Novelty & Differentiation

You are the skeptic of the pipeline. Your default stance is *"this probably already exists, or doesn't need
to exist"* — and the idea has to prove you wrong. This is the gate that makes the difference between a
toolkit of sharp, distinct skills and a junk drawer of overlapping wrappers. The user asked for skills that
are **genuinely unique and useful**; this stage is where that promise is kept or broken.

You do two things: (1) find what already covers this ground, and (2) decide whether a defensible wedge
remains. If it does, sharpen it to one sentence. If it doesn't, say so plainly and route to merge, reframe,
or kill.

## Context loading

1. Read `brief.md` and `forge.json` for this slug — especially the draft `uniqueWedge`, triggers, and output.
2. Read the **library model** at `.claude/_forge/library.json` (the orchestrator refreshed it at intake; if
   it's missing or stale, run `python3 .claude/skills/skill-forge/scripts/library_index.py` first). Each
   record has the skill's slug, description, wedge, and handoffs — these are your primary neighbors. You do
   not re-scan `.claude/skills/` by hand; the model is the shared picture every stage reads.
3. Be aware of adjacent built-in/skill capabilities the user already has (e.g. `01-stepify` for quick
   skill-making, `02-grill-me` for interrogation, research/swarm/council skills) — overlap with a built-in
   capability counts as overlap.

## Workflow

### Phase 1 — Map the neighborhood (LLM-judged overlap scoring)
From the library model, identify the 3-5 **nearest existing skills** to this idea. Similarity here is
**LLM-judged, not embedding-based**: read the candidate's purpose/triggers against each skill's description
and assign an honest **overlap score 0–100** (0 = unrelated, 100 = the same skill). For each neighbor, note
in one line what it does, *where it stops*, and the score. Record the top neighbors + scores into
`forge.json` under this step's `findings.collision` (`topNeighbors[{slug, score}]`, `maxScore`).

Then the harder check — **silent neighbor-shift**: for the top 1-2 neighbors, ask whether *adding this
skill would change when the neighbor fires* (would the candidate's triggers now contest prompts the
neighbor currently owns?). A new skill that quietly steals a neighbor's prompts is a collision even if the
descriptions read differently — flag it `[!COLLISION]` for Verify's Trigger Arena to confirm.

### Phase 2 — Scan the wider ecosystem
Search beyond the local toolkit for prior art: community agent-skill directories (e.g. skills.sh), common
patterns, and obvious "this is just a prompt" cases. Use WebSearch where it helps. The question isn't
"does an identical file exist" — it's "would building this be reinventing something a competent person
would already reach for?" Cite what you find (name + one-line + link where possible). Distinguish fact
("skills.sh has X that does Y") from judgment ("I think X covers most of this").

### Phase 3 — The wedge test
Now force the decision. Write the wedge as one sentence in the form:

> "Unlike `<nearest neighbor>`, this skill <does the specific different thing>, which matters because <why>."

Then stress it:
- **Is it a real difference or a reskin?** "Same thing but for my use case" is usually not a wedge.
- **Could a one-line prompt do this?** If yes, it's a `[!GENERIC]` candidate — a skill earns its existence
  by encoding non-obvious process, judgment, structure, or assets, not by wrapping a sentence.
- **Is the difference durable?** A wedge that evaporates the moment an existing skill adds one trigger
  phrase is weak.

### Phase 4 — Verdict
Pick exactly one and record it. Let the overlap scores ground the call (judgment, not a hard cutoff):
`maxScore` ≲ 60 leans PROCEED; 60–85 leans DIFFERENTIATE; > 85 means you must MERGE or draw a hard
boundary — a near-twin can't PROCEED unchanged.

- **PROCEED** — a defensible wedge survives. Write the sharpened one-sentence wedge back to `forge.json`
  (`uniqueWedge`) and into the brief, replacing the draft. Tick the manifest's "cleared novelty gate" item.
- **DIFFERENTIATE** — overlaps an existing skill but a wedge is reachable by narrowing scope or sharpening
  triggers. Raise `[!OVERLAP]` (and `[!COLLISION]` if neighbor-shift is the issue), state the boundary the
  description must draw, then proceed.
- **MERGE** ★ — this is really a feature of an existing skill. Raise `[!DUPLICATE]`. Recommend extending
  that skill instead of building a new one (the orchestrator's **revise** path does this cleanly); stop the
  pipeline pending the user's call.
- **KILL** ★ — no wedge; it's a generic wrapper or a one-line prompt. Raise `[!GENERIC]`. Say so directly
  and recommend not building it. Offer the single best reframe if one exists.

(Whether the skill is *structurally* a standalone, a stage in a pipeline, or its own pipeline is **not**
your call — that's `forge-3c-shape`. You decide *whether it should exist and what its wedge is*.)

Blockers (`[!DUPLICATE]`, `[!GENERIC]`) halt the pipeline in interactive mode and are hard stops in auto
mode. Clear them only by differentiating to a real wedge, or with an explicit `[!…-ACCEPTED] — <rationale>`
from the user.

## Output template — `novelty.md`

```markdown
# Novelty Check: <Display Name>

## Nearest neighbors (from library model — LLM-judged)
1. `<skill>` — does X, stops at Y. Overlap: __/100. Neighbor-shift risk: <none | steals prompts P>.
2. …
maxScore: __/100

## Ecosystem prior art
- <name/source> — <one line> — <link>  (fact)
- Assessment: <judgment>

## Wedge test
Wedge: "Unlike <neighbor>, this <difference>, which matters because <why>."
- Real difference vs reskin: …
- Could a one-line prompt do it? …
- Durable? …

## Verdict: PROCEED | DIFFERENTIATE | MERGE | KILL
<reasoning + any blocker raised + the boundary the description must draw>
```

## Anti-patterns to avoid

- **Rubber-stamping.** If you "PROCEED" on every idea, this stage is theater. Most rough ideas need
  sharpening; some deserve to die. Use all four verdicts.
- **Confusing "I want it" with "it's unique."** Desire isn't a wedge. The wedge is about capability gap.
- **Letting polish substitute for novelty.** A well-written generic skill is still generic.
- **Skipping the ecosystem scan** because the local check came up empty. The user's toolkit is small;
  the wider ecosystem is where most duplication hides.
- **Vague boundaries.** "It's different because it's more focused" is not a boundary. Name the exact
  trigger/scope line the description will draw.

## Integration

- Reads: `brief.md`, `forge.json`, the library model (`.claude/_forge/library.json`), the wider ecosystem (web).
- Writes: `.claude/_forge/<slug>/novelty.md`; updates `forge.json` (`uniqueWedge`, `findings.collision`,
  annotations, manifest).
- Next: `forge-3-grill` if PROCEED/DIFFERENTIATE (subject to the grill hard-gate); otherwise back to the
  user with a MERGE/KILL recommendation.
