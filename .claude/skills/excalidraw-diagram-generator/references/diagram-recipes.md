# Diagram recipes

Short, concrete starting points for each archetype. These are layout patterns, not literal templates — adapt coordinates and labels to the actual content. The goal is to give you a solid first draft to iterate from, not a one-size-fits-all skeleton.

## Flowchart

**Layout:** Vertical center column, 120–150px between steps. Decision diamonds fan branches ±200px on x.

**Element pattern:**
- Start node: ellipse or pill-shaped rectangle (rounded), label "Start"
- Steps: rounded rectangles
- Decisions: diamonds, label as a yes/no question
- Branch labels: small standalone text near the arrow ("Yes", "No")
- End node: ellipse, label "Done" or describe end state

**Coordinate sketch for 4-step flow:**
```
Start         (400, 50)   200x60
↓
Step 1        (400, 170)  200x80
↓
Decision      (380, 310)  240x100   (diamond, yes/no question)
├─ Yes →  Step 2A   (180, 470)  200x80
└─ No  →  Step 2B   (620, 470)  200x80
              ↓
End           (400, 620)  200x60
```

**Color cue:** mark the "happy path" with one accent color on the arrows along it.

---

## System / architecture diagram

**Layout:** Cluster by tier. Frontend on top, API in middle, data on bottom — OR left-to-right by request flow. Frames around each tier.

**Element pattern:**
- Each service: rectangle with the service name as a label
- External actors (users, third-party APIs): rectangle with a different stroke color or dashed border
- Connections: arrows with short labels describing the call ("REST", "Webhook", "gRPC")
- Frames: light background, label as the tier name ("Frontend", "API", "Data")

**Coordinate sketch for a SaaS architecture:**
```
Frame: Frontend     (50, 50)    900x180
  Web App          (100, 100)   200x100
  Mobile App       (400, 100)   200x100
  Chrome Ext.      (700, 100)   200x100

Frame: API          (50, 280)   900x180
  REST API         (250, 330)   200x100
  Auth Service     (550, 330)   200x100

Frame: Data         (50, 510)   900x180
  Postgres         (200, 560)   200x100
  Redis            (450, 560)   200x100
  S3               (700, 560)   200x100
```

Arrows between tiers carry traffic-direction info. Don't draw every line — only the meaningful ones. A diagram where every service connects to every other service is a diagram that says nothing.

---

## Mind map

**Layout:** Center node at (450, 350). First-level branches at ~250px radius, evenly spaced around the circle. Second-level branches extend outward from their parent.

