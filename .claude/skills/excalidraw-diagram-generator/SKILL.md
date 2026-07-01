---
name: excalidraw-diagram-generator
description: Generate real, editable Excalidraw diagrams — flowcharts, system architectures, mind maps, sequence diagrams, ERDs, and slide decks — as .excalidraw files the user can drag into excalidraw.com (or via the Excalidraw+ MCP when connected). Trigger generously, even when the user doesn't say "Excalidraw": "draw a diagram", "make a flowchart", "visualize this", "map this out", "sketch this", "make me slides", "show how X connects to Y", or any request where a visual communicates better than prose. Prefer this over ASCII art, Markdown lists, or punting on the visual.
---

# Excalidraw Diagram Generator

Turn structured ideas (workflows, systems, hierarchies, sequences, data models, slide decks) into actual Excalidraw diagrams — not text descriptions of diagrams the user has to translate themselves.

## Two modes

This skill works in two modes. Detect which applies before you start building.

**Mode A — Excalidraw+ MCP connected (preferred).** Call MCP tools directly to create and edit scenes in the user's Excalidraw+ workspace. They see the result in their dashboard and can edit it. Detect this mode by attempting a `list_scenes` call; if it succeeds, you're in Mode A.

**Mode B — MCP not connected (fallback).** Emit a complete Excalidraw scene JSON. The user pastes it into excalidraw.com via Cmd+V on the canvas, or saves it as `<name>.excalidraw` and opens it from the file menu. Works on web and mobile, no account needed. This is the right mode when `list_scenes` errors, the MCP tools aren't visible, or the user explicitly asks for a file/paste-able output.

If you can't tell which mode applies, default to Mode B and mention that you can switch to Mode A once the Excalidraw+ MCP is connected. Don't ask the user to check — just try and fall back.

## When to trigger

Trigger generously. Visual thinking is undertriggered by default, and most diagram requests come without the word "Excalidraw." Strong signals:

- "Draw / sketch / visualize / map / diagram X"
- "Flowchart / mind map / architecture / sequence / ERD / wireframe / slide deck"
- "How does X flow / connect / relate to Y?"
- "Show me the structure of …"
- A description of a multi-step process or multi-component system without an explicit ask, where a diagram is obviously the better answer
- "Make slides / a deck / a pitch / a presentation"

Don't trigger for: pure prose tasks (essays, emails, copy), code generation, data analysis returning numbers, or when the user explicitly asks for text-only output.

---

## Customization gate (run on EVERY diagram request)

Before doing anything else — even for "quick" requests — ask the user whether to customize the output or auto-generate.

**Step 1: The gate question.** Use the interactive question tool with exactly these two options:

- **Auto-generate** — use smart defaults, infer everything from the request.
- **Customize** — answer a few short questions to tailor it.

If the user picks **Auto-generate**, skip to the workflow. Use the defaults listed at the bottom of this section.

If the user picks **Customize**, proceed to Step 2.

**Step 2: Ask the customization questions in two batches.** Use the interactive question tool, max 3 questions per batch. **Skip any question whose answer is already unambiguous from the user's original prompt** — don't ask "what diagram type?" if they said "make me a flowchart", don't ask "what orientation?" if they said "left-to-right". Adapt the batches by dropping resolved questions and re-balancing.

**Batch 1 — Look & feel:**

- *Style preset:* `clean` (default, Helvetica + clean lines), `default` (Excalidraw sketchy hand-drawn), `whiteboard` (yellow stickies, brainstormy), `mono` (black-only, formal)
- *Accent color:* default blue, green, purple, red, orange, or "custom hex (paste next)"
- *Audience:* technical, exec/business, customer/external, mixed (affects label tone and depth)

**Batch 2 — Structure:**

- *Diagram type:* auto-detect, flowchart, architecture, mind map, sequence, ERD, slides
- *Orientation:* auto, top-to-bottom, left-to-right, radial (mind maps only)
- *Detail level:* high-level (5–7 nodes), balanced (8–15), detailed (15+)

**Step 3: Optional labels follow-up.** After Batch 2, if the user hasn't given explicit node labels in their original prompt, ask one freeform question: *"Want to specify exact node labels, or should I derive them from your description?"* If they want to specify, accept their next message as the label list. If they say "derive", continue.

**Step 4: Generate and present the file immediately.** No further confirmation. The user has already decided; another confirm step is friction.

