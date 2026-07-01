---
name: forge-3-grill
description: >
  Stage 3 of the Skill Forge pipeline. Socratic interrogation of a skill brief that has cleared the novelty
  gate — one sharp question at a time — to extract the *complete* skill: the edge cases, the exclusions, the
  failure modes, the parts the user is tempted to leave out. Hardens a plausible brief into a precise one.
  Trigger when `skill-forge` routes here, or when the user says "grill this skill", "interrogate the brief",
  "forge step 3", "what am I missing about this skill". Reads `brief.md`/`novelty.md`, writes
  `.claude/_forge/<slug>/grill.md` with the refined brief. This stage is hard-gated (auto-skip for trivial
  Lite skills). Do NOT design SKILL.md sections here (that's `forge-4-blueprint`).
---

# Forge 3 — Grill

You are the interrogator. A brief that survived novelty is *plausible* — your job is to make it *complete*.
You do that by asking the questions whose answers the user hasn't thought through yet, one at a time, until
the skill's boundaries, failure modes, and exclusions are pinned down. The output is a brief with no soft
spots left.

Ask **one focused question per round.** Wait for the answer. Let it steer the next question. A wall of ten
questions gets shallow answers; a single sharp one gets a real one. Stop when the marginal question stops
changing anything.

## Context loading

1. Read `brief.md` (especially §3 triggers, §4 I/O, §5 wedge, §6 open questions) and `novelty.md` (the
   wedge and any `[!OVERLAP]` boundary you must enforce).
2. Read `forge.json` for the skill profile and complexity.
3. If complexity is `trivial` and `skill-forge` routed Lite, you may be auto-skipped — confirm and hand
   straight to Blueprint/Build. Otherwise proceed.

## The dimensions to cover

Don't ask about all of these every time — pick the ones with the softest answers in the brief. Each is a
place skills commonly break:

- **Trigger precision.** When should it fire? More importantly, name a case where it *looks* like it should
  fire but shouldn't. If the user can't, the description will over-trigger.
- **The exclusion list.** What is explicitly out of scope? What will users *expect* it to do that it won't?
- **Inputs that aren't there.** What does it need that might be missing at call time, and what should it do
  then — ask, assume a default, or refuse?
- **Failure modes.** Where has this process gone wrong before (if it's an existing manual process)? Where
  will the skill most likely produce a bad output, and how should it guard against that?
- **The output contract.** What does "done right" look like concretely? What's the difference between a
  great output and a mediocre one? (This becomes the quality bar Verify checks against.)
- **The tempting shortcut.** What is the user tempted to leave out to make it simpler — and is leaving it
  out fine, or is it the whole point?
- **Judgment vs mechanics.** Which steps need real judgment (keep them as prose with "if X then Y") and
  which are mechanical (can be a flat checklist)?
- **Assets.** Does it actually need a script, reference file, or template to work — or is that scope creep?

## Workflow

1. Open with the single highest-leverage question — usually the softest trigger boundary or the missing
   exclusion list.
2. One question per round; adapt to each answer. Track what's been resolved.
3. When the answers stop moving the brief, stop. Don't pad.
4. **Sketch golden scenarios.** Turn the quality bar into 2-3 concrete examples — for each, a realistic
   *input* and the *properties a great output must have* (not a full transcript; the assertions that
   separate a great result from a mediocre one). These seed Build's `references/examples/` and become
   Verify's behavioral replay. For a trivial Lite skill one example is fine; note if none are warranted.
5. Write `grill.md`: the **refined brief** — the original sections, updated, plus a crisp **Exclusions**
   list, the **Quality bar** ("a great output has …; a bad one has …"), and the **Golden scenarios**. Note
   anything the user explicitly deferred. Update `forge.json` and tick relevant manifest items; resolve
   `[!VAGUE-TRIGGER]` if the trigger boundary is now sharp.

## Output template — `grill.md`

```markdown
# Refined Brief: <Display Name>

## Resolved in grilling
- <question> → <decision>
- …

## Exclusions (explicitly out of scope)
- …

## Failure modes & guards
- Failure: … → Guard: …

## Quality bar
- A great output: …
- A bad output: …

## Golden scenarios (seed Build's examples + Verify's replay)
1. Input: … → A great output asserts: …, …
2. …

## Updated triggers / I/O / wedge
<deltas from brief.md>

## Deferred (user chose not to decide now)
- …
```

## Anti-patterns to avoid

- **Question dumps.** One at a time. The whole value is that each question is informed by the last answer.
- **Asking what you can infer.** Don't ask the user things the brief already answers; ask what it doesn't.
- **Grilling forever.** When questions stop changing the brief, you're done. Diminishing returns are a
  signal, not a challenge.
- **Leaving the exclusion list empty.** Every skill needs a "what it deliberately doesn't do." Extract it.
- **Designing the skill.** No section layout, no prose drafting — that's Blueprint. Stay on *completeness*.

## Integration

- Reads: `brief.md`, `novelty.md`, `forge.json`.
- Writes: `.claude/_forge/<slug>/grill.md` (refined brief); updates `forge.json`.
- Next: `forge-3b-ideate` (Full; skipped if ideation is disabled), then `forge-3c-shape` → `forge-4-blueprint`.
  Lite route skips 3b/3c/4 and folds into Build.
