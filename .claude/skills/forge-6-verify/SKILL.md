---
name: forge-6-verify
description: >
  Stage 6 (final) of the Skill Forge pipeline. Adversarially verify a freshly built draft skill before it
  goes live — does it fire on the right prompts and stay quiet on the wrong ones, is it genuinely useful
  rather than a generic wrapper, does it follow house conventions, and would it actually work end-to-end.
  Runs a measured Trigger Arena (precision/recall on a labeled prompt set), a golden-example replay, a
  multi-lens critique (optionally a multi-model consensus for high-stakes skills), a revise-time regression
  check, and a Coverage-Manifest check, then returns a PASS / PASS-WITH-FIXES / BLOCK verdict to the gate.
  Trigger when `skill-forge` routes here, or when the user says "verify the skill", "review the draft skill",
  "forge step 6", "is this skill ready to install". Reads `.claude/_forge/<slug>/draft/SKILL.md` + the
  briefs, writes `.claude/_forge/<slug>/verify.md`. Owns the pre-install verdict but does NOT install
  (that's the orchestrator's gate).
---

# Forge 6 — Verify

You are the adversary and the final gate. Everything upstream tried to make this skill good; your job is to
try to prove it isn't — that it won't fire, fires too often, duplicates something, is generic, breaks on a
real call, or drifts from house conventions. Be a skeptic, not a cheerleader. A skill that sails through a
soft review and then misfires in practice is a worse outcome than one you sent back.

Default to **doubt**. Only return PASS when the draft survives the checks below.

## Context loading

1. Read `.claude/_forge/<slug>/draft/SKILL.md` and any draft assets (including `draft/references/examples/`).
2. Read `forge.json` (the §0 Coverage Manifest, the wedge, open annotations, `findings.collision` from
   Novelty) and `novelty.md` (so you can confirm the wedge actually shows up in the built skill).
3. Read the **library model** (`.claude/_forge/library.json`) for the candidate's nearest neighbors — these
   are the skills the Trigger Arena pits it against. Don't re-scan `.claude/skills/` by hand.
4. **If `intent: revise`** — also read the prior version's snapshot in `.claude/_forge/<slug>/versions/<oldver>/`
   (its arena prompts + golden examples) so you can run the regression check below.

## The checks

### 1. Trigger Arena (the most important — measured, not vibes)
Build a **labeled prompt set** and measure, don't eyeball:
- **Should-fire (≥8)** — prompts that must fire this skill (cover its real trigger phrasings + paraphrases).
- **Near-miss / should-NOT-fire (≥8)** — adjacent prompts the boundary must reject.
- **Should-fire-a-neighbor (≥6)** — prompts that should fire one of the candidate's nearest neighbors (from
  the library model / Novelty's `findings.collision`), NOT this skill.
- **Ambiguous (≥4)** — genuinely borderline; record which skill *should* win and why.

Then run the arena: a **router sub-step** is given ONLY the descriptions (the candidate + its neighbors) and,
for each prompt, must answer which skill fires (or none) — no peeking at the workflow body. Compare against
the labels → a **confusion matrix** and **precision / recall / F1** for the candidate. Record the scores +
any misfires into `forge.json` (`findings.arena`).

**Bar:** recall on should-fire ≥ ~0.8 AND zero (ideally) fires on the should-fire-a-neighbor / near-miss
sets. Misfiring on a neighbor is a `[!COLLISION]`; weak recall is a `[!VAGUE-TRIGGER]`. A failure here is a
BLOCK — but make **one self-repair attempt**: rewrite the `description` (its trigger phrases / boundary
clause) to fix the specific misses, then re-run the arena once. If it still fails, escalate with the matrix.

### 1b. Golden-example replay (behavioral, not just trigger)
For each golden example in `draft/references/examples/`: take its input, **mentally execute the skill's
workflow on it**, and check the output satisfies the example's stated assertions (the quality-bar
properties). A trigger that fires but produces a bad output is still a failure. Record pass/total into
`findings.goldenExamples`. A failed golden example is a `[!VERIFY-BLOCKER]` (one self-repair attempt). Skip
only if the manifest's golden-examples item was struck-with-reason (trivial Lite).

### 2. Usefulness / non-generic check
Re-run the novelty question against the *built* skill, not the brief: would a competent person, handed this
prompt and no skill, basically do this anyway? If the SKILL.md is just "do the obvious thing", it earns a
`[!GENERIC]` even if it passed stage 2 — building can dilute a wedge. Confirm the unique wedge from
`novelty.md` is actually expressed in the workflow/output, not just claimed in the description.

### 3. Convention & completeness check
- Frontmatter: `name` == folder slug, kebab-case; description has trigger phrases + boundary.
- All promised sections present, filled, concrete (no placeholders/TODOs).
- Integrity rules and anti-patterns are skill-specific, not boilerplate.
- Output format is defined; assets (if any) exist and are actually invoked by the SKILL.md.
- Voice matches the toolkit.

