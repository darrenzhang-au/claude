---
name: skill-forge
description: >
  Orchestrate the robust, multi-stage pipeline that turns a rough skill idea into a finished, genuinely
  unique and useful Claude Skill — and safely revise skills that already exist. This is the heavy-duty
  cousin of `01-stepify` (which is a quick one-shot): use skill-forge when an idea deserves real extraction,
  a novelty/dedup check, interrogation, a design blueprint, careful authoring, and adversarial verification
  before it goes live. Trigger when the user says things like "forge a skill", "skill-forge", "build me a
  new skill for X", "I have an idea for a skill", "run the skill pipeline", "turn this idea into a skill
  properly", "new skill from scratch", or — for the revise path — "update/upgrade/version this skill",
  "revise an existing skill", "add a capability to <skill>". This skill is the ROUTER and STATE-KEEPER: it
  builds a model of the existing skill library, decides which forge stages to run or skip, tracks progress
  in a per-skill `forge.json`, runs the pipeline interactively (gate between stages) or in auto mode
  (hands-off with a final review gate), and owns the install gate that promotes a verified draft into the
  live `.claude/skills/` directory. Do NOT use for a quick checklist/SOP/one-step skill (use `01-stepify`).
---

# Skill Forge — Pipeline Orchestrator

You are the decision-maker, router, and state-keeper for the Skill Forge pipeline: a compact-but-robust
assembly line that takes a rough skill idea and extracts a finished, genuinely unique and useful Claude
Skill — or safely evolves one that already exists. Your job is to model the library, look at the idea,
choose a route, run the stages in order (or skip the ones that add no value), keep an honest record in
`forge.json`, and never let a half-baked or duplicative skill go live without passing the gates.

The north star is in the user's own words: **genuinely unique and useful**. Every gate in this pipeline
exists to defend that. A skill that duplicates one the user already has, or that is so generic it could be
a one-line prompt, has failed — no matter how polished the prose.

## The pipeline

| # | Stage | Skill | Always? | Job |
|---|-------|-------|---------|-----|
| 1 | Extract | `forge-1-extract` | Always | Pull a structured **skill brief** out of the raw idea: identity, who/when, triggers, output, the unique wedge. |
| 2 | Novelty | `forge-2-novelty` | Always | Dedup against the **library model** + the wider ecosystem; score overlap; sharpen or kill the wedge. **Never skipped.** |
| 3 | Grill | `forge-3-grill` | Hard-gated | Socratic interrogation to extract the *complete* skill — edges, exclusions, failure modes, golden scenarios. |
| 3b | Ideate | `forge-3b-ideate` | Full only / opt-out | The creative-genius step: propose **3 sets of 4** additions the user didn't ask for, as an accept/reject menu. Pure proposal. |
| 3c | Shape | `forge-3c-shape` | Full only | Decide the skill's **structure** against the library: standalone, a stage in an existing pipeline, or its own new pipeline. |
| 4 | Blueprint | `forge-4-blueprint` | Always | Design the SKILL.md structure: sections, trigger phrasing, workflow, integrity rules, golden examples, assets. |
| 5 | Build | `forge-5-build` | Always | Author the actual SKILL.md (+ scripts/references + golden examples) into the draft folder. |
| 6 | Verify | `forge-6-verify` | Always | Trigger Arena (measured) + golden-example replay + adversarial critique + convention check. Owns the pre-install verdict. |
| — | Install | *(this orchestrator)* | Gate | Promote the verified draft into live `.claude/skills/`, update the library model, run library-wide regression. Explicit approval. |

Nine skills total (eight stages + this orchestrator). Far shorter than a feature pipeline, but each stage
is a real gate, not a rubber stamp. Ideate is the one purely *additive* stage — it never blocks and never
changes the skill on its own; it only offers options. Everything else either models, extracts, gates,
builds, or verifies.

## The Skill Library model (the substrate every stage reads)

Skill Forge is **library-aware**: stages don't re-scan `.claude/skills/` ad hoc — they read one shared
model of the library so dedup, structure decisions, and regression are all grounded in the same picture.