**Element pattern:**
- Center: ellipse, larger font, the core concept
- First-level: rectangles with one-word labels
- Second-level: smaller rectangles or just text
- Connections: lines (not arrows — mind maps aren't directional)

**Coordinate sketch for 4-branch mind map:**
```
Center "Topic"        (380, 320)  140x60   (ellipse)
North "Branch 1"      (380, 100)  140x50
East  "Branch 2"      (650, 320)  140x50
South "Branch 3"      (380, 540)  140x50
West  "Branch 4"      (110, 320)  140x50

Sub-branches sprout from each branch node, extending another ~150px
in the same radial direction.
```

Use lines, not arrows. Mind maps aren't process flows.

---

## Sequence diagram

**Layout:** Actors as headers along the top at y=50. Vertical lifelines drop down. Messages are horizontal arrows between lifelines. Time flows top-to-bottom.

**Element pattern:**
- Actor headers: rectangles at y=50, spaced 250–300px apart on x
- Lifelines: vertical dashed lines from each actor's bottom edge down to y=700+
- Activation bars: thin vertical rectangles on a lifeline during its active phase (optional)
- Messages: horizontal arrows between two lifelines, labeled with the call name
- Self-calls: small arrow loops on a single lifeline

**Coordinate sketch for 3-actor sequence:**
```
Actor A: User       (100, 50)   180x60
Actor B: API        (400, 50)   180x60
Actor C: Database   (700, 50)   180x60

Lifelines (dashed lines):
  A: from (190, 110) to (190, 700)
  B: from (490, 110) to (490, 700)
  C: from (790, 110) to (790, 700)

Messages (arrows):
  y=180: A → B    "POST /login"
  y=240: B → C    "SELECT user WHERE email=..."
  y=300: C → B    "user record"
  y=360: B → A    "200 + JWT"
```

**Color cue:** errors or async responses in a different stroke color.

---

## ERD (entity-relationship diagram)

**Layout:** Entities as tall rectangles, 280–320px apart horizontally. Relationships as labeled lines with crow's-foot or 1/N markers (or just labels — Excalidraw doesn't have native crow's foot, so a text label like "1:N" works).

**Element pattern:**
- Each entity: a rectangle with multi-line text — first line is the entity name (bold-ish, larger), then attributes one per line below
- Primary keys: prefix with "PK" or asterisk
- Foreign keys: prefix with "FK"
- Relationships: lines (not arrows) between entities, with a small text label near the midpoint

**Coordinate sketch for 3-entity model:**
```
Users          (100, 100)  220x200
  text:
    Users (PK: id)
    ─────────────
    name
    email
    created_at

Orders         (450, 100)  220x240
  text:
    Orders (PK: id)
    ─────────────
    FK: user_id
    total
    status
    created_at

Products       (800, 100)  220x200
  text:
    Products (PK: id)
    ─────────────
    name
    price
    stock

Relationships:
  Users  ── 1:N ──  Orders      (line + small "1:N" text)
  Orders ── N:M ──  Products    (via order_items, label as "via order_items")
```

Keep attribute lists short (5–6 max per entity). If an entity has more, summarize and link to a separate detail diagram.

---

## Presentation / slide deck

**Layout:** Frames in a horizontal row. Default size 854x480, ~350px gap between frames.

**Element pattern per slide:**
- Frame as the slide boundary, `roughness: 0`, named `Slide 1`, `Slide 2`, etc.
- Title: standalone text, fontSize 36, near top-center
- Body: standalone text or a small cluster of rectangles, vertically centered
- Don't stuff a slide. One idea per slide.

**Coordinate sketch for 4-slide deck:**
```
Slide 1: Title           (0, 0)       854x480
  Title text             (200, 180)   454x60    "Q4 Planning"
  Subtitle text          (250, 260)   354x40    "October 2025"

Slide 2: Agenda          (1204, 0)    854x480   (1204 = 854 + 350)
  Title                  (1304, 60)   654x50    "Agenda"
  Bullet 1               (1304, 180)  500x40    "1. Revenue review"
  Bullet 2               (1304, 240)  500x40    "2. Top initiatives"
  Bullet 3               (1304, 300)  500x40    "3. Hiring plan"
  Bullet 4               (1304, 360)  500x40    "4. Open questions"

Slide 3: Content         (2408, 0)    854x480
  ...

Slide 4: Closing         (3612, 0)    854x480
  ...
```

**Rules from the official docs:**
- Use `frame`, one per slide.
- 854x480, ~350px gap.
- Every element on a slide sets `frameId` to that slide's frame.
- Prefer standalone text for titles/body. Reserve labels for shape-bound text.
- 3–6 slides unless asked otherwise.
- Don't cram multi-line text into circles or decorative shapes.

---

## Picking the right archetype when the request is fuzzy

Sometimes the user says "draw the thing" and the right shape isn't obvious. Quick decision tree:

- Is it a process with steps that happen in order? → **Flowchart**
- Is it a set of components with named connections? → **Architecture**
- Is it a topic with sub-ideas radiating out? → **Mind map**
- Is it interactions between entities over time? → **Sequence**
- Is it entities with attributes and relationships? → **ERD**
- Is it content meant to be presented one screen at a time? → **Presentation**

If two fit, pick the one that captures the *most important* aspect of the answer and use elements from the other where they help. Don't try to be all six at once.
