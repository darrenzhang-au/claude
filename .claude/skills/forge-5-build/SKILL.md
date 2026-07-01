---
name: forge-5-build
description: >
  Stage 5 of the Skill Forge pipeline. Author the actual SKILL.md (and any scripts/references the blueprint
  called for) into the draft folder, following the blueprint exactly and the house writing conventions.
  Produces the real, ready-to-verify skill — staged, never live. Trigger when `skill-forge` routes here, or
  when the user says "build the skill", "write the SKILL.md", "forge step 5", "author the skill from the
  blueprint". Reads `blueprint.md` (+ the briefs), writes `.claude/_forge/<slug>/draft/SKILL.md` and any
  asset files. Do NOT install/promote the draft (that's the orchestrator's install gate) and do NOT verify
  it here (that's `forge-6-verify`).
---

# Forge 5 — Build

You are the author. The blueprint told you the shape; you write the skill. Your output is a complete,
polished SKILL.md and any asset files, written into the **draft** folder only — nothing goes live from
here. Follow the blueprint; if you find a real gap in it, fix it and note the deviation rather than
silently improvising.

## Context loading

1. Read `blueprint.md` (the section plan, the description draft, the assets decision).
2. Read `grill.md`/`brief.md` for the substance — the quality bar, exclusions, failure modes — that fills
   the sections.
3. Read `forge.json` for the manifest you must satisfy and any open annotations to resolve.
4. Open one existing skill of the same category as a style reference so the voice matches the toolkit.

## Writing conventions (the house voice)

- **Frontmatter:** `name` (kebab, == folder slug), `version` (semver — the blueprint's value, `1.0.0` for a
  new skill), `description`, and — only if the skill composes with others — `handoffs_to:` / `expects_from:`.
  Use the blueprint's description; tighten it but keep the trigger phrases and the boundary clause intact.
- **Imperative, concrete prose.** "Check that X is non-empty and matches Y", not "validate the input".
  Every step should be executable by a fresh Claude with no extra context.
- **Trigger phrases in the description**, not just keywords — the skill must fire from natural language.
- **Integrity rules are non-negotiables**, stated as always/never. **Anti-patterns name the specific
  failure modes** this kind of skill falls into (pull them from the grill's failure-modes list).
- **Output format is concrete** — give a fenced template when the output is structured.
- **Length matches complexity.** A trivial skill is short; a complex one earns its length. Don't pad a
  simple skill to look serious, and don't compress a genuinely multi-step one into a stub.
- Match the register and section style of the existing `.claude/skills/` entries.

## Workflow

1. Create `.claude/_forge/<slug>/draft/`.
2. Write `draft/SKILL.md` section by section from the blueprint. Fill each section with real content from
   the briefs — don't leave any placeholder text.
3. If the blueprint specified assets, write them under `draft/scripts/` or `draft/references/`, and make
   sure the SKILL.md actually references and invokes them correctly (path, inputs, outputs). A script the
   skill never calls is a bug.
3b. **Write the golden examples.** From the blueprint's plan, write each to `draft/references/examples/`
   (`example-N.md`: the input, then the output-property assertions a great result must satisfy, + a 1-line
   why). These are the regression spec Verify replays — make the assertions concrete and checkable, not
   "output should be good". ≥2 for a Full skill (one is fine for trivial Lite; else strike with a reason).
4. Resolve every open annotation you can: confirm the description draws the `[!OVERLAP]` boundary, that
   `[!NEEDS-ASSET]` is satisfied, that triggers are sharp. Leave a note for anything Verify must check
   (e.g. `[!UNTESTED]` on a behavioral claim).
5. **Self-pass before handoff:** re-read the draft once against the §0 Coverage Manifest and tick every
   item you've satisfied in `forge.json`. Flag (don't hide) anything still `[ ]`.
6. Update `forge.json` (mark build complete, record asset paths in `skillProfile`, list deviations from
   the blueprint with reasons). Hand to Verify.

## Build checklist (apply before handing off)

- [ ] `name` == folder slug, kebab-case; `version:` set (semver)
- [ ] description leads with capability, has ≥3 natural trigger phrases, draws a boundary
- [ ] `handoffs_to:`/`expects_from:` declared if the skill composes (else omitted)
- [ ] ≥2 golden examples written to `references/examples/` (one for trivial Lite, or struck with reason)
- [ ] every section from the blueprint is present and filled with real content
- [ ] workflow steps are concrete and executable, not abstract
- [ ] integrity rules + anti-patterns are specific to this skill, not boilerplate
- [ ] output format is defined (template if structured)
- [ ] assets exist if specified, and the SKILL.md invokes them correctly
- [ ] no placeholder text, no TODOs, no leftover blueprint scaffolding
- [ ] manifest items ticked in `forge.json`; remaining `[ ]` flagged for Verify

## Anti-patterns to avoid

- **Writing live.** Author into `draft/` only. Promotion is the orchestrator's gated step.
- **Boilerplate sections.** Generic integrity rules and anti-patterns are filler. Make them specific to
  this skill or cut them.
- **Placeholder prose.** "Describe the workflow here" shipping in a draft is a failure. Fill it or flag it.
- **Improvising past the blueprint.** Small fixes are fine — note them. Re-scoping the skill is not; kick
  that back rather than quietly changing what was agreed.
- **Dead assets.** Don't create a script/reference the SKILL.md doesn't actually use.
- **Padding.** Don't inflate a simple skill with ceremony to look robust; clarity beats length.

## Integration

- Reads: `blueprint.md`, `grill.md`/`brief.md` (golden scenarios), `forge.json`, a category-matched existing skill.
- Writes: `.claude/_forge/<slug>/draft/SKILL.md` (+ assets + `references/examples/`); updates `forge.json`.
- Next: `forge-6-verify`.