- **Builder:** `scripts/library_index.py` — a pure, mechanical parser. It scans the live skills directory
  and writes:
  - `.claude/_forge/library.json` — the machine model: per skill the slug, description, wedge (if known),
    `version`, `category`, declared `handoffs_to`/`expects_from`, a `looks_like_pipeline` hint, and an
    `integration_excerpt`. A **regenerable cache** — gitignored, never hand-edited.
  - `.claude/skills/INDEX.md` — the human-facing index, grouped by category (committed).
- **Similarity is LLM-judged, not embedding-based.** The script does no scoring. When a stage needs
  "nearest neighbors" or an overlap score, a sub-step reads the descriptions from `library.json` and judges
  overlap directly (0–100). This keeps the forge dependency-free; it's accurate at the current library size.
- **Handoff/dependency graph.** New skills declare `handoffs_to:` / `expects_from:` in frontmatter; for
  existing skills the edges are inferred once (from their `integration_excerpt`) and cached in the model.
  `forge-3c-shape` reads this graph to judge composition; Verify uses it to catch broken handoffs.
- **When it runs:** refresh the model at **intake** (run start); update it incrementally at **install**.
- **Backfill offer.** If the model reports `unversioned` skills (no `version:` frontmatter), mention it once
  and *offer* a one-time library-wide backfill run (stamp `version: 1.0.0` + seed a `CHANGELOG.md`). Never
  backfill silently or without approval — it edits live skills.

Run the builder with: `python3 .claude/skills/skill-forge/scripts/library_index.py` (no args needed).

## Two intents: create vs revise

Record `intent` in `forge.json`.

- **create** (default) — a new skill from a raw idea. Runs the full/lite pipeline below.
- **revise** — change an *already-installed* skill (add a capability, sharpen triggers, fix a bug, bump a
  version). Load the live `SKILL.md` (+ its `CHANGELOG.md` if present), run a **delta-focused** pass:
  Extract-the-change → Novelty *only if scope expands* → Grill the change → Blueprint/Build the edit into a
  fresh `draft/` → Verify with **regression** (re-run the prior version's Trigger Arena prompts + golden
  examples against the new draft; a regression blocks). Then the install gate handles versioning below.

Revising is a first-class path here — do **not** tell the user to "just edit it directly"; that loses the
novelty re-check, the regression net, and the version/changelog trail.

### Versioning, changelog, rollback (install-gate mechanics)

- **`version:` (semver) in frontmatter.** New skills start at `1.0.0`. On revise, classify the change and
  bump: **major** = breaking (trigger-surface shift that changes when it fires, removed/renamed script,
  changed I/O contract); **minor** = additive (new capability, more triggers); **patch** = fix/clarify.
- **`CHANGELOG.md`** in the skill folder — append an entry per install (`## vX.Y.Z — <real date>` + bulleted
  changes drafted from the diff). Get the real date at runtime (`date +%F`); don't guess.
- **Rollback snapshot.** Before overwriting a live skill on revise, copy the current live version to
  `.claude/_forge/<slug>/versions/<oldver>/`. If a regression surfaces after promotion, restore from there.

## Two modes

**Interactive (default).** Run one stage, show its output, recommend proceed/skip for the next stage with a
one-line reason, let the user confirm. This is the right mode when the idea is fuzzy or the user wants to
shape it as it forms.

**Auto.** Triggered by "auto", "hands-off", "just forge it", "run the whole thing and only ask me at the
end". Collect a short batch of up-front answers, then run every stage applying the gates below without
stopping, accepting each stage's recommended default and logging it to the **Decision Ledger** (see schema).
Stop hands-off only for the **hard stops** listed below. End at a single final gate where the user can flip
any logged decision and trigger a **selective re-run** of just the affected downstream stages, then approve
the install.

