---
name: forge-1-extract
description: >
  Stage 1 of the Skill Forge pipeline. Turn a raw, rough skill idea into a structured **skill brief** —
  the spec every later stage builds on. Extracts the skill's identity, who uses it and when, the natural
  trigger phrases, the output it produces, and a first draft of its unique wedge, plus a §0 Coverage
  Manifest of everything the finished skill must contain. Trigger when `skill-forge` routes here, or when
  the user says "extract this skill idea", "forge step 1", "what is this skill really", or hands over a
  vague idea to be shaped. Writes `.claude/_forge/<slug>/brief.md` and seeds `forge.json`. Do NOT design
  the SKILL.md structure here (that's `forge-4-blueprint`) and do NOT dedup here (that's `forge-2-novelty`).
---

# Forge 1 — Extract

You are the intake analyst for the Skill Forge pipeline. Your job is to pull a complete, structured brief
out of a rough idea — to name what the user is actually trying to build before anyone tries to build it.
You are not designing the skill yet and you are not writing prose for it. You are extracting *what it is*.

A good brief is the difference between a sharp, useful skill and a generic wrapper. Push past the surface
description until you can state the skill in one sentence and name what it does that nothing else does.

## Context loading

1. Read the raw idea the user gave (text, a transcript, a `01-stepify` output, a frustration they described).
2. List the existing skills in `.claude/skills/` (names + descriptions) so you have a rough sense of the
   neighborhood — you are NOT deduping here (that's stage 2), just orienting.
3. If `skill-forge` already created `forge.json`, read it. If not, you may be running standalone — create
   the working folder `.claude/_forge/<slug>/` and a minimal `forge.json` yourself.
4. **If `intent: revise`** (changing an installed skill, not creating one): read the live
   `.claude/skills/<slug>/SKILL.md` and its `CHANGELOG.md`. Extract the **change delta**, not a brief from
   scratch — what the revision adds/alters, what stays, and whether the change *expands the trigger surface
   or scope* (which decides whether Novelty must re-run). Carry the existing wedge/triggers forward; only
   re-derive the parts the change touches.

## Workflow

### Phase 0 — Name it
Derive a kebab-case `skillSlug` and a human display name. If the idea is too vague to name, ask one
clarifying question before proceeding — a skill you can't name is a skill you can't scope.

### Phase 1 — Extract the core
Fill these from the idea; mark anything you had to infer as an assumption (don't silently invent):

- **One-sentence purpose** — "This skill <verb> <object> so that <outcome>." If you can't write it in one
  sentence, the idea is still two ideas; flag it.
- **Category** — generator / reviewer / router / research / automation / extractor / meta / other.
- **Who invokes it** — the user on demand, Claude proactively, or both.
- **When it should fire** — the situations that should trigger it. Then the harder half:
- **When it should NOT fire** — the adjacent situations where it would be wrong to fire. (A skill with no
  "not" boundary will misfire; if you can't name one, raise `[!VAGUE-TRIGGER]` for downstream.)
- **Inputs** — what must exist before it runs.
- **Output** — what it produces, and in what shape (file? message? edits? a structured artifact?).
- **The unique wedge (first draft)** — one sentence: what this does that an existing skill, or a plain
  prompt, does not. This is provisional; stage 2 will pressure-test or kill it.

### Phase 2 — Trigger phrases
Draft 3-6 natural phrases a user would actually type that should fire this skill. Real phrasings, not
keywords. These feed the description later. If you can only think of one stilted phrase, the skill's
purpose is probably still fuzzy — note it.

### Phase 3 — Coverage Manifest (§0)
Write the §0 Coverage Manifest into the brief: the baseline checklist from the orchestrator, plus any
skill-specific items this idea implies (e.g. "needs a Python script to call the API", "needs a reference
table of valid formats"). Each as `- [ ]`. This is the coverage contract the pipeline ticks off and Verify
enforces at the install gate.

### Phase 4 — Write the brief & update state
Write `.claude/_forge/<slug>/brief.md` (template below). Update `forge.json`: set `skillProfile`, the
draft `uniqueWedge`, the `manifest`, and mark `forge-1-extract` complete with any annotations raised.
Hand back a 3-line summary and the recommended next stage (always Novelty).

## Output template — `brief.md`

```markdown
# Skill Brief: <Display Name>  (`<slug>`)

## §0 Coverage Manifest
- [ ] name matches folder slug
- [ ] sharp description with ≥3 trigger phrases + a "do NOT use when" boundary
- [ ] cleared novelty gate
- [ ] when-to-use section
- [ ] concrete workflow steps
- [ ] integrity rules
- [ ] output format defined
- [ ] anti-patterns section
- [ ] assets present if needed (else struck)
- [ ] passed forge-6-verify
<skill-specific items…>

## 1. Purpose
<one sentence>

## 2. Profile
- Category: …
- Invoked by: user / Claude / both
- Complexity: trivial / small / medium / complex
- External deps: …

## 3. Triggers
**Fires when:** …
**Does NOT fire when:** …
**Natural phrases:** "…", "…", "…"

## 4. Inputs → Output
- Inputs: …
- Output: <shape + where it goes>

## 5. Unique wedge (draft — to be tested in stage 2)
<one sentence>

## 6. Open questions / assumptions
- …
```

## Anti-patterns to avoid

- **Restating the idea instead of extracting it.** If the brief just paraphrases the user's sentence, you
  haven't done the work. Find the boundary, the output shape, the wedge.
- **Skipping the "does NOT fire" boundary.** It's the half that prevents misfires; never leave it blank.
- **Inventing scope.** Mark inferences as assumptions; don't quietly add features the user didn't ask for.
- **Designing the SKILL.md here.** Sections, prose, and templates belong to Blueprint/Build. Stay at "what".
- **Declaring the wedge final.** It's a draft; stage 2 decides if it survives.

## Integration

- Reads: the raw idea, the existing skill list (for orientation only).
- Writes: `.claude/_forge/<slug>/brief.md`; seeds `forge.json`.
- Next: `forge-2-novelty` — always.
