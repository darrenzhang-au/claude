# Golden Example 3 — Boundary / negative case (must redirect)

## Input
> "I run a SaaS doing $30k/mo on seat-based pricing. Should I add a usage-based tier?"

## A great output asserts
- **Declines to design a model and redirects** to `business-model-enhancer`, because a **working revenue model already exists** and the ask is an *enhancement* to it, not a design-from-scratch.
- The redirect is **explicit and reasoned** — names why (existing model + additive change), and names the correct skill — rather than silently answering the question.
- Does **NOT** run intake, diverge, or converge on a new model.

## A bad output has
- Designing a fresh business model over the top of the existing $30k/mo one.
- Answering "yes/no, add the tier" with a full pre-mortem as if it were zero-to-one.
- Ignoring that a model already exists.

**Why:** this is the `[!COLLISION]` guard from novelty — the single most important negative case. If the skill fires here, it steals `business-model-enhancer`'s prompts. It must stay quiet and redirect.
