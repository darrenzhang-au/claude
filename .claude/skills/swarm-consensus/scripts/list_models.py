#!/usr/bin/env python3
"""List available OpenRouter models with pricing, sorted cheapest first.

Use this to refresh the default model lists in query_swarm.py when models
get deprecated or new ones become available.

Usage:
    python list_models.py                  # all models
    python list_models.py --filter opus    # only models matching 'opus'
    python list_models.py --top-cheap 20   # 20 cheapest models
"""

import argparse
import os
import sys

try:
    import httpx
except ImportError:
    print("ERROR: httpx not installed. Run: pip install httpx", file=sys.stderr)
    sys.exit(2)


def fmt_price(raw):
    try:
        per_mil = float(raw) * 1_000_000
        return f"${per_mil:.3f}"
    except (TypeError, ValueError):
        return "—"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--filter", default=None, help="Substring filter on model id")
    p.add_argument("--top-cheap", type=int, default=None, help="Show only the N cheapest")
    args = p.parse_args()

    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("ERROR: OPENROUTER_API_KEY not set", file=sys.stderr)
        sys.exit(2)

    r = httpx.get(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {key}"},
        timeout=30,
    )
    r.raise_for_status()
    models = r.json()["data"]

    if args.filter:
        models = [m for m in models if args.filter.lower() in m["id"].lower()]

    # Sort by prompt price ascending (free models first)
    def sort_key(m):
        try:
            return float(m.get("pricing", {}).get("prompt", 0) or 0)
        except (TypeError, ValueError):
            return float("inf")

    models.sort(key=sort_key)

    if args.top_cheap:
        models = models[: args.top_cheap]

    print(f"{'Model ID':<48} {'$/1M in':>10} {'$/1M out':>10} {'Context':>10}")
    print("-" * 82)
    for m in models:
        pricing = m.get("pricing", {}) or {}
        ctx = m.get("context_length") or "—"
        print(
            f"{m['id']:<48} "
            f"{fmt_price(pricing.get('prompt')):>10} "
            f"{fmt_price(pricing.get('completion')):>10} "
            f"{str(ctx):>10}"
        )
    print(f"\n{len(models)} models")


if __name__ == "__main__":
    main()
