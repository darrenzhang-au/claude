#!/usr/bin/env python3
"""Query multiple OpenRouter models in parallel and save responses as JSON.

Usage:
    python query_swarm.py --tier frontier --count 4 --prompt "Your question"
    python query_swarm.py --tier cheap --count 6 --prompt-file prompt.txt
    python query_swarm.py --models "openai/gpt-5,anthropic/claude-opus-4.7" --prompt "..."
"""

import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import httpx
except ImportError:
    print("ERROR: httpx not installed. Run: pip install httpx", file=sys.stderr)
    sys.exit(2)

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Default model tiers. Update via scripts/list_models.py output and edit here.
# Diversity across labs is intentional — a real swarm needs different families.
FRONTIER_MODELS = [
    "anthropic/claude-opus-4.7",
    "openai/gpt-5",
    "google/gemini-2.5-pro",
    "x-ai/grok-4",
    "deepseek/deepseek-r1",
]

CHEAP_MODELS = [
    "anthropic/claude-haiku-4.5",
    "openai/gpt-5-mini",
    "google/gemini-2.5-flash",
    "deepseek/deepseek-chat",
    "meta-llama/llama-4-maverick",
    "qwen/qwen3-72b-instruct",
    "mistralai/mistral-large",
    "x-ai/grok-4-mini",
]


async def query_one(client, model, prompt, system, temperature, max_tokens, timeout):
    """Query a single model and return a result dict (always succeeds, errors are captured)."""
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/anthropics/swarm-consensus",
        "X-Title": "Swarm Consensus Skill",
    }
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    t0 = time.time()
    try:
        r = await client.post(OPENROUTER_URL, headers=headers, json=payload, timeout=timeout)
        latency = round(time.time() - t0, 2)
        if r.status_code != 200:
            return {
                "model": model,
                "ok": False,
                "error": f"HTTP {r.status_code}: {r.text[:400]}",
                "latency_s": latency,
            }
        data = r.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return {
                "model": model,
                "ok": False,
                "error": f"Unexpected response shape: {json.dumps(data)[:400]}",
                "latency_s": latency,
            }
        usage = data.get("usage", {}) or {}
        return {
            "model": model,
            "ok": True,
            "response": content,
            "latency_s": latency,
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "total_tokens": usage.get("total_tokens"),
            # OpenRouter returns total cost in usage.cost on many models
            "cost_usd": usage.get("cost"),
        }
    except (httpx.TimeoutException, asyncio.TimeoutError):
        return {
            "model": model,
            "ok": False,
            "error": f"timeout after {timeout}s",
            "latency_s": round(time.time() - t0, 2),
        }
    except Exception as e:
        return {
            "model": model,
            "ok": False,
            "error": f"{type(e).__name__}: {e}",
            "latency_s": round(time.time() - t0, 2),
        }


async def run_swarm(models, prompt, system, temperature, max_tokens, timeout):
    async with httpx.AsyncClient() as client:
        tasks = [
            query_one(client, m, prompt, system, temperature, max_tokens, timeout)
            for m in models
        ]
        return await asyncio.gather(*tasks)


def select_models(tier, count, override):
    if override:
        return [m.strip() for m in override.split(",") if m.strip()]
    if tier == "frontier":
        pool = FRONTIER_MODELS
    elif tier == "cheap":
        pool = CHEAP_MODELS
    else:
        print(f"ERROR: --tier must be 'frontier' or 'cheap' (got {tier!r})", file=sys.stderr)
        sys.exit(2)
    if count > len(pool):
        print(
            f"WARN: requested {count} models from {tier} tier but pool has {len(pool)}. Using all.",
            file=sys.stderr,
        )
        return list(pool)
    return list(pool[:count])


def parse_args():
    p = argparse.ArgumentParser(description="Query multiple OpenRouter models in parallel.")
    p.add_argument("--prompt", help="Prompt sent to every model")
    p.add_argument("--prompt-file", help="Read prompt from a file (use for long prompts)")
    p.add_argument("--system", default=None, help="Optional system prompt sent to all models")
    p.add_argument("--tier", choices=["frontier", "cheap"], default=None)
    p.add_argument("--count", type=int, default=None, help="How many models from the tier")
    p.add_argument("--models", default=None, help="Comma-separated explicit model list (overrides --tier/--count)")
    p.add_argument("--temperature", type=float, default=0.7)
    p.add_argument("--max-tokens", type=int, default=2000)
    p.add_argument("--timeout", type=int, default=90, help="Per-model timeout in seconds")
    p.add_argument("--output", default=None, help="Output JSON path (default: runs/swarm-<timestamp>.json)")
    return p.parse_args()


def main():
    args = parse_args()

    if "OPENROUTER_API_KEY" not in os.environ:
        print(
            "ERROR: OPENROUTER_API_KEY not set.\n"
            "  Get a key at https://openrouter.ai/keys\n"
            "  Then: export OPENROUTER_API_KEY=\"sk-or-...\"",
            file=sys.stderr,
        )
        sys.exit(2)

    # Resolve prompt
    if args.prompt_file:
        prompt = Path(args.prompt_file).read_text()
    elif args.prompt:
        prompt = args.prompt
    else:
        print("ERROR: provide --prompt or --prompt-file", file=sys.stderr)
        sys.exit(2)

    # Resolve models
    if not args.models and not args.tier:
        print("ERROR: provide --tier or --models", file=sys.stderr)
        sys.exit(2)

    # Default counts per tier when not specified
    count = args.count
    if count is None and args.tier:
        count = 4 if args.tier == "frontier" else 6

    models = select_models(args.tier, count or 0, args.models)
    if not models:
        print("ERROR: no models selected", file=sys.stderr)
        sys.exit(2)

    # Output path
    script_dir = Path(__file__).resolve().parent
    if args.output:
        out_path = Path(args.output)
    else:
        runs_dir = script_dir / "runs"
        runs_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_path = runs_dir / f"swarm-{ts}.json"

    # Announce
    tier_label = args.tier or "custom"
    print(f"Querying {len(models)} models ({tier_label} tier)...", file=sys.stderr)
    for m in models:
        print(f"  - {m}", file=sys.stderr)

    # Run
    t0 = time.time()
    results = asyncio.run(
        run_swarm(models, prompt, args.system, args.temperature, args.max_tokens, args.timeout)
    )
    elapsed = round(time.time() - t0, 2)

    # Aggregate
    ok = [r for r in results if r["ok"]]
    failed = [r for r in results if not r["ok"]]
    total_cost = sum((r.get("cost_usd") or 0) for r in ok)
    total_tokens = sum((r.get("total_tokens") or 0) for r in ok)

    output = {
        "meta": {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "tier": tier_label,
            "models_requested": len(models),
            "models_succeeded": len(ok),
            "models_failed": len(failed),
            "wall_time_s": elapsed,
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(total_cost, 4) if total_cost else None,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
        },
        "prompt": prompt,
        "system": args.system,
        "responses": results,
    }

    out_path.write_text(json.dumps(output, indent=2))

    # Summary to stderr, path to stdout (so it's easy to capture)
    cost_str = f"~${total_cost:.4f}" if total_cost else "cost unknown"
    print(
        f"{len(ok)}/{len(models)} succeeded in {elapsed}s · {cost_str} · {total_tokens} tokens",
        file=sys.stderr,
    )
    if failed:
        print("Failures:", file=sys.stderr)
        for f in failed:
            print(f"  - {f['model']}: {f['error'][:150]}", file=sys.stderr)
    print(str(out_path))


if __name__ == "__main__":
    main()