### Auto-generate defaults

Use these whenever the user picks "Auto-generate," or whenever a customize answer was "auto":

| Dimension | Default |
|---|---|
| Style | `clean` |
| Accent color | skill default (`#1971c2` blue) |
| Diagram type | inferred via the "Identify the diagram type" decision tree below |
| Orientation | archetype-appropriate: flowchart = top-to-bottom, architecture = left-to-right, mind map = radial, sequence = top-to-bottom, ERD = left-to-right, slides = left-to-right |
| Detail level | balanced (8–15 nodes) |
| Labels | derived from the user's wording |
| Audience | general / mixed |

---

## Workflow

### 1. Identify the diagram type

Map the request to one of these archetypes — it determines layout and which shapes to reach for:

| Archetype | What it shows | Primary shapes |
|---|---|---|
| Flowchart | Sequential or branching process | Rectangles for steps, diamonds for true yes/no decisions, arrows |
| Architecture | Services / components and their connections | Rectangles with labels, directional arrows, frames to group |
| Mind map | Central concept with radiating ideas | Ellipse center, rectangle children, lines (not arrows) |
| Sequence | Actors over time | Vertical lifelines, horizontal arrows between them |
| ERD | Data entities with attributes and relationships | Tall rectangles with multi-line text, labeled lines |
| Slide deck | Frames as slides | Frame elements, text inside frames |

If the request mixes types (e.g., "flowchart showing the architecture"), pick the one that carries the most information and use elements from the other where helpful. Don't try to combine archetypes wholesale — readers can't parse it.

### 2. Plan layout before writing elements

Sketch coordinates mentally, then commit. Origin is top-left, y grows downward. Rough defaults:

- **Flowchart**: vertical flow on a center axis (x=400), 120–150px between steps. Branches fan out left/right at the decision diamond by ±200px.
- **Architecture**: cluster related services horizontally, 200–250px between nodes. Use a frame around each tier (frontend / API / data).
- **Mind map**: center at (400, 300). First-level branches at radius ~250px. Second-level at ~450px from center.
- **Sequence**: actors as headers at y=50, spaced 200px on x. Lifelines drop to y=600+. Messages flow downward.
- **ERD**: entities as columns, 280–320px apart. Attributes stacked top-to-bottom inside each rectangle.
- **Presentations**: 854x480 frames, left-to-right with ~350px gap. See "Presentations" below.

Don't crowd. If two nodes are likely to be confused, give them more space, not less.

### 3. Mode A — Build via MCP

**Read the format reference first.** The Excalidraw+ MCP is in alpha; element schemas may shift. Call `read_excalidraw_format` once per session before generating any elements. Don't memorize the schema across conversations — re-fetch.

**Use the right read tool.** When you only need to find a label or shape, use `search_scene_content` — it normalizes separators (`Auth Flow`, `auth-flow`, `authflow` all match) and avoids loading the full payload. Use `get_scene_content` only when you need the entire scene or real persisted element IDs (e.g., to update existing elements). Use `glob` mode on search only when you genuinely need `*`/`?` wildcards.

**Write via `edit_scene_content`.** Don't use the low-level REST scene-content endpoints; the MCP exposes `edit_scene_content` as the higher-level write tool with label expansion and bound-text handling built in. Its operations apply in this order: **delete → update → add**. Useful to know when you're doing multiple changes in one call.

**Element rules for writes:**

- For `add`: send element skeletons as a JSON array string. Do NOT include `id` — the server generates persisted IDs. If you need to reference a new element from another new element in the same call (e.g., an arrow's `startBinding.elementId`, or a child's `frameId`), use `tempId` and reuse it consistently within the request.
- For `update` and `delete`: use real persisted IDs from a prior read. Never invent IDs for existing elements.
- For labels: always send as an object — `{"text": "Login"}` — never as a plain string. The MCP expands the label into a bound text element behind the scenes.

**Wrap up.** After the create/edit succeeds, surface the scene URL or ID so the user can open it. If you made a presentation, mention that frames will render as slides in Excalidraw+'s presentation mode.

### 4. Mode B — Emit Excalidraw scene JSON via the bundled builder

