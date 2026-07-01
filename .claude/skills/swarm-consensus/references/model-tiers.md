# Model Tiers Reference

Default model lists for swarm-consensus. Verified against OpenRouter as of May 2026 — IDs rotate, so refresh with `scripts/list_models.py` if calls start failing.

## Why diversity matters

A swarm is only useful if its members can disagree meaningfully. Five OpenAI models will agree with each other most of the time because they share training data, RLHF objectives, and architectural family. The defaults below intentionally mix labs (Anthropic, OpenAI, Google, xAI, DeepSeek, Meta, Mistral, Qwen) so disagreement signals something real.

When you add or replace a model, prefer one from an under-represented lab in the current list.

## Frontier tier

Use for high-stakes reasoning. Slower (often 15–40s) and more expensive (~$0.02–$0.10 per call, depending on prompt length).

| Model ID | Lab | Notes |
|---|---|---|
| `anthropic/claude-opus-4.7` | Anthropic | Strong all-around reasoning, careful with nuance |
| `openai/gpt-5` | OpenAI | Strong math and structured reasoning |
| `google/gemini-2.5-pro` | Google | Long context (1M+), multimodal-aware |
| `x-ai/grok-4` | xAI | Better current-events awareness than most |
| `deepseek/deepseek-r1` | DeepSeek | Reasoning-focused, sometimes verbose chain-of-thought |

## Cheap tier

Use for breadth, factual lookup, brainstorming. Fast (often 3–10s) and ~10–50x cheaper than frontier.

| Model ID | Lab | Notes |
|---|---|---|
| `anthropic/claude-haiku-4.5` | Anthropic | Fast, solid baseline reasoning |
| `openai/gpt-5-mini` | OpenAI | Cheap, broad knowledge |
| `google/gemini-2.5-flash` | Google | Very fast, long context |
| `deepseek/deepseek-chat` | DeepSeek | Excellent price/performance |
| `meta-llama/llama-4-maverick` | Meta | Open-weights perspective |
| `qwen/qwen3-72b-instruct` | Alibaba | Strong on Chinese context, decent general |
| `mistralai/mistral-large` | Mistral | European lab, different priors |
| `x-ai/grok-4-mini` | xAI | Cheap, current-events |

## Updating the lists

When a model in this list starts failing (HTTP 404, "model not found", etc.):

```bash
python scripts/list_models.py --filter <lab-name>
```

Find the current ID for that lab's equivalent model, then edit the lists at the top of `scripts/query_swarm.py`.

To browse the whole catalog:

```bash
python scripts/list_models.py | less
```

To find the cheapest models meeting some quality bar (for the cheap tier):

```bash
python scripts/list_models.py --top-cheap 30
```

## Picking custom models

Sometimes the tier defaults aren't right. Use `--models` to specify exactly:

```bash
python scripts/query_swarm.py \
    --models "anthropic/claude-opus-4.7,openai/gpt-5,google/gemini-2.5-pro" \
    --prompt "..."
```

Good cases for custom model lists:
- **Domain expertise**: pick models known to be strong in a specific domain (e.g. coding-focused for code review)
- **Cost ceiling**: pick three frontier models when the budget allows five but you want speed
- **Comparing siblings**: e.g. all reasoning models, or all open-weights models
- **Excluding a model that's been unreliable** lately

## Models to avoid in a swarm

- **Tiny models (<7B params)** — they tend to agree with stronger models trivially or hallucinate, adding noise not signal
- **Highly specialized models** (e.g. code-only, math-only) for general questions — they'll be over-confident outside their domain
- **Models from labs you've already represented** unless they bring a distinct capability (e.g. a reasoning variant)