Auto-mode hard stops (the only things that break hands-off):
1. `[!DUPLICATE]` — Novelty found a near-identical existing skill and can't auto-differentiate.
2. `[!GENERIC]` — no defensible unique wedge survives; the skill may not be worth building.
3. `[!VERIFY-BLOCKER]` — Verify found a defect that survives one self-repair attempt.
4. A reframe signal — the idea is really a tweak to an existing skill, or three ideas wearing a trench coat.
   (Shape formalizes this: a `[!REFRAME]` from 3c — "this should be a stage in pipeline X" or "this is
   really a pipeline of N skills" — is a hard stop unless the user pre-authorized the restructure.)

## Routing: full vs lite

Pick the route at entry, state it, and record it in `forge.json`.

- **Full** (default for anything non-trivial): all stages — Extract → Novelty → Grill → Ideate → Shape →
  Blueprint → Build → Verify.
- **Lite** (trivial / mechanical skills — a single deterministic transform, no branching, no judgment, no
  assets): Extract → Novelty → Build → Verify. Grill, Ideate, Shape, and Blueprint fold into Extract/Build.
  Still never skip Novelty or Verify.

Lite hard-gate (auto-route to Lite, no need to ask): the idea is one deterministic step, has no decision
points, produces a fixed-format output, and needs no scripts/references. Anything touching judgment,
branching, external services, or multi-step workflow → Full.

If unsure, default to Full and tell the user they can downshift.

**Ideation opt-out.** Ideate (3b) is the one stage the user can turn off at intake. If the opening prompt
signals the idea is fixed — "the idea is strict / locked", "no extra ideas", "build exactly what I
described", "don't suggest additions" — set `ideationEnabled: false` in `forge.json` and skip 3b without
proposing. Absent that signal, `ideationEnabled` defaults to `true` for Full and `false` for Lite. The
opt-out only governs Ideate; it never disables a gate stage.

## Summary Sandwich (bracket every build with bullets)

Two lightweight bullet lists bracket construction — high-level only, never paragraphs:

- **Top slice — Objective recap.** Right *before* construction begins (after Shape, before Blueprint), emit
  a bulleted list of the skill's objective: what it's for, who/when it fires, the one-sentence wedge, and
  what it produces. Interactive → a confirm checkpoint ("building toward this — right?"). Auto → log it.
  Persist to `forge.json` (`summary.objective[]`).
- **Bottom slice — In practice.** After Verify, at the install gate, emit a bulleted list of what the
  finished skill does in practice: its triggers, key behaviors, output, and the main guards. Persist to
  `summary.inPractice[]`. This is part of the install summary the user approves.

## Hard gates vs soft judgment

These are the source of truth; every stage and the auto-runner inherit them. Record which gate fired in
each step's `gate` field.

- **forge-1-extract** — always. (No skill without a brief.)
- **forge-2-novelty** — always. Duplicating an existing skill is the #1 failure mode; this gate is
  non-negotiable and cannot be skipped in any mode or route. Reads the library model for overlap scoring.
- **forge-3-grill** — auto-proceed when ANY of: brief has ≥2 open questions; the trigger boundary is fuzzy
  (you can't crisply say when it should NOT fire); the unique wedge isn't yet one sharp sentence; complexity
  is medium+ (branching or judgment involved). Auto-skip only for genuinely trivial Lite skills.
- **forge-3b-ideate** — Full route only, and only when `ideationEnabled` is true. Auto-skip for Lite/trivial
  skills and whenever the user opted out at intake. When it does run it never blocks: it only proposes a
  menu, and acceptance is the user's. If the brief is already mature/tightly bounded, it may recommend
  skipping with a reason — surface that (interactive) or log it (auto).
- **forge-3c-shape** — Full route only; auto-skip for Lite/trivial. Always *suggests* a structure
  (standalone / join-existing-pipeline / new-pipeline) grounded in the library model. The structural choice
  is the user's (accept/reject, like Ideate). Auto-*implementation* of a multi-skill build or pipeline
  wiring is **never** automatic — it sits behind its own explicit gate (see Composition build gate below).
- **forge-4-blueprint** — always in Full; folded into Build for Lite. Must honor every idea accepted in 3b,
  the structure decided in 3c, ignore rejected ideas, and plan the golden examples + Trigger Arena bar.
- **forge-5-build** — always. Authors the golden examples and sets `version:` frontmatter.
- **forge-6-verify** — always. Runs the Trigger Arena (measured precision/recall) and replays golden
  examples. The multi-model **consensus** sub-step is conditional: run it for non-trivial or high-stakes
  skills, or on request; skip for trivial Lite skills.
- **Install** — never automatic. Always an explicit gate, in both modes. Promoting a draft makes it live
  and invocable — treat it as an outward action and confirm first. The install gate also updates the
  library model and runs library-wide regression.
- **Composition build gate** — if Shape's accepted decision is "join an existing pipeline" (which edits a
  live orchestrator) or "spin out a new pipeline" (which recursively forges N sub-skills), that build is a
  separate explicit gate beyond the normal install gate, because it touches/creates multiple live skills.

When no hard gate fires and a call is still needed, make a soft recommendation *with a reason* and let the
user decide (interactive) or log it to the ledger (auto). Never skip a stage silently.

## State & file conventions (source of truth)

**Library model (run-level, beside the staging area):**
```
.claude/_forge/library.json          # generated by library_index.py — cache, gitignored
.claude/skills/INDEX.md              # human-facing index — committed
```

**Working (staging) area — never a live skill:**
```
.claude/_forge/<skill-slug>/
  brief.md          # forge-1 output: the skill brief (+ §0 Coverage Manifest)
  novelty.md        # forge-2 output: nearest neighbors + overlap scores + the wedge + verdict
  grill.md          # forge-3 output: refined brief + golden scenarios (if run)
  ideation.md       # forge-3b output: the 3×4 idea menu + verdicts + integrated additions (if run)
  shape.md          # forge-3c output: structure decision + composition plan (if run)
  blueprint.md      # forge-4 output: the SKILL.md design
  verify.md         # forge-6 output: Trigger Arena scores + golden replay + verdict
  forge.json        # the state machine (schema below)
  versions/<ver>/   # rollback snapshots of a live skill (revise intent only)
  draft/
    SKILL.md        # forge-5 output: the actual skill, built + verified here
    scripts/        # optional, only if the skill needs them
    references/
      examples/     # golden examples (input + output-property assertions)
```

`.claude/_forge/` sits beside `skills/`, NOT inside it, and the draft SKILL.md is nested under `draft/`,
so an in-progress skill can never be discovered and accidentally invoked. Create the folder at runtime.

**Live area (after the install gate):**
```
.claude/skills/<skill-slug>/
  SKILL.md          (+ scripts/ references/ if present)
  CHANGELOG.md      # version history (created on first install, appended on revise)
```
Promotion is a copy of `draft/` → `.claude/skills/<slug>/`. The orchestrator deciding which slug/path is
fine; writing a *live* skill is the gated step.

### `forge.json` schema

```json
{
  "skillSlug": "kebab-case-name",
  "displayName": "Human Name",
  "intent": "create | revise",
  "route": "full | lite",
  "mode": "interactive | auto",
  "ideationEnabled": true,
  "version": "1.0.0",
  "draftPath": ".claude/_forge/<slug>/",
  "installedPath": null,
  "librarySnapshotAt": "ISO-8601",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601",
  "skillProfile": {
    "category": "generator | reviewer | router | research | automation | extractor | meta | other",
    "invocation": "on-demand | proactive | both",
    "producesArtifact": true,
    "needsScripts": false,
    "needsReferences": false,
    "externalDeps": [],
    "complexity": "trivial | small | medium | complex"
  },
  "summary": { "objective": [], "inPractice": [] },
  "shape": { "decision": "standalone | join | new-pipeline", "targetPipeline": null, "subSkills": [], "rationale": "" },
  "manifest": [
    { "item": "Sharp description with trigger phrases", "status": "todo | done | struck", "note": "" }
  ],
  "uniqueWedge": "One sentence: what this does that no existing skill does.",
  "steps": [
    {
      "skill": "forge-1-extract",
      "status": "complete | skipped | pending | in-progress | blocked",
      "gate": "always | hard-proceed:<rule> | hard-skip:<rule> | soft | manual",
      "runAt": "ISO-8601",
      "findings": {},
      "annotations": []
    }
  ],
  "decisions": [
    {
      "id": "D1",
      "step": "forge-1-extract",
      "decision": "Scoped triggers to X, excluded Y",
      "chosen": "X",
      "provenance": "user | default | maximize",
      "rationale": "...",
      "affects": ["brief.md", "consumed-by: blueprint, build"],
      "superseded": false
    }
  ],
  "blockers": [],
  "escalated": false
}
```

Stage-specific findings live in the relevant step's `findings`, e.g. Novelty records
`{ "collision": { "topNeighbors": [{"slug": "...", "score": 0–100}], "maxScore": N } }` and Verify records
`{ "arena": { "precision": 0.0, "recall": 0.0, "f1": 0.0, "misfires": [] }, "goldenExamples": { "passed": N, "total": N } }`.

The `decisions[]` ledger is the auto-mode contract: every default the runner takes is logged with
provenance and the downstream stages it affects, so the final gate can show all of them and a flipped
decision can drive a precise re-run.

### Coverage Manifest (§0 of `brief.md`)

A `- [ ]` checklist of everything the finished skill MUST contain. Verify enforces it: at the install
gate every line is `[x]` or `~~struck~~ — reason`; no bare `[ ]` may remain. Baseline items:

- [ ] `name` matches folder slug (kebab-case)
- [ ] `version:` set in frontmatter (semver)
- [ ] Sharp `description` with ≥3 natural trigger phrases AND a "do NOT use when" boundary
- [ ] Cleared the novelty gate (wedge stated; nearest neighbors + overlap scores listed)
- [ ] Structure decision recorded (standalone / join / new-pipeline) [Full only]
- [ ] "When to use" section
- [ ] Workflow / process steps (concrete, not abstract)
- [ ] Integrity rules / non-negotiables
- [ ] Output format defined
- [ ] Anti-patterns section
- [ ] ≥2 golden examples present and passing (else struck with reason for trivial Lite)
- [ ] Assets present if the skill needs them (else struck with reason)
- [ ] `handoffs_to:`/`expects_from:` declared if the skill composes (else struck)
- [ ] Passed forge-6-verify (Trigger Arena ≥ bar + golden replay + convention check)

Stages add skill-specific items as they go.

### Annotation & blocker vocabulary

Flags upstream stages raise for downstream stages to resolve. Blockers (★) must be resolved or explicitly
accepted with a written rationale before the install gate.

- `[!DUPLICATE]` ★ — a near-identical skill already exists. Resolve: differentiate, merge-into-existing, or kill.
- `[!GENERIC]` ★ — no defensible unique value; risks being a one-line prompt. Resolve: sharpen the wedge or kill.
- `[!VAGUE-TRIGGER]` — the description won't reliably fire (or fires too often). Resolve in Blueprint/Build.
- `[!OVERLAP]` — partial overlap with an existing skill; clarify the boundary in the description.
- `[!COLLISION]` ★ — the Trigger Arena or library-wide regression shows this skill steals a neighbor's
  prompts (or vice versa). Resolve: tighten boundaries on one side; re-run the arena.
- `[!REFRAME]` ★ — Shape found the idea is really a stage in an existing pipeline, or a whole pipeline of
  skills. Resolve: accept the restructure (Composition build gate) or consciously keep it standalone.
- `[!NEEDS-ASSET]` — the skill needs a script/reference to actually work; Build must produce it.
- `[!UNTESTED]` — a claim/behavior the skill asserts hasn't been checked. Verify must check it.
- `[!REGRESSION]` ★ — on revise, the new draft fails a prior-version arena prompt or golden example.
  Resolve: fix the regression or consciously accept it as an intended breaking change (→ major bump).
- `[!VERIFY-BLOCKER]` ★ — Verify found a defect that blocks install. One self-repair attempt, then escalate.

To clear a blocker, write `[!<FLAG>-RESOLVED]` (fixed) or `[!<FLAG>-ACCEPTED] — <rationale>` (deferred with
reason). No silent acceptance; every blocker leaves a paper trail.

## Workflow

### Interactive mode
0. **Model the library.** Run `library_index.py` to refresh `library.json` + `INDEX.md`. Note any
   `unversioned` skills and offer the backfill run (once, non-blocking). Set `librarySnapshotAt`.
1. **Intake.** Take the raw idea (or the target skill, for revise). Set `intent`. Derive a kebab-case
   `skillSlug`. Create `.claude/_forge/<slug>/` and an initial `forge.json` (status all `pending`). Pick the
   route (full/lite) and state it. For revise, load the live SKILL.md + CHANGELOG and snapshot it to
   `versions/<oldver>/`.
2. **Run stages in order.** Invoke each forge stage. After each, read its output, update `forge.json`
   (status, findings, annotations, gate), then recommend the next stage with a one-line reason. Honor hard
   gates automatically; surface soft calls for confirmation. Emit the **Objective recap** (Summary Sandwich
   top slice) before Blueprint.
3. **Resolve blockers** as they appear; never carry a ★ blocker past the install gate.
4. **Install gate.** When Verify passes: emit the **In-practice** bullets (bottom slice), show the final
   draft + manifest, set/confirm `version:`, then on explicit approval promote `draft/` →
   `.claude/skills/<slug>/`, write/append `CHANGELOG.md`, update the library model (`library_index.py`),
   run **library-wide regression** (re-check the new skill's nearest neighbors for trigger collisions), set
   `installedPath`, and introduce the skill (triggers + 2-3 first prompts to try).

### Auto mode
1. **Model + intake + up-front batch.** Refresh the library model. Same setup, plus ask the 3-4
   highest-leverage questions in one batch (the wedge, the trigger boundary, the output shape, any must-have
   asset). Capture whether ideation is wanted ("any directions to explore, or keep it strict?") and any
   structural preference for Shape.
2. **Run hands-off.** Drive all stages applying the gates verbatim, accepting each stage's recommended
   default, appending a ledger row per default with provenance `default` (or `user` where the batch answered
   it). Honor only the four hard stops. Ideate (3b) generates its 3×4 menu but default-**rejects** every
   idea; Shape (3c) records a recommended structure but never auto-builds a sub-pipeline. Log the Objective
   recap to `summary.objective`.
3. **Final gate.** Present: the built draft, the In-practice bullets, the manifest, and the full Decision
   Ledger — *including the ideation menu and the Shape recommendation* so the user sees what they could opt
   into. Let the user flip any row → re-enter at that row's `step` and re-run it + every downstream stage
   (mark superseded rows, append fresh ones; re-run Verify since inputs changed). Then the explicit install
   gate (and the Composition build gate, if Shape's decision was accepted).

## Anti-patterns to avoid

- **Skipping Novelty to move faster.** This is the gate that makes skills *worth having*. Never skip it.
- **Skipping the library refresh.** Stages that judge dedup/structure against a stale picture make bad calls.
  Refresh `library.json` at intake; update it at install.
- **Hand-editing `library.json`.** It's a regenerable cache. Fix the source skill and re-run the indexer.
- **Letting a `[!GENERIC]` skill through** because the prose reads well. A polished generic wrapper is still
  a generic wrapper — kill or sharpen it.
- **Auto-installing.** Promotion is always an explicit, confirmed step. A live skill changes future behavior.
- **Revising in place without the trail.** Never tell the user to "just edit the skill directly". Revise runs
  the regression net and writes a version bump + changelog + rollback snapshot.
- **Auto-building a sub-pipeline.** Shape may *recommend* spinning out a pipeline or wiring into one, but
  building multiple live skills is its own explicit gate — never a hands-off side effect.
- **Duplicating `01-stepify`.** If the idea is a quick checklist/SOP or a single mechanical step, hand it
  to `01-stepify` instead of spinning up the full forge.
- **Letting Ideate bloat the skill.** Every accepted idea must still serve the wedge; reject ones that dilute
  the core, and never include an idea the user didn't explicitly accept.
- **Silent defaults in auto mode.** Every default goes in the ledger; the final gate shows them all.
- **Writing the draft into `.claude/skills/`.** Always stage in `.claude/_forge/`; only the install gate
  writes live.
- **Re-running upstream stages on a flip.** Inputs above the entry point didn't change; re-running wastes
  work and can churn already-good output.

## Integration

- Upstream: a raw idea, a `01-stepify` output the user decided deserves the full treatment, or an existing
  skill to revise.
- Substrate: `scripts/library_index.py` → `library.json` + `INDEX.md`, refreshed at intake, updated at install.
- Each stage reads `forge.json` + the library model + the prior stage's artifact and writes its own; this
  orchestrator owns routing, the ledger, versioning, and the install + composition gates.
- Downstream: a live, versioned skill in `.claude/skills/<slug>/` (+ `CHANGELOG.md`), the updated library
  model, and a short introduction (triggers + first prompts).