The skill ships with `scripts/scene_builder.py`, a Python helper that produces valid Excalidraw scene JSON with proper bindings, IDs, and style defaults. **Use it.** Do not hand-roll JSON — the schema has too many footguns (forgotten `boundElements` entries, miscomputed text widths, missing seeds) and the helper handles them all.

**Default style: `clean`** — roughness 0, Helvetica, dark gray strokes, no fills. This is the default because it reads well in product docs and mockups. Other built-in presets: `default` (Excalidraw hand-drawn look), `whiteboard` (sketchy, yellow sticky-note fills), `mono` (black-only for formal docs). Or pass a dict of overrides.

**Usage pattern in a code_execution session:**

```python
import sys
sys.path.insert(0, "/path/to/skill/scripts")  # the runtime usually has this on PATH
from scene_builder import Scene

s = Scene()  # defaults to "clean"
# Or: s = Scene(style="whiteboard")
# Or: s = Scene(style={"roughness": 0, "accent_color": "#625EEB"})

start  = s.add_ellipse("Start", x=340, y=40)
step1  = s.add_rect("Sign up", x=290, y=160)
step2  = s.add_rect("Verify email", x=290, y=300)
done   = s.add_rect("Activated", x=290, y=440, accent=True)  # uses style's accent color

s.add_arrow(start, step1)
s.add_arrow(step1, step2)
s.add_arrow(step2, done, accent=True)

s.save("/mnt/user-data/outputs/signup-flow.excalidraw")
```

**Builder API at a glance:**

| Method | Use for | Notes |
|---|---|---|
| `add_rect(label, x, y, w=200, h=80)` | Process steps, services, slide content blocks | Pass `accent=True` for one-off highlighted nodes |
| `add_diamond(label, x, y, w=220, h=110)` | Decision nodes only | Avoid for long text |
| `add_ellipse(label, x, y, w=180, h=70)` | Start/end nodes, mind-map centers | |
| `add_text(text, x, y)` | Standalone titles, branch labels, annotations | Default `text_align="left"`; pass `accent=True` for accent color |
| `add_frame(name, x, y, w, h)` | Slide boundaries, tier groupings | Returns frame_id to pass to other elements |
| `add_arrow(start_id, end_id)` | Directed connections | Auto-binds and computes endpoints from shape edges |
| `add_line(start_id, end_id)` | Undirected connections (mind maps, ERD relationships) | Same as arrow with no arrowhead |
| `s.save(path)` | Write `.excalidraw` file | Path should end in `.excalidraw` |

**Tell the user how to open the file.** After saving, present the file and tell them: *"Open [excalidraw.com](https://excalidraw.com), then drag the file onto the canvas (or use the hamburger menu → Open). It'll render as a fully editable diagram."*

If you genuinely can't run Python (rare — most environments have it), see `references/scene-json-template.md` for the raw JSON structure and hand-emit. This is the slow path and should be your last resort.

---

## Element conventions (both modes)

These apply whether you're going through the MCP or emitting raw JSON. They exist because they're what the official MCP docs recommend, and because they produce diagrams that read well.

