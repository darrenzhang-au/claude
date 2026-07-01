---
name: swarm-consensus
description: Query multiple AI models in parallel via OpenRouter and synthesize their responses into one answer with disagreement notes. Use this skill whenever the user wants to "swarm" a question, get a "consensus" or "second opinion" from multiple AIs, cross-check an answer against other models, validate an important decision, or pressure-test code, research, or creative work with diverse model perspectives. Trigger on phrases like "swarm this," "consensus," "ask multiple models," "what do other AIs think," "cross-check," "second opinion from other models," or any request to broaden a single-model answer into a multi-model verdict — even when the user doesn't explicitly say "swarm." Especially useful for high-stakes decisions, factual claims worth verifying, code reviews, and creative brainstorming where breadth of perspective matters.
---

# Swarm Consensus

Run a prompt against multiple AI models in parallel via OpenRouter, then synthesize their responses into one unified answer with brief notes on where they disagreed.

## The workflow

This is a four-step loop. Don't skip step 1 or step 4.

### 1. Assess complexity and suggest a tier

Read the user's prompt. Decide which tier and roughly how many models fit, using the heuristics below. Then **tell the user your suggestion and confirm before running.** Don't run silently — the user wanted a "suggest but confirm" flow.

**Frontier tier (3–5 expensive models)** — use when the prompt involves:
- Important decisions or strategic advice
- Subtle code architecture, debugging, or design tradeoffs
- Nuanced analysis, novel reasoning, math, or expert judgment
- Anything where a wrong answer would be costly

Default to **4 frontier models**. Use 5 only for unusually high-stakes or contested topics. Use 3 for faster turnaround when the question is narrower.

**Cheap tier (5–8 fast models)** — use when the prompt is:
- Factual lookup or verification
- Brainstorming, ideation, or creative breadth
- A quick gut-check on something low-stakes
- Cost-sensitive

Default to **6 cheap models**. Use 8 for broad brainstorms; 5 for tighter consensus.

**When unsure**, default to **frontier × 4** for anything analytical, decisional, or technical; **cheap × 6** for brainstorming or factual lookups.

Phrase the confirmation as a clear suggestion, e.g.:

> This looks like a strategic decision — I'd suggest the **frontier tier with 4 models** (~$0.10–0.30, ~20–40s). Sound good, or do you want to adjust the tier or count?

### 2. Verify setup

The script needs two things:

1. **`httpx` installed** — if missing, run `pip install httpx`
2. **`OPENROUTER_API_KEY` in the environment** — if unset, tell the user to:
   - Get a key at https://openrouter.ai/keys
   - Run `export OPENROUTER_API_KEY="sk-or-..."` (or add it to their shell config)

The script will exit with a clear error if either is missing.

### 3. Run the swarm

Call the script. It runs all models in parallel and saves results to a timestamped JSON file.

```bash
python scripts/query_swarm.py --tier frontier --count 4 --prompt "<the user's prompt>"
```

For long prompts (code, documents, multi-paragraph context), use `--prompt-file` instead of `--prompt`:

```bash
echo "<prompt>" > /tmp/swarm_prompt.txt
python scripts/query_swarm.py --tier frontier --count 4 --prompt-file /tmp/swarm_prompt.txt
```

Full flag list:
- `--tier` — `frontier` or `cheap` (required unless `--models` given)
- `--count` — how many models from the tier's pool (default 4 frontier, 6 cheap)
- `--models` — comma-separated explicit model list, overrides `--tier`/`--count`
- `--prompt` or `--prompt-file` — one is required
- `--system` — optional system prompt sent to all models
- `--temperature` — default 0.7
- `--max-tokens` — default 2000 per response
- `--timeout` — per-model timeout in seconds, default 90
- `--output` — output JSON path, default `runs/swarm-<timestamp>.json` next to the script

The script prints a one-line summary to stderr (e.g. `5/6 succeeded in 18.4s, ~$0.04`) and the JSON path to stdout. Read the JSON to synthesize.

### 4. Synthesize the output

After the script finishes, read the JSON and write a synthesis with this structure:

```
## Consensus answer
[The position the majority of models converged on, in your own words. Lead with this.]

## Where models disagreed
[Brief — 2–4 bullet points. Name which models took the minority view and what the substantive difference was. Skip this section if there was essentially no disagreement.]

## Unique angles worth flagging
[Optional. Any single model's insight the others missed but that seems valuable. Skip if nothing notable.]

## Swarm metadata
N/M models succeeded · ~$X.XX · ~Xs wall time
```

Keep it tight. Don't dump every model's full response in the synthesis — the JSON has that if the user asks. If a model failed or timed out, note it briefly in the metadata line.

If models split roughly 50/50 on a question, say so explicitly — don't fake a consensus.

## When *not* to use this skill

- Trivial questions a single model would nail (don't burn 6 API calls on "what's 2+2")
- Questions that depend on private user context the models can't see
- When the user just wants your own opinion, not a swarm

## Tips for better swarms

- For **yes/no questions**, add to the system prompt: "Start your response with 'Yes' or 'No', then justify." This makes disagreement visible at a glance.
- For **code review**, paste code in via `--prompt-file` and ask each model the same focused question (e.g. "Find bugs and security issues in this function").
- For **time-sensitive topics**, include the current date in the system prompt — model knowledge cutoffs vary widely.
- For **creative work**, raise temperature to 0.9–1.0 to get more divergent outputs worth synthesizing.

## Maintenance

Model IDs on OpenRouter rotate over time. If a model in the default tier list fails consistently:

```bash
python scripts/list_models.py | less
```

This prints the current OpenRouter catalog with pricing. Update the `FRONTIER_MODELS` and `CHEAP_MODELS` lists at the top of `scripts/query_swarm.py`.

See `references/model-tiers.md` for the current defaults and notes on picking good swarm members (diversity across labs matters — five OpenAI models isn't really a swarm).
