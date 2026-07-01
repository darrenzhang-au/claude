---
name: steelman
description: Stress-test the user's position by finding the strongest possible counter-arguments — the ones an informed, fair-minded critic would actually make — and then judging which objections survive scrutiny, which break the position, and how to respond. Use this skill whenever the user explicitly asks to "steelman," "stress test," "red team," "poke holes in," "argue against," or "find the best case against" their idea, position, plan, or decision. Also use it when the user is clearly weighing a real decision or commitment with non-trivial stakes — career moves, major purchases, business strategy, public positions, hiring, big bets — even if they don't use the word "steelman," because the point of the skill is to surface the failure modes they can't see from inside their own position. Don't trigger on casual opinions, hypotheticals, or venting.
---

# Steelman

The user wants their position pressure-tested by the strongest version of the opposition, not the easiest version. They want to either commit with confidence or revise with clarity. The job is to find the objections an informed, charitable critic would actually advance — and then be honest about which ones matter.

## What a real steelman is (and isn't)

A real steelman is **fair**. That means:

- The strongest version of opposing views, given charitably
- Focused on load-bearing assumptions, not surface details
- Honest about which objections actually break the position vs. which are survivable
- A genuine attempt to find failure modes the user can't see from inside their own position

It is **not**:

- Devil's advocacy as performance — generating objections to look thorough
- A laundry list of every conceivable nitpick
- Manufactured controversy when the position is actually fine
- Strawmen dressed up in stronger clothing

If the position is genuinely strong, say so. False balance is worse than no analysis. The user is paying attention to whether the pressure is real, and the skill loses all value the moment it starts inventing objections to seem rigorous.

## Workflow

Move through these phases in order. Don't skip ahead, but scale the depth to the stakes — a quick gut-check on a small decision shouldn't get the same treatment as a major commitment.

### Phase 1: Lock down the position

Before red-teaming, get the position into a form sharp enough to attack. Fuzzy targets produce fuzzy objections. If anything is unclear, ask:

- **The claim**: What exactly is the user asserting or deciding?
- **The reasoning**: What's the load-bearing logic? What does this depend on being true?
- **The bet**: What outcome are they betting on? What's the actual decision?
- **The disconfirmer**: What evidence or argument would change their mind?

You don't need all four if the position is already clear. One or two clarifying questions is usually enough — over-questioning here is its own failure mode. If the user has handed you a well-formed position, restate it in one sentence and move on.

### Phase 2: Generate the dialectic — case for vs. case against, by angle

Build the analysis as a side-by-side dialectic. For each load-bearing angle on the position, give the **strongest case for** and the **strongest case against**. Both sides get full fairness — no strawmen on either side. The point is to let the user see the full landscape from inside the same view, not to argue one side.

**Pick 3–6 angles that are actually load-bearing for this position.** Don't force the full list. Common angles to consider:

- **Assumptions**: What does the position quietly depend on being true? Is that defensible vs. contested?
- **Evidence**: What concrete data supports the position vs. undermines it?
- **Base rates / track record**: How have similar positions or decisions fared? What does the reference class say?
- **Bottleneck / mechanism**: Does the position correctly identify what's binding? Could the same conclusion follow from a different mechanism?
- **Second-order effects**: What follows from being right? What's the opportunity cost?
- **Incentive analysis**: Who benefits if the position is right? Who if wrong? Is bias warping the framing?
- **Alternative framings**: Is the question itself well-posed, or does a reframing dissolve the position?
- **Execution / psychology / "boring" objection**: The unsexy practical concern (cost, complexity, founder wiring, who actually does the work). Often the most load-bearing — and the easiest to skip.

For each angle, generate the **best case for** in 2–4 bullets and the **best case against** in 2–4 bullets. The discipline: every bullet has to be one a smart, informed, charitable advocate for that side would actually advance. If you can't find a strong case for one side on a given angle, that's a signal the angle isn't actually contested — skip it or call it.

Then assign a **winner** per angle:
- **For**: case for the position is meaningfully stronger
- **Against**: case against is meaningfully stronger
- **Even**: genuinely contested, depends on facts the user has access to but you don't
- **Reframing**: this angle suggests the question is the wrong shape

Be honest about evens and reframings. A table where every angle goes the same way is suspect unless the position is genuinely lopsided.

### Phase 3: Aggregate verdict

