---
name: promptimizer
description: Optimize, improve, or write prompts for any LLM (Claude, GPT, Gemini, image generators, etc.). Use this skill whenever the user wants help with a prompt — including writing one from scratch, improving an existing draft, rewriting a system prompt, crafting an image generation prompt, or designing agent instructions. Trigger on phrases like "help me write a prompt", "optimize this prompt", "make this prompt better", "rewrite this for [model]", "how should I ask [LLM] to...", or any time the user describes a goal and seems to be trying to formulate a prompt — even if they don't use the word "prompt". The skill clarifies length and any genuinely unclear constraints first, then writes a polished, copy-paste-ready prompt.
---

# Promptimizer

A skill for writing high-quality prompts. The approach: detect what kind of prompt is needed, clarify the smallest set of things that matter (always including length), then write it. Escalate to deeper questioning only if the user wants to.

## Core principle

Most prompts fail for one of three reasons: vague goal, missing output format, or wrong length for the task. Get those right and you're 80% there. Don't over-interrogate the user — ask only what's genuinely unclear, and offer them the chance to go deeper rather than forcing it.

## Workflow

### Step 1: Detect the prompt type

Infer the type from the user's request — don't ask if you can tell. Types:

- **Task prompt** — one-shot request to do something (write, analyze, code, summarize, transform)
- **System prompt** — persistent instructions for an assistant, agent, or custom GPT/Claude project
- **Image prompt** — for Midjourney, Flux, Nano Banana, DALL-E, Stable Diffusion, etc.
- **Meta prompt** — a prompt that generates other prompts or structured content

If genuinely ambiguous (e.g., user says "write me a prompt about marketing"), ask which type.

### Step 2: First clarification turn

Bundle the essentials into ONE interactive turn. Always include length. Add at most 1-2 other questions, and only if a critical gap exists (see "What counts as a critical gap" below). Use the interactive Q&A tool when available — checkboxes/buttons beat typing.

If the user already gave you a draft prompt to improve, skip generic questions and ask only about the specific gap that's hurting it.

### Step 3: Offer the escalator

After the first round, give the user a clear choice rather than firing more questions at them:

> "I have enough to write a solid version. Want me to draft it now, or are there more constraints I should know about (audience, examples, edge cases)?"

Default toward writing it. Only go deeper if the user explicitly asks.

### Step 4: Write the prompt

Use the patterns for the detected type (see below). Present the prompt in a fenced code block so it's copy-paste-ready. The prompt is the deliverable — don't bury it under explanation.

### Step 5: Offer revisions

