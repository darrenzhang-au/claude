# Test ideas for the Excalidraw Diagram Generator

Real-world tests to run after installing the skill. Better than synthetic prompts — ListingView contexts will surface failure modes that "draw me a generic flowchart" won't.

## Tests that pressure the customization gate

**1. The tiny-request test.** Type: *"flowchart of how I publish a listing"* — short, casual, no context. Does the customize-vs-auto prompt feel necessary or annoying for something this small? Honest gut-check on the "always ask" decision. If it feels heavy, change the gate to "Only when vague" in SKILL.md (~30-second edit, one phrase).

**2. The over-specified test.** Type: *"top-to-bottom flowchart, clean style, 5 steps, accent purple, of the publish flow"* — every dimension specified. The gate should still trigger, but if you pick Customize, every question should auto-skip. Tests whether the "skip resolved questions" logic actually works.

## Tests that pressure diagram quality

**3. The architecture-sprawl test.** *"Diagram the full ListingView system — Next.js frontend, Express API, Postgres, Chrome extension, Framer marketing site, plus the Discord monitor bot and the AI listing builder service."* 7+ components, multiple tiers, future-state. Does it cluster sensibly or turn into spaghetti?

**4. The "explain to my mom" test.** Pick something technical (OAuth flow, webhook architecture, anything jargon-heavy) and pick **audience = customer/external**. Does the language actually shift, or does it ignore the audience flag and use jargon anyway? This is where most diagram tools fail.

**5. The "would I send this?" test.** Generate a real sponsorship deck — actual numbers, a real channel name (Cassiy Johnson, Hannah Gardner, someone in the Etsy creator space), specific dates. Open the file. Ask yourself: *would I send this?* If yes, the skill earned its keep.

## Tests that pressure the edges

**6. The wrong-archetype test.** Ask for *"a flowchart of how my data model works"* — but that's actually an ERD. Does the skill correct the archetype, or dumbly produce a flowchart of entity relationships (which would be bad)? Tests whether it has judgment about what you actually need vs. what you asked for.

**7. The iteration test.** Generate any diagram, then in the next message say: *"make it whiteboard style instead"* or *"add a step for X between Y and Z."* Does it regenerate cleanly, or lose context and start from scratch?

---

## If you only run two

- **#1 (tiny request)** — answers the friction question fastest, easy to react to. Easy revert path if it feels heavy.
- **#5 (real sponsorship deck)** — answers whether this skill is *actually useful* or just a fun build, because the output would be used for real.

Skip #2 unless #1 felt good. #6 and #7 are nice-to-haves for a v2 iteration.