After the dialectic table, integrate across angles into an overall verdict. This is the most important phase and the easiest to skip. Don't just tally for/against — weight by importance. A position that wins on 4 minor angles and loses on 1 critical angle is *losing*, not winning.

Three possible aggregate verdicts:

- **Position holds**: Wins on the load-bearing angles. The against cases are real concerns but survivable.
- **Position needs revision**: Loses on one or more load-bearing angles. State the specific revision that would address the losses.
- **Position doesn't hold**: Loses on the angles that matter most. The case against is stronger than the case for, and no easy revision saves it.

Be willing to land on any of these honestly. False balance (everything is "even") is just as suspect as false destruction (everything is "against"). The aggregate verdict should track the actual landscape, not seem balanced.

### Phase 4: Response and revision

Based on the aggregate verdict, give the user something actionable:

- **Position holds**: Identify the strongest against cases — those are what the user needs to be ready to defend if pushed. Sketch their best response.
- **Position needs revision**: Show the revised position. Don't just say "this fails on angle X" — articulate the better version of the position that survives.
- **Position doesn't hold**: Explain what to consider instead. The skill identifies failure modes; the user makes the call. But if there's a clearly stronger neighboring position, name it.

End with a one-paragraph bottom line that the user could screenshot. It should answer: does the position hold, need revision, or fail — and what's the next action?

## Output format

Use a single dialectic table — case for, case against, winner per angle — followed by an aggregate verdict and bottom line. Use `<br>` for line breaks inside cells (markdown tables don't support real bullets, but `<br>•` renders cleanly).

```
## The position
[1-2 sentence restatement so the user can confirm understanding]

## The dialectic

| Angle | Case for | Case against | Winner |
|-------|----------|--------------|--------|
| [Angle name] | • [Best pro point]<br>• [Best pro point]<br>• [Best pro point] | • [Best con point]<br>• [Best con point]<br>• [Best con point] | **For / Against / Even / Reframing** |
| ... | ... | ... | ... |

## Aggregate verdict
[Position holds / needs revision / doesn't hold — with the load-bearing angles named]

## What to do
[Concrete next step. If holds: what to be ready to defend. If revise: the revised position. If fails: the stronger neighboring position.]

## Bottom line
[One short paragraph — the screenshot-worthy summary.]
```

**Format notes:**
- Pick 3–6 angles. Skip angles that aren't load-bearing — don't pad to fill rows.
- Keep each side to 2–4 bullets. If you can't compress to 4, the case has filler.
- The Winner column must be honest — don't engineer balance. If 5/6 angles go "Against," the position is in trouble and the verdict should say so.
- "Even" is allowed when the angle genuinely depends on facts you don't have. Don't use it to dodge.
- If the analysis is substantial (say >600 words) or the user will likely refer back to it, offer to save as a `.md` file at the end.

## Handling pushback

After the verdict, the user will often push back on a specific objection — "I don't think that one holds because…" Engage with their response on the merits:

- If their rebuttal is sound, update the verdict honestly. Say so directly: "Fair — that objection doesn't survive your response. Updated verdict: …"
- If their rebuttal misses the point, explain why and hold the line. Don't reflexively concede just because they disagreed.
- If their rebuttal is partial — addresses some of the objection but not all — say which part survives.

The failure mode here is being agreeable. The user asked for fair pressure; capitulating under social pressure makes the whole exercise worthless.

## Common failure modes to avoid

- **Pedantic objections**: "Have you defined X precisely?" Almost always a waste unless the definition is actually load-bearing. Focus on what could change the decision.
- **Manufactured balance**: Inventing objections to seem thorough. If the position is strong, the report should be short. Three real objections beat six padded ones.
- **Caving under pushback**: Reflexively conceding when the user disagrees. Evaluate their response on the merits, not on the social pressure.
- **Generic objections**: "But what about unintended consequences?" applied to anything. Engage with the specific position, not the abstract class of decision.
- **Ignoring the boring objection**: The unsexy practical concern (cost, complexity, execution risk) is often the one that actually matters.
- **Devil's advocate theater**: Performing skepticism with rhetorical flourishes. The user wants signal, not show.
- **Confusing critique with prescription**: The skill identifies what could go wrong. It doesn't tell the user what to do. The verdict is the user's, informed by the analysis.

## The standard

When generating each objection, ask: would a smart, informed, charitable critic — someone who has thought about this domain seriously — actually raise this? If yes, include it. If no, leave it out. The user is trying to think more clearly, not collect counter-arguments.
