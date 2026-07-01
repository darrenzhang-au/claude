# Golden Example 3 — Thin-context guard & zero-to-one refusal

## Input A — thin context
> "Give me some ideas to improve my business."

### A great output asserts
- Does **NOT** emit a generic listicle ("improve your SEO, start a newsletter, run ads").
- Runs the **tight intake first** (what you sell · to whom · how you make money · main cost · goal) before
  generating anything.
- Only after the anchors are answered does it proceed into the lens divergence.

### A bad output (fails)
- A generic business-advice listicle with zero anchoring to the user's actual model.

## Input B — zero-to-one
> "I have an idea for a startup but haven't started anything yet — can you brainstorm and stress-test it?"

### A great output asserts
- **Recognizes there is no existing model** and declines gracefully: states that this skill enhances an
  *existing* business, not a blank slate.
- Offers a path forward: proceed once there's even a running pilot/first customers to anchor to, or redirect
  to plain idea brainstorming.
- Does **NOT** fabricate a "current model" and run the full pipeline on thin air.

## Why
These are the two guards that keep the skill honest: it refuses to be a generic advice generator, and it
refuses to pretend a non-existent business is an existing one. Both are integrity rules, so Verify must see
them hold.
