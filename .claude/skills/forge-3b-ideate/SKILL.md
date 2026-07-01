---
name: forge-3b-ideate
description: >
  Stage 3b of the Skill Forge pipeline — the creative-genius step. Given a brief that cleared novelty and
  grilling, propose the additions the user *didn't* think to ask for: three themed sets of four ideas each
  (scope extensions, robustness & safety, delight & leverage) presented as an explicit accept/reject menu,
  with an optional clarifying round on whatever gets accepted. Enriches a skill before it's designed —
  without unilaterally inventing scope. Trigger when `skill-forge` routes here, or when the user says
  "what else could this skill do", "suggest extra ideas for this skill", "ideate on this skill", "forge
  step 3b", "enrich the skill", "give me ideas I didn't think of". Reads `grill.md`/`brief.md`, writes
  `.claude/_forge/<slug>/ideation.md`. Full-route only; auto-skips for trivial/Lite skills and skips
  entirely when the user flagged the idea as strict/locked. Do NOT design SKILL.md sections here (that's
  `forge-4-blueprint`) and do NOT interrogate the core brief here (that's `forge-3-grill`).
---

# Forge 3b — Ideate

You are the creative genius of the pipeline. Every prior stage has been faithful to what the user *said*;
your job is the one thing they can't do for themselves — surface the good additions they never thought to
ask for. You hand them a menu, not a mandate: *"You may not have thought of these — here are three sets of
four ideas you could consider including."* They keep what they like and discard the rest. Nothing you
propose enters the skill until the user accepts it.

The bar is high. Ideas must be *specific to this skill* (not "add error handling" but "if the input
transcript has no timestamps, fall back to paragraph-index anchors") and must serve the wedge, not dilute
it. A menu of generic filler is worse than no menu — it wastes the user's attention and tempts scope creep.

## When to run vs skip

- **Run** (default in the Full route) when the idea has room to grow — most non-trivial skills.
- **Skip** when `skill-forge` routed Lite or complexity is `trivial` (auto-skip, confirm and hand to
  Blueprint), or when the user flagged the idea as **strict / locked / "no extra ideas" / "exactly as
  described"** at intake — the orchestrator records this; honor it without proposing.
- If the brief is already tight and well-bounded, you *may* propose fewer or note that the idea is mature
  and recommend skipping — but say so explicitly rather than padding to hit twelve.

## Context loading

1. Read `grill.md` if it exists (the refined brief — especially Exclusions and the Quality bar), else
   `brief.md`. The Exclusions list is a hard fence: never propose something already ruled out without
   flagging the tension explicitly.
2. Read `novelty.md` for the wedge and any `[!OVERLAP]` boundary — every proposed idea must keep the wedge
   sharp and stay on the right side of that boundary.
3. Read `forge.json` for the skill profile, complexity, and the `ideationEnabled` flag.
4. Glance at 1-2 structurally similar existing skills for what "good" additions look like in this category.

## The three sets (adapt the lenses to the skill)

Propose **exactly three sets of four ideas** (twelve total) unless the idea is genuinely thin — then ship
fewer and say which set ran dry. Default lenses; rename them to fit the skill's category:

- **Set A — Scope extensions.** Adjacent things the skill could *also* do: extra output modes, variants,
  a batch path, a complementary artifact, a second trigger surface.
- **Set B — Robustness & safety.** What the skill should do when reality misbehaves: missing inputs,
  malformed data, ambiguous requests, guards against the failure modes grill surfaced, graceful refusal.
- **Set C — Delight & leverage.** The affordances that make it feel crafted: presets, worked examples,
  sensible defaults, integration hooks into the user's other skills/tools, power-user options.

Each idea is one line in the form:

> **A2. <short title>** — <what it adds and the concrete situation it helps> · cost: S/M/L · wedge: strengthens | neutral | risks-dilution

`cost` is your honest read of build complexity. `wedge` flags whether the idea sharpens the core, is
neutral, or risks bloating it — be willing to label your own idea `risks-dilution` so the user can weigh it.

## Workflow

1. **Generate.** Produce the three sets (A1–A4, B1–B4, C1–C4) to the format above. Make them specific,
   non-overlapping, and ranked best-first within each set. Flag any stretch/low-value idea as such rather
   than dressing it up.
2. **Present the menu.** Show all twelve and ask the user to accept by id (e.g. "A2, B1, C3, C4"). Default
   for anything unanswered is **reject**. Make clear they can accept zero — the skill is already complete
   without any of these.
3. **Optional clarifying round.** If an *accepted* idea needs a scoping decision before it can be designed
   (e.g. "you took A2 — should the batch mode cap at N items or stream?"), ask a short round of questions —
   one at a time, and only about accepted ideas. Skip this round entirely if every accepted idea is
   self-explanatory. Do not re-grill the core brief; that's done.
4. **Integrate.** For each accepted idea, write how it changes the brief and which future section/asset it
   lands in. Add a Coverage Manifest item per accepted idea that expands what the skill must contain.
5. **Record.** Write `ideation.md`. Update `forge.json`: append a `decisions[]` row per accepted idea
   (`step: "forge-3b-ideate"`, `provenance: "user"`), add the new manifest items, mark `forge-3b-ideate`
   complete. Hand back a short summary (accepted / rejected counts) and the next stage (Blueprint).

**Auto mode.** Generate the full menu, default-**reject** all twelve (provenance `default`), and write them
to `ideation.md` + the ledger so the final gate can surface them. Do not run the clarifying round and do not
include anything — the user flips-to-include accepted ideas at the final gate, which re-runs Blueprint →
Build → Verify for the additions.

## Output template — `ideation.md`

```markdown
# Ideation: <Display Name>  (`<slug>`)

## Status
Ran (proposed 3×4) | Skipped — <reason: lite | trivial | strict-idea | mature-brief>

## Proposed menu
### Set A — <lens>
- **A1. <title>** — <what it adds + when it helps> · cost: S/M/L · wedge: strengthens|neutral|risks-dilution
- A2 … A4
### Set B — <lens>
- B1 … B4
### Set C — <lens>
- C1 … C4

## Verdicts
- Accepted: <ids>
- Rejected: <ids>
- Flagged stretch / low-value: <ids, if any>

## Clarifying round (if run)
- <question> → <answer>

## Integrated additions (carried into Blueprint)
- <accepted id + title> → <how it changes the brief / target section or asset>

## Manifest additions
- [ ] <new coverage item from an accepted idea>
```

## Anti-patterns to avoid

- **Generic filler.** "Add logging", "support more formats", "make it configurable" — if an idea could apply
  to any skill, it's not an idea, it's padding. Every proposal must name a situation specific to *this* skill.
- **Padding to twelve.** Three sets of four is the target, not a quota. A thin idea shipped to fill a slot
  costs the user more attention than it's worth — ship fewer and say so.
- **Proposing excluded scope.** Grill drew the exclusion fence for a reason. Don't re-litigate it; if an idea
  genuinely reopens an exclusion, flag the tension and let the user choose, don't smuggle it in.
- **Diluting the wedge.** The most dangerous ideas are the attractive ones that turn a sharp skill into a
  Swiss-army knife. Label `risks-dilution` honestly; a great skill says no to good ideas.
- **Including without acceptance.** Silence is rejection. Nothing enters the brief unless the user says yes.
- **Re-grilling the core.** Your questions are about *accepted additions only*. The brief's core was pinned
  down in stage 3 — don't reopen it.
- **Designing the skill.** Sections, prose, templates are Blueprint's job. You decide *what else*, not *how*.

## Integration

- Reads: `grill.md`/`brief.md`, `novelty.md`, `forge.json`, nearest existing skills (for calibration).
- Writes: `.claude/_forge/<slug>/ideation.md`; updates `forge.json` (`decisions[]`, manifest, step status).
- Next: `forge-3c-shape` — accepted additions are part of the final scope it sizes; then `forge-4-blueprint`,
  which must honor every integrated addition and ignore the rejected ones.
