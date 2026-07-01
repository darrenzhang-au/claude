---
name: skills-sh-finder
description: Search skills.sh (the open Agent Skills directory) for existing community-built skills that match what the user is trying to do, then suggest the best matches with a one-line summary and a copy-paste install command. Use this PROACTIVELY at the start of any non-trivial task — building an integration, working with a specific framework/SaaS/API, automating a workflow, doing creative or design work, or anything the user might want to repeat later — so they don't accidentally reinvent something that already exists. Also use ON-DEMAND whenever the user mentions skills.sh, says things like "is there a skill for this," "find me a skill," "anything pre-built for X," "search skills.sh," or asks whether a community skill exists. Cast a wide net — surface anything plausibly related, not just exact matches. Do not trigger for trivial one-shot questions (e.g. "what's 2+2," "summarize this email") where a skill would never apply.
---

# Skills.sh Finder

Search the public skills.sh catalog for existing agent skills before building something from scratch. Skills.sh is the open community directory of reusable agent capabilities — at the time of writing it holds 90,000+ skills covering frameworks, SaaS integrations, design workflows, marketing, testing, and more.

The point of this skill is simple: **before you (or the user) write a new skill, prompt, or workflow from scratch, check whether someone has already built one.** Casting a wide net is the goal — false positives are cheap, missed matches are costly.

## When to activate

**Proactively** at the start of any task that meets at least one of these conditions:

- The user is starting something they might want to repeat (a workflow, a content series, a recurring report).
- The task involves a named tool, framework, SaaS product, or API (e.g. "build something with Supabase," "set up Stripe," "write a Next.js component").
- The task is in a domain with rich existing tooling (design, marketing, SEO, testing, agent workflows, deployment).
- The user says something that hints at building a skill or workflow ("I want to make a skill that...", "I keep doing X manually").

Search **silently and briefly** in these cases — one quick web_search, surface only if there's a good match, otherwise proceed with the actual work without making a fuss.

**On-demand** when the user explicitly invokes it — "search skills.sh," "is there a skill for this," "find me something pre-built," "anything on skills.sh," "any community skills for X."

**Do not activate** for trivial one-shot tasks, simple factual questions, casual conversation, or tasks where Claude can clearly handle it directly in one turn with no repeatable value.

## How to search

**Primary method: web_search with the `site:` operator.** This is the most reliable approach in claude.ai because it works without URL allowlist restrictions and returns rich descriptive snippets inline (often including the install command), so a single search is usually enough.

```
web_search: site:skills.sh <query>
```

Examples:
- `site:skills.sh seo audit`
- `site:skills.sh stripe payments`
- `site:skills.sh next.js auth`
- `site:skills.sh video editing`

**Query construction tips:**
- Use the domain noun, not the verb. "stripe payments" beats "set up payments."
- Include the framework/tool name when there is one. "next.js auth" beats "auth."
- Search the workflow noun for broad tasks. "seo audit," "design system," "react component."
- If the first query returns nothing useful, try a broader synonym before giving up.
- For wide-net searches, run 2-3 related queries (e.g. `site:skills.sh video editing` AND `site:skills.sh ai video`) rather than one super-broad one.

**Alternate method: REST API.** Skills.sh exposes `GET https://skills.sh/api/v1/skills/search?q=<query>&limit=10` returning JSON. In claude.ai, `web_fetch` may refuse this URL unless it has appeared in prior context — so prefer `web_search` first. The API is most useful when:
- You need structured data programmatically (an artifact, a script).
- You need to fetch the full SKILL.md contents: `GET /api/v1/skills/{source}/{skill}`.
- You need security audit data: `GET /api/v1/skills/audit/{source}/{skill}`.

**Filtering rules:**
- Skip results where the URL or snippet indicates the skill is a duplicate/fork of another.
- Skills from `anthropics/*`, `vercel-labs/*`, `supabase/*`, `firebase/*`, `microsoft/*`, and other first-party publishers are higher trust — flag them as "official" when relevant.
- A skill in the search results doesn't always have visible install counts in the snippet — that's fine, don't fabricate numbers. Just omit the count if you don't see one.