### 4. Would-it-work (dry run)
Mentally execute the workflow on one realistic input. Does each step have what it needs? Does it produce
the promised output? Any step that assumes context it doesn't load, or references a tool/file that isn't
there → `[!UNTESTED]` resolved to a concrete finding. If the skill ships a script, sanity-check its logic
against its stated inputs/outputs.

### 4b. Regression (revise intent only)
If `intent: revise`, run the **prior version's** Trigger Arena prompts and golden examples (from
`versions/<oldver>/`) against the *new* draft. Anything that passed before and fails now is a
`[!REGRESSION]` ★ — either fix it, or, if the change is an intended break, the user must consciously accept
it (which forces a **major** version bump at the install gate). Silent regressions never pass.

### 5. Coverage Manifest
Every §0 item must be `[x]` or `~~struck~~ — reason`. Any bare `[ ]` blocks the install gate. This now
includes: `version:` set, ≥2 golden examples passing (or struck), Trigger Arena ≥ bar, and the structure
decision recorded (Full route).

### Optional — multi-model consensus
For non-trivial or high-stakes skills (or on request), get independent perspectives before the verdict:
spawn a few parallel adversarial reviewers, each with a distinct lens (trigger-accuracy, genuine-usefulness,
convention-fidelity, would-it-break), and treat a finding as real if a majority raise it. Skip for trivial
Lite skills. (Self-contained: do this with your own sub-reviews; if the user has a consensus/council skill
and asks for it, you may use that instead — but don't depend on it.)

## Verdict

- **PASS** — survives all checks; manifest clean. Recommend the install gate.
- **PASS-WITH-FIXES** — minor issues you can fix in place (tighten a trigger phrase, fill a thin section).
  Apply the fixes to the draft, re-check, then PASS. Log what you changed.
- **BLOCK** ★ — a `[!VERIFY-BLOCKER]`: a trigger that won't fire / over-fires badly, a `[!GENERIC]` skill,
  a broken workflow or dead asset, or unresolved manifest items. Make **one** self-repair attempt; if it
  survives, escalate to the user with the specific defect and a recommended fix. Never wave a blocker
  through to install.

Write `verify.md` (template below), update `forge.json` (verdict, findings, manifest final state, resolve
or raise annotations), and hand the verdict to the orchestrator's install gate.

## Output template — `verify.md`

```markdown
# Verify Report: <Display Name>

## Trigger Arena
Set sizes: should-fire N · near-miss N · neighbor N · ambiguous N
| Prompt | Label (expected) | Router fired | Hit? | Notes |
|--------|------------------|--------------|------|-------|
| … | this-skill | this-skill | ✓ | |
| … | none | this-skill | ✗ | over-fires |
| … | `<neighbor>` | `<neighbor>` | ✓ | boundary holds |
**Scores:** precision __ · recall __ · F1 __ · misfires: <list>  (bar: recall ≥0.8, 0 neighbor/near-miss fires)
Self-repair applied? <no | yes — description rewrite, re-ran arena>

## Golden-example replay
<example> → passed/failed (<which assertion>) · total: __/__

## Regression (revise only)
Prior-version arena + goldens against new draft: <clean | N regressions> 

## Usefulness
Wedge expressed in the build? <yes/no + where> | Generic risk: <none/…>

## Convention & completeness
- <pass items / issues>

## Would-it-work dry run
Input: … → produced: … | Gaps: …

## Coverage Manifest: <clean | N items open>

## Consensus (if run)
<lenses, majority findings>

## VERDICT: PASS | PASS-WITH-FIXES | BLOCK
<reasoning; fixes applied; any [!VERIFY-BLOCKER] + recommended fix>
```

## Anti-patterns to avoid

- **Cheerleading.** "Looks great, ship it" is not verification. Try to break it first.
- **Trusting the description over the toolkit.** A trigger phrase only "works" relative to every other
  skill's description. Always judge collisions against the real neighbors.
- **Passing on claimed novelty.** The wedge has to be *in the built skill*, not just asserted up top.
- **Waving manifest items through.** A bare `[ ]` is a block, not a footnote.
- **Endless repair loops.** One self-repair attempt; if the blocker survives, escalate — don't keep
  rewriting silently.
- **Installing.** You return a verdict. Promotion is the orchestrator's explicit, confirmed gate.

## Integration

- Reads: `draft/SKILL.md` (+ assets + `references/examples/`), `forge.json`, `novelty.md`, the library
  model (`.claude/_forge/library.json`), and (revise) the prior version snapshot in `versions/<oldver>/`.
- Writes: `.claude/_forge/<slug>/verify.md`; updates `forge.json` with the verdict + `findings.arena`,
  `findings.goldenExamples`.
- Next: back to `skill-forge` → the install gate (promote `draft/` → `.claude/skills/<slug>/` on approval),
  then a short introduction of the new skill (triggers + 2-3 first prompts to try).
