---
name: forge-4-blueprint
description: >
  Stage 4 of the Skill Forge pipeline. Turn a refined, de-duplicated skill brief into a concrete SKILL.md
  **design** — the section-by-section blueprint the build stage fills in. Decides the description and its
  trigger phrasing, the "when to use" / workflow / integrity-rules / output / anti-patterns sections, whether
  the skill needs scripts or reference files, and what each must contain. Trigger when `skill-forge` routes
  here, or when the user says "blueprint this skill", "design the SKILL.md", "forge step 4", "lay out the
  skill structure". Reads `brief.md`/`grill.md`, writes `.claude/_forge/<slug>/blueprint.md`. Do NOT write
  the final skill prose here (that's `forge-5-build`).
---

# Forge 4 — Blueprint

You are the architect. You have a complete brief; your job is to decide the *shape* of the skill before a
word of it is written — what sections it has, how the description is phrased so it fires correctly, what
goes in each section, and whether it needs supporting files. A good blueprint makes the build stage almost
mechanical. A skipped blueprint produces a skill that wanders.

## Context loading

1. Read `grill.md` if it exists (the refined brief), else `brief.md`. Read `novelty.md` for the wedge and
   any boundary the description must draw.
2. Read `ideation.md` if it exists. Treat every **accepted** idea as a requirement to design in (it carries
   a target section/asset note); ignore the rejected ones. Accepted ideas added manifest items — honor them
   in the section map.
3. Read `shape.md` if it exists. If the decision was **standalone**, design one skill as normal. If it was
   **join a pipeline** or **new pipeline**, you are designing one skill in that structure — honor the
   handoff contract (`handoffs_to`/`expects_from`) and design only this skill's slice, not the whole pipeline.
4. Read `forge.json` for the profile, manifest, and any open annotations.
5. Read 1-2 existing skills in `.claude/skills/` that are structurally closest to what you're building
   (e.g. a generator like `06-json-prompt-builder`, a reviewer, a router) to match house conventions.

## SKILL.md anatomy (the house standard)

Design every section deliberately. The baseline shape:

```
---
name: <kebab-slug, == folder name>
description: <trigger-rich; see rules below>
---

# <Display Name>
<one-sentence purpose>

## When to use
- <natural trigger phrase>           (3-6 of them)
- <and when NOT to use / boundary>

## Workflow            (or "Process" / numbered phases for multi-step skills)
1. <concrete step>
...

## Integrity rules     (the non-negotiables — what it must always/never do)
- ...

## Output format
<exactly what the result looks like; a template if the output is structured>

## Anti-patterns to avoid
- <the specific ways this kind of skill goes wrong>
```

Adapt, don't pad: a trivial Lite skill may collapse Workflow + Output; a complex skill may split Workflow
into phases and add an "Integration / handoff" section. Add sections the skill genuinely needs; don't ship
empty scaffolding.

## The description — the highest-leverage 1-3 sentences

The description is what makes the skill fire at the right time. Design it explicitly:
- **Lead with the capability**, then **embed 3+ natural trigger phrases** the way the user actually talks
  ("turn this into X", "make me a Y"), not bare keywords.
- **Draw the boundary**: include a "do NOT use when…" or "use <other skill> for…" clause so it doesn't
  over-trigger or collide with a neighbor (carry the boundary from novelty's `[!OVERLAP]`).
- **Name the output** if it produces a file/artifact.
- Match the register of the existing toolkit's descriptions (terse, trigger-forward).

## Assets decision

Decide — and justify — whether the skill needs:
- **scripts/** — only if it must execute deterministic logic (API calls, parsing, math) that prose can't
  reliably do. Specify language, inputs, outputs, and how the skill invokes it.
- **references/** — only if the skill needs a lookup table, schema, style guide, or examples too long to
  inline. Specify the file and its shape.
- Default to **none**. Most skills are self-contained prose. An asset that isn't load-bearing is debt.
  If the brief raised `[!NEEDS-ASSET]`, resolve it here to a concrete file spec or strike it with a reason.

## Workflow

1. Choose the section set (from the anatomy) that fits this skill's complexity. Justify any add/drop.
2. Draft the **description** to spec and the one-sentence purpose.
3. For each section, write a 1-3 line **spec of what it will contain** (not the final prose) — enough that
   build is fill-in-the-blanks. For Workflow, list the actual steps/phases.
4. Make the assets decision and spec any files.
5. **Plan the golden examples.** Carry the grill's golden scenarios into a concrete plan: which 2-3 examples
   Build will write to `references/examples/`, each as `{ input, output-property assertions }`. Note the
   **Trigger Arena expectation** for Verify: the should-fire phrasings and the nearest neighbor(s) the
   boundary must beat (from `novelty.md`'s `findings.collision`). Set the frontmatter `version:` — `1.0.0`
   for a new skill, or the bumped value for a revise.
6. Map each Coverage Manifest item to the section/asset that will satisfy it, so nothing is orphaned.
7. Write `blueprint.md`; update `forge.json` (`skillProfile.needsScripts/needsReferences`, manifest ticks
   for design-level items, resolve `[!VAGUE-TRIGGER]`/`[!NEEDS-ASSET]` as decided).

## Output template — `blueprint.md`

```markdown
# Blueprint: <Display Name> (`<slug>`)

## Frontmatter
- name: <slug>
- version: <1.0.0 | bumped value for revise>
- description (draft): "<trigger-rich description with boundary>"
- handoffs_to / expects_from: <none | the skills this composes with>

## Section plan
- # <Display Name> — purpose: "<one sentence>"
- ## When to use — phrases: …; boundary: …
- ## Workflow — steps: 1)… 2)… 3)…
- ## Integrity rules — …
- ## Output format — <inline | template; shape>
- ## Anti-patterns — the 4-6 failure modes to name
- <any extra section + why>

## Assets
- scripts/: <none | file + spec>
- references/: <none | file + spec>
- references/examples/: <2-3 golden examples — input + assertions each>

## Trigger Arena expectation (for Verify)
- should-fire phrasings: …
- nearest neighbor(s) the boundary must beat: `<slug>` (overlap __/100)

## Manifest → section map
- <manifest item> → <section that satisfies it>
```

## Anti-patterns to avoid

- **Scaffolding for its own sake.** Don't design sections the skill doesn't need just to look thorough.
- **A weak description.** If the description doesn't contain real trigger phrases and a boundary, the skill
  won't fire right — this is the single most common skill defect. Get it right here.
- **Inventing assets.** Scripts/references are debt unless load-bearing. Justify every one or drop it.
- **Writing the final prose.** Specs, not paragraphs. Build does the prose.
- **Orphaned manifest items.** Every coverage item must map to a section; if one doesn't, either add the
  section or strike the item with a reason.

## Integration

- Reads: `grill.md`/`brief.md`, `ideation.md` (accepted additions), `novelty.md`, `forge.json`, nearest
  existing skills (for convention).
- Writes: `.claude/_forge/<slug>/blueprint.md`; updates `forge.json`.
- Next: `forge-5-build`.