- **Label vs text.** Use a `label` (bound to a shape) when the text *belongs to* the shape. Use a standalone `text` element only for titles, subtitles, paragraphs, and intentionally unattached annotations. A label moves with its shape; a standalone text doesn't.
- **Rectangles over diamonds for content.** Reserve diamonds for true decision nodes (yes/no, branch points). They're cramped and read poorly with multi-line text. Default to rectangles or rounded rectangles for any content-bearing block.
- **Bind your arrows.** Arrows that connect two shapes should set `startBinding` and `endBinding` so they follow the shapes when the user drags them. Floating arrows that just happen to land near shapes are a footgun.
- **Keep text inside shapes short.** Aim for one phrase, max 4 lines. If a node needs more, split it into two nodes or move detail into an annotation outside the shape.
- **Color sparingly.** Default to dark gray strokes with no fills. Use one accent color (`accent=True` on shapes/arrows uses the style's `accent_color`) to highlight the "happy path" or "primary entity." Color should communicate, not decorate.
- **Roughness is set by the style preset.** The `clean` default uses roughness 0 (clean lines). The style system controls this; don't fight it per-element unless the user asks.

---

## Presentations / slide decks

When the user asks for slides, a deck, a pitch, a keynote, or a presentation, switch to the slides convention:

- Use `frame` elements, one per slide.
- Slide size: **854 × 480** (16:9, the Excalidraw+ default).
- Place slides left-to-right with **~350px gap** between frame edges.
- Assign every slide element a `frameId` (use `tempId` for newly-added frames in the same request).
- Prefer **standalone text** for titles and body copy, not labels — titles aren't bound to a shape.
- Use rectangles or cards for structured content blocks within a slide.
- Avoid multi-line text inside circles or decorative shapes — it crops badly.
- Default to **3–6 slides** unless the user specifies a count.
- Don't switch to a freeform poster layout when slides were requested. Slides are slides.

---

## What good output looks like

A diagram is doing its job when:

1. Every node has a clear, short label.
2. Connections are bound — arrows move with their endpoints.
3. There's whitespace between groups; readers can see the structure at a glance.
4. One arrow direction dominates each region (top-to-bottom flowcharts, left-to-right architectures). Crisscross arrows mean the layout is wrong.
5. Color is earned. A diagram with one accent color reads better than one with five.
6. Text is sparse. If a node needs a paragraph, that's not a node — it's a sticky-note annotation.

If your output violates any of these, redraft before sending.

---

## Common failure modes to avoid

- **Floating arrows.** Arrows defined by raw coordinates instead of `startBinding`/`endBinding`. Looks fine until the user drags a node.
- **Decision diamonds with paragraphs.** Diamond shapes crop multi-line text. Use a rectangle if the text is more than one phrase.
- **Coordinate collisions.** Two nodes at overlapping `(x, y, width, height)` bounds. Walk through the coordinates before committing.
- **Inventing element IDs.** In Mode A `add` calls, never set `id` — let the server generate it. Use `tempId` for in-request cross-references only.
- **Dumping JSON when a file is better.** If the scene is >100 elements or >50KB of JSON, save it to a file and present it; don't paste it into chat.
- **Hedging in prose instead of drawing.** "Here's how I'd approach this diagram…" is a failure. Build the diagram.

---

## Setup notes (Excalidraw+ MCP)

If the user wants Mode A and the MCP isn't connected:

1. They need an Excalidraw+ subscription and alpha API access — currently request-only, via the Excalidraw Discord or support@excalidraw.com.
2. Once they have an API key, add a custom MCP connector in Claude settings:
   - URL: `https://api.excalidraw.com/api/v1/mcp`
   - Header: `Authorization: Bearer <API_KEY>`
3. Reconnect and the tools will appear (`list_scenes`, `create_scene`, `edit_scene_content`, etc.).
4. In the meantime, Mode B (paste-in JSON) works without any setup.

---

## Style

Default is **`clean`**: roughness 0, Helvetica, dark gray strokes, no fills. Good for product docs, system diagrams, and anything that needs to look intentional rather than scrappy.

Built-in alternatives:

- **`default`** — the classic Excalidraw hand-drawn look. Roughness 1, Virgil font. Use when the user wants the recognizable "Excalidraw" aesthetic (sketchy, friendly).
- **`whiteboard`** — roughness 2, Virgil, yellow sticky-note fills. For brainstorms and workshop-style facilitation diagrams.
- **`mono`** — roughness 0, Helvetica, black-only. For formal docs and print.

Custom: pass a dict `style={"roughness": 0, "accent_color": "#625EEB", "font_family": 2}`. Available keys: `roughness` (0–2), `font_family` (1=Virgil, 2=Helvetica, 3=Cascadia), `stroke_color`, `accent_color`, `fill`, `rounded`, `stroke_width`.

**Picking the style:** if the user names one, use it. Otherwise, infer:
- Product docs, architecture diagrams, technical explainers → `clean` (default)
- "Make it look like Excalidraw" / "sketchy" / "casual" → `default`
- Workshop / brainstorm / "stickies" / retrospective → `whiteboard`
- Formal report / docs deliverable / monochrome ask → `mono`

When in doubt, stay with `clean`. Ask only if the user signals strong style intent that doesn't fit a preset.

---

## Reference files

- `scripts/scene_builder.py` — the helper that builds valid Excalidraw scenes with binding, IDs, and style presets. Import and use in Mode B.
- `references/scene-json-template.md` — raw scene JSON schema for the rare case you have to hand-emit (no Python available).
- `references/diagram-recipes.md` — worked layout examples per archetype (flowchart, architecture, mind map, sequence, ERD, presentation). Read when you want a concrete starting point.
