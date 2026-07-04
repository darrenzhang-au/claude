# Novelty Check: Raw to Reel

## Nearest neighbors (from library model — LLM-judged)
1. `infographic-builder` — builds static HTML social graphics from text/data; stops at images, never touches video/audio. Overlap: 10/100. Neighbor-shift risk: none ("make a social graphic" vs "edit my video" don't contest prompts).
2. `skills-sh-finder` — meta skill that finds community skills; could *surface* video tools but does no editing. Overlap: 5/100. Neighbor-shift risk: none.
3. `excalidraw-diagram-generator` — visual artifact generator, unrelated medium. Overlap: 4/100. Neighbor-shift risk: none.

maxScore (local library): 10/100 — no local skill touches video or audio at all.

Note: the Vyra MCP server (when connected) has built-in editor skills (`transcript-cleanup` removes filler/dead air on the Vyra timeline). That is a *session capability*, not a library skill, and it ends inside Vyra — it cannot produce a Premiere deliverable. Boundary to draw: "user wants the edit in Vyra → use Vyra; user wants a Premiere project from raw footage → this skill."

## Ecosystem prior art
- **ButterCut** — open-source Claude Code video editing; WhisperX transcription → ready-to-import roughcut as FCPXML / Premiere XML / Resolve DRP — https://github.com/barefootford/buttercut (fact). Closest prior art: same interchange-file endgame. It builds *roughcuts* from footage; PolyForm **Noncommercial** license (fact) — a constraint for social content made commercially.
- **6missedcalls/video-editing-skill** — Bash+FFmpeg+Whisper agent skill: jumpcut (dB-threshold silence removal), captions, overlays; re-renders the file destructively, no NLE export — https://github.com/6missedcalls/video-editing-skill (fact).
- **auto-editor** — CLI that cuts silence mechanically and exports Premiere/Resolve timelines — https://knightli.com/en/2026/04/23/auto-editor-auto-cut-silence-premiere-resolve-workflow/ (fact).
- **Commercial SaaS/plugins** — TimeBolt, Recut, Gling, OpusClip, CutBack's Premiere Assistant all do silence/filler removal or auto-shorts as paid products (fact).
- Assessment (judgment): the *mechanical* half (silence detection, cut lists, XML export) is well-trodden. What no prior-art agent skill encodes is the **editorial** half for short-form talking-head: semantic retake/flub detection (keep the last good take), a coherence gate on the surviving message, a ≤60s enforcement ladder that trims weakest content rather than silences, and a hook-first reorder — plus the 9:16 sequence and captions as one post-ready package. auto-editor and jumpcut tools cut *silence*, not *mistakes*; ButterCut assembles roughcuts, it doesn't finish a reel.

## Wedge test
Wedge: "Unlike auto-editor/ButterCut-style roughcut and silence-cut tools, raw-to-reel makes *editorial* judgments from the transcript — drops flubbed and repeated takes keeping the best one, tightens to ≤60s through a coherence gate so the survivor still makes sense, and leads with the hook — delivering a post-ready 9:16 Premiere sequence + captions rather than a roughcut, which matters because the judgment pass is exactly the part the user is doing by hand today."
- Real difference vs reskin: real — silence-threshold cutting and semantic mistake/retake/coherence judgment are different capabilities; the latter is the LLM's contribution and the stated pain ("removes all the mistakes and awkwardness... must make sense to the audience").
- Could a one-line prompt do it? No — it needs a working FCP7 XML generator script (frame math, fps, media refs), a transcription workflow, a cut rubric, and a repeatable coherence/60s process.
- Durable? Yes vs mechanical cutters (different capability class). vs ButterCut: partially convergent endgame, but the short-form editorial finishing (retakes, 60s ladder, hook) is out of its roughcut scope, and its noncommercial license limits it anyway.

## Verdict: PROCEED
Local library is empty in this space (maxScore 10). Ecosystem prior art covers the mechanical layer; the wedge lives in the editorial layer and the post-ready (not roughcut) deliverable. No `[!DUPLICATE]`/`[!GENERIC]`. Two boundary lines the description must draw: (1) not for in-Vyra editing sessions; (2) not a silence-remover — if the user only wants dead-air stripped mechanically, point at auto-editor-class tools. Annotation `[!NEEDS-ASSET]` stands: the XML generator script is load-bearing and must be verified against Premiere's importer shape.