## How to present results

Surface 3-5 matches by default, more if the user asked for a wide net or many matches exist. Cast a wide enough net that adjacent skills (not just exact matches) appear — the user explicitly prefers breadth over precision here.

**Format each suggestion as a short block:**

```
**[Skill Name]** — `owner/repo` [· official, if applicable]
[One-sentence plain-language description of what it does and when it'd help, synthesized from the search snippet. Make it concrete to the task at hand — don't just copy the listing's first line.]
🔗 https://skills.sh/owner/repo/skill-slug
📦 `npx skills add owner/repo/skill-slug`
```

Notes on the format:
- The description sentence is *your* synthesis, not a verbatim quote — make it useful for the user's specific task.
- For the install command, prefer the specific skill path (`owner/repo/skill-slug`) over the whole repo (`owner/repo`) so the user doesn't install dozens of unrelated skills from a multi-skill repo.
- If multiple skills come from the same source repo (e.g. `obra/superpowers`, `coreyhaines31/marketingskills`), group them visually under one heading.
- Order results by **relevance to the task**, not by install count. Install count is a tiebreaker, not the primary sort.

If the search returns nothing useful, say so directly. Then offer to either (a) help build a custom skill, or (b) try a different search query the user suggests.

## Proactive mode — keep it light

When firing proactively (not because the user asked), be brief and non-blocking:

> Quick heads up before I dive in — I checked skills.sh and there are a few existing skills that might save you time on this: [...] Want to pause and look at any of them, or should I just continue with the task?

If proactive search returns nothing useful, **don't mention you searched** — just do the task. No need to narrate dead-ends.

## Optional: pulling skill details

If the user wants to see what a skill actually does before installing, fetch the full skill contents:

```
GET https://skills.sh/api/v1/skills/<owner>/<repo>/<skill-slug>
```

This returns the SKILL.md and any bundled files as JSON. Summarize the SKILL.md description and key instructions for the user in plain language — don't dump the raw file unless asked.

## Optional: security audit check

For skills the user is about to install, especially from less-known publishers, fetch the audit results:

```
GET https://skills.sh/api/v1/skills/audit/<owner>/<repo>/<skill-slug>
```

If status is `warn` or `fail` for any audit partner, surface that clearly before recommending install. If it's a 404, the skill simply hasn't been audited yet — that's not a red flag on its own, just worth mentioning for unknown publishers.

## Installation context

In claude.ai (this environment), skills are not installed via `npx` — that command is for code-environment agents like Claude Code, Cursor, etc. For claude.ai users, the install command is informational: they'd add the skill manually via their Claude settings or use it from the source repo. Still surface the `npx` command since it's the canonical reference, but if asked "how do I actually install this in claude.ai," explain that they need to copy the SKILL.md content into a skill via Claude's UI, or point them to the source GitHub repo.

## Examples

**Good proactive trigger:**
> User: "Help me build a marketing landing page in Next.js"
> Action: Search `next.js landing page` and `marketing landing page` quietly. If `vercel-labs/agent-skills/next-best-practices` or similar surfaces, mention it briefly before starting. If nothing strong, just build the page.

**Good on-demand trigger:**
> User: "Is there a skill on skills.sh for doing SEO audits?"
> Action: Search `seo audit`. Find `coreyhaines31/marketingskills/seo-audit`. Surface it with description and install command.

**Bad trigger (do not activate):**
> User: "What's the capital of France?"
> Action: Just answer. No skills.sh search needed.

**Wide-net behavior:**
> User: "I want to make videos with AI."
> Action: Cast wide. Search `ai video`, `video generation`, `video edit`. Surface AI video gen skills, video editing skills, and adjacent tools like image-to-video and motion graphics — not just the closest match.