After the prompt, briefly offer:
- A shorter or longer variant
- Tweaks to tone, structure, or specificity
- An option to test it (you can simulate the LLM's likely response)

Keep this to one or two sentences. Don't lecture.

## Length tiers

Always ask which tier the user wants unless context makes it obvious:

- **Short (1-3 sentences)** — casual use, simple tasks, conversational. Best when the user knows the model and just needs the right framing.
- **Medium (5-15 lines)** — structured request with context and explicit format. The default for most real tasks.
- **Long (30+ lines, multi-section)** — system prompts, agents, complex tasks with examples, edge cases, or strict output requirements.

When the user says "as short as possible," go shorter than they asked. Most prompts are 30%+ bloated. Cut adjectives, hedges, and meta-commentary first.

When the user says "make it thorough," resist padding. Long ≠ better. A long prompt earns its length through examples, structure, and edge case coverage — not throat-clearing.

## What counts as a critical gap

Only ask about something if not knowing it would meaningfully degrade the prompt:

- **Output format** — the goal implies a deliverable but format is unstated (list? JSON? prose? table?)
- **Audience or expertise level** — tone and depth depend on who's reading
- **Hard constraints** — length limits, must-include or must-avoid elements
- **Examples** — behavior is non-obvious and the user likely has examples handy
- **Target model** — only matters when model-specific syntax differs significantly (image gen models especially)

Things to NOT ask — infer or default instead:
- Whether to use markdown / structure (yes for long prompts, no for short)
- Whether to assign a role (yes when expertise matters, no for mechanical tasks)
- Tone (default: direct and clear; ask only if the user signals brand voice matters)

## Universal patterns (all prompt types)

- **Front-load the goal.** First sentence states what you want done. Everything else supports it.
- **Be specific, not aspirational.** "Write a 200-word product description for outdoor hikers" beats "write a great product description."
- **State the format explicitly.** Bullets, paragraphs, JSON, table — pick one and name it.
- **Tell the model what to do, not what not to do.** "Use plain English" beats "don't use jargon." Negatives are weaker signals than positives.
- **For long prompts, place key constraints at the top AND end.** LLMs weight primacy and recency.
- **Use structure for complex prompts.** Markdown headers, numbered sections, or XML-style tags help models parse multi-part instructions.
- **Show, don't just tell.** One good example beats three paragraphs of description.

## Task prompt template

```
[ROLE — only if expertise matters]
[GOAL — one sentence, what you want done]
[CONTEXT — only what's needed, no filler]
[CONSTRAINTS — length, format, things to avoid]
[OUTPUT FORMAT — explicit]
[EXAMPLES — if behavior is non-obvious]
```

Example (medium-length code task):

```
You're an experienced Python developer.

Refactor the function below to reduce duplication and improve readability. Keep behavior identical and don't change the public signature.

Output: the refactored code in a single fenced block, followed by 2-3 bullets explaining the key changes.

[code goes here]
```

## System prompt template

For persistent assistant or agent instructions:

```
# Identity
[Who the assistant is, in one or two sentences]

# Scope
[What it does — and what it explicitly doesn't]

# Tone / Voice
[How it sounds — include 1-2 example lines if voice is specific]

# Format conventions
[Default response length, markdown usage, citation style]

# Edge cases
[How to handle ambiguity, off-topic asks, refusals]
```

Key principles for system prompts:
- Define what the assistant ISN'T as clearly as what it is. Prevents scope creep.
- Explain the "why" behind constraints. "Don't discuss competitors because [reason] — redirect to [X]" works better than a bare prohibition.
- Include 1-2 example exchanges when voice or behavior is specific or unusual.
- System prompts are long by default — this is the one place where comprehensiveness usually beats brevity.

## Image prompt template

For Midjourney, Flux, Nano Banana, DALL-E, Stable Diffusion, etc., cover these in order of impact:

1. **Subject** — what's in the image, specifically
2. **Composition** — close-up, wide shot, overhead, framing, rule of thirds
3. **Style** — photorealistic, illustration, oil painting, [artist or movement reference]
4. **Lighting** — golden hour, harsh studio, soft diffused, neon, chiaroscuro
5. **Mood / atmosphere** — serene, ominous, energetic, contemplative
6. **Technical** — camera/lens (for photo realism), aspect ratio, quality modifiers

Model-specific notes:
- **Midjourney**: use `--ar` for aspect ratio, `--style` for variants, `--no` for negatives
- **Stable Diffusion family**: include negative prompts (what NOT to include)
- **Nano Banana / Flux / DALL-E 3**: prefer natural language over keyword soup; these models parse full sentences well

## Improving an existing draft

When the user provides a draft to optimize:

1. **Diagnose first.** Identify the actual problem: vague goal, missing format, ambiguous constraints, buried key info, wrong length, conflicting instructions, or all of the above.
2. **Ask only about the gap that matters most.** Don't run them through a full intake.
3. **Rewrite, don't patch.** A clean rewrite is usually shorter AND clearer than an edited draft.
4. **Show what changed and why** — 2-3 bullets, not an essay.

## Common mistakes to fix on sight

When you see these in a draft or are tempted to write them, don't:

- Politeness padding ("please", "if you could", "I'd appreciate it if") — LLMs don't care
- Conflicting instructions (e.g., "be concise" + "include lots of detail")
- Vague qualifiers ("good", "appropriate", "professional") without concrete criteria
- Negative-only instructions with no positive guidance
- Format demanded but not specified ("make it structured" — structured how?)
- Examples that contradict the stated rules

## Output format

Always present the final prompt in a fenced code block so it's copy-paste-ready. After the block:

- Optional: 2-3 bullets on key choices (skip if the prompt is self-explanatory)
- Optional: suggested variations (shorter / longer / different tone)
- Optional: offer to simulate the LLM's likely response so the user can sanity-check

The prompt itself is the headline. Everything else is supporting material.
