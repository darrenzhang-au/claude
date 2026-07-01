#!/usr/bin/env python3
"""
library_index.py — build the Skill Forge "Skill Library" model.

Pure, mechanical parser. Scans the live skills directory, extracts each skill's
frontmatter + a few structural fields, and emits:

  - library.json : the machine model (single source of truth for the forge run).
                   A regenerable CACHE — gitignored, never hand-edited.
  - INDEX.md     : the human-facing library index (grouped by category).

This script does NO judgment: no similarity scoring, no "is this a pipeline"
classification, no handoff inference. Those are agent-driven steps that READ
this model (forge-2-novelty does LLM-judged similarity, forge-3c-shape reads the
handoff graph, etc.). Keeping the script dumb keeps it fast and deterministic.

Usage:
    python3 library_index.py [--skills-dir DIR] [--out-json PATH] [--out-index PATH]

Defaults assume this file lives at .claude/skills/skill-forge/scripts/ and the
skills live at .claude/skills/.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

# Stages of the forge pipeline itself — flagged so the model knows which folders
# are the builder's own machinery vs. user skills.
FORGE_INTERNAL = {
    "skill-forge",
    "forge-1-extract", "forge-2-novelty", "forge-3-grill", "forge-3b-ideate",
    "forge-3c-shape", "forge-4-blueprint", "forge-5-build", "forge-6-verify",
}


def _default_paths():
    here = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.abspath(os.path.join(here, "..", ".."))      # .claude/skills
    forge_dir = os.path.abspath(os.path.join(skills_dir, "..", "_forge"))
    return (
        skills_dir,
        os.path.join(forge_dir, "library.json"),
        os.path.join(skills_dir, "INDEX.md"),
    )


def parse_frontmatter(text):
    """Return (frontmatter_dict, body) for a SKILL.md. Minimal YAML: scalars and
    simple `key: [a, b]` / `key:\n  - a` lists. Good enough for skill frontmatter;
    we are not a general YAML engine."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip("\n")
    body = text[end + 4:]
    fm = {}
    key = None
    buffer_list = None
    for line in raw.split("\n"):
        if not line.strip():
            continue
        # list item under the previous key
        m_item = re.match(r"^\s*-\s+(.*)$", line)
        if m_item and buffer_list is not None:
            buffer_list.append(m_item.group(1).strip().strip("\"'"))
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", line)
        if not m:
            # continuation of a folded scalar (e.g. multi-line description)
            if key is not None and buffer_list is None:
                fm[key] = (str(fm.get(key, "")).rstrip() + " " + line.strip()).strip()
            continue
        key = m.group(1)
        val = m.group(2).strip()
        if val in (">", "|", ">-", "|-"):          # folded/literal block scalar
            fm[key] = ""
            buffer_list = None
        elif val.startswith("[") and val.endswith("]"):   # inline list
            fm[key] = [v.strip().strip("\"'") for v in val[1:-1].split(",") if v.strip()]
            buffer_list = None
        elif val == "":                              # maybe a block list follows
            fm[key] = ""
            buffer_list = []
            fm[key] = buffer_list
        else:
            fm[key] = val.strip().strip("\"'")
            buffer_list = None
    # collapse empty list-buffers that never got items back to ""
    for k, v in list(fm.items()):
        if isinstance(v, list) and not v:
            fm[k] = ""
    return fm, body


def _section(body, *titles):
    """Return the text of the first matching `## <title>` section, else ''."""
    for title in titles:
        m = re.search(r"^#{1,3}\s+" + re.escape(title) + r"\s*$", body, re.M | re.I)
        if not m:
            continue
        start = m.end()
        nxt = re.search(r"^#{1,3}\s+\S", body[start:], re.M)
        return body[start: start + nxt.start()].strip() if nxt else body[start:].strip()
    return ""


def extract_skill(slug, skill_dir):
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm, body = parse_frontmatter(text)
    desc = fm.get("description", "")
    if isinstance(desc, list):
        desc = " ".join(desc)
    desc = re.sub(r"\s+", " ", desc).strip()

    has_scripts = os.path.isdir(os.path.join(skill_dir, "scripts"))
    has_refs = os.path.isdir(os.path.join(skill_dir, "references"))

    return {
        "slug": slug,
        "name": fm.get("name", slug),
        "description": desc,
        "version": fm.get("version", None),          # None => never versioned (backfill candidate)
        "category": fm.get("category", None),
        "handoffs_to": fm.get("handoffs_to", []) if isinstance(fm.get("handoffs_to", []), list) else [fm.get("handoffs_to")],
        "expects_from": fm.get("expects_from", []) if isinstance(fm.get("expects_from", []), list) else [fm.get("expects_from")],
        "is_forge_internal": slug in FORGE_INTERNAL,
        "has_scripts": has_scripts,
        "has_references": has_refs,
        # cheap heuristic flag for forge-3c-shape: does the skill read like an
        # orchestrator/pipeline (sequences other skills)? Confirmed by the agent, not trusted blindly.
        "looks_like_pipeline": bool(re.search(r"orchestrat|pipeline|stage \d|sub-?skill|routes? (to|through)|hand(s|off)", body, re.I)),
        "integration_excerpt": _section(body, "Integration", "Handoff", "Integration / handoff")[:600],
    }


def build_model(skills_dir):
    skills = []
    for slug in sorted(os.listdir(skills_dir)):
        d = os.path.join(skills_dir, slug)
        if not os.path.isdir(d):
            continue
        rec = extract_skill(slug, d)
        if rec:
            skills.append(rec)
    unversioned = [s["slug"] for s in skills if not s["is_forge_internal"] and not s["version"]]
    return {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "skillsDir": skills_dir,
        "count": len(skills),
        "unversioned": unversioned,            # backfill candidates (offer a run)
        "skills": skills,
    }


def render_index(model):
    lines = ["# Skill Library Index", "",
             f"_Generated {model['generatedAt']} · {model['count']} skills_  ",
             "_Auto-generated by skill-forge/scripts/library_index.py — do not edit by hand._", ""]
    by_cat = {}
    for s in model["skills"]:
        cat = s.get("category") or ("forge-internal" if s["is_forge_internal"] else "uncategorized")
        by_cat.setdefault(cat, []).append(s)
    for cat in sorted(by_cat):
        lines.append(f"## {cat}")
        lines.append("")
        for s in sorted(by_cat[cat], key=lambda x: x["slug"]):
            ver = f" `v{s['version']}`" if s["version"] else ""
            pipe = " · 🔗pipeline" if s["looks_like_pipeline"] else ""
            desc = s["description"]
            if len(desc) > 240:
                desc = desc[:237] + "…"
            lines.append(f"- **{s['slug']}**{ver}{pipe} — {desc}")
        lines.append("")
    return "\n".join(lines)


def main():
    sd, oj, oi = _default_paths()
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills-dir", default=sd)
    ap.add_argument("--out-json", default=oj)
    ap.add_argument("--out-index", default=oi)
    args = ap.parse_args()

    if not os.path.isdir(args.skills_dir):
        print(f"error: skills dir not found: {args.skills_dir}", file=sys.stderr)
        return 1

    model = build_model(args.skills_dir)
    os.makedirs(os.path.dirname(args.out_json), exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=2)
    with open(args.out_index, "w", encoding="utf-8") as f:
        f.write(render_index(model))

    msg = f"library model: {model['count']} skills → {args.out_json}"
    if model["unversioned"]:
        msg += f" · {len(model['unversioned'])} unversioned (backfill candidates)"
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
