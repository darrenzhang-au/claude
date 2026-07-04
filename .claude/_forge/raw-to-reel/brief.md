# Skill Brief: Raw to Reel  (`raw-to-reel`)

## §0 Coverage Manifest
- [ ] name matches folder slug (kebab-case)
- [ ] `version:` set in frontmatter (semver)
- [ ] sharp description with ≥3 trigger phrases + a "do NOT use when" boundary
- [ ] cleared novelty gate (wedge stated; nearest neighbors + overlap scores listed)
- [ ] structure decision recorded (standalone / join / new-pipeline)
- [ ] when-to-use section
- [ ] concrete workflow steps
- [ ] integrity rules / non-negotiables
- [ ] output format defined
- [ ] anti-patterns section
- [ ] ≥2 golden examples present and passing
- [ ] assets present if needed (else struck)
- [ ] `handoffs_to:`/`expects_from:` declared if the skill composes (else struck)
- [ ] passed forge-6-verify (Trigger Arena ≥ bar + golden replay + convention check)
Skill-specific:
- [ ] Python script that emits a frame-accurate FCP7 XML sequence (Premiere Pro 2022-importable) from a cut list
- [ ] Transcription step with WORD-level timestamps (Whisper family), incl. dependency check + install guidance
- [ ] Cut-decision rubric: flubbed/repeated takes, filler words, dead air, false starts, tangents — with keep-last-good-take logic
- [ ] Coherence gate: kept transcript must read as a complete, sensical message before cuts are finalized
- [ ] ≤60s enforcement ladder (mistakes → filler/dead air → redundancy → weakest tangents), never cutting the core message
- [ ] Hook pass: strongest opening line surfaced to the front when it improves the edit (reorder expressed in the sequence)
- [ ] 9:16 vertical sequence settings (1080×1920) with sane default scale/position for 16:9 sources
- [ ] SRT caption file generated from kept-content word timestamps
- [ ] Edit report: every cut listed with timecode + reason, plus final runtime
- [ ] XML structural self-check before handing over (validates against FCP7 XML shape)

## 1. Purpose
This skill turns one raw talking-to-camera clip into a post-ready ≤60-second short-form edit by transcribing it with word-level timestamps, cutting mistakes/retakes/filler/dead air, tightening and (when useful) reordering for a hook while preserving a coherent message, and delivering a Premiere Pro 2022-importable FCP7 XML sequence (9:16) plus SRT captions and a cut report — so the user opens Premiere with the edit already made.

## 2. Profile
- Category: automation (produces artifact)
- Invoked by: user on demand
- Complexity: complex (multi-step, editorial judgment, generated assets)
- External deps: ffmpeg/ffprobe, Whisper-family transcriber (faster-whisper preferred), Python 3

## 3. Triggers
**Fires when:** the user hands over (or points at) a raw talking-head/selfie-style video and wants the mistakes, retakes, filler, or awkwardness removed to make it postable short-form content — Reels / TikTok / Shorts.
**Does NOT fire when:**
- The edit is multi-cam, b-roll-driven, or long-form (target > ~90s) — that's a real NLE session, not this pipeline.
- The video has no speech (music/montage content) — the whole engine is transcript-driven.
- The user wants the edit done inside the Vyra editor session (Vyra's own skills apply there).
- The user only wants captions, only wants format conversion/compression, or only wants a thumbnail/description.
**Natural phrases:** "clean up this raw video for socials", "remove the mistakes from my talking-head clip", "turn this raw take into a reel", "make this post-ready — cut the flubs and dead air", "get this down to 60 seconds for TikTok", "I recorded myself talking, edit out the bad takes"

## 4. Inputs → Output
- Inputs: path to one raw video file with speech (multiple retakes may live inside the one file); optional prefs (target platform, caption style, whether reordering is allowed).
- Output: a `<clip-name>-edit/` folder containing `sequence.xml` (FCP7 XML, 9:16, all cuts applied, importable into Premiere Pro 2022 via File→Import), `captions.srt`, and `edit-report.md` (every cut + reason, kept-transcript readout, final runtime). Non-destructive: XML references the original media.

## 5. Unique wedge (draft — to be tested in stage 2)
Nothing in the library touches video; unlike Vyra's in-editor skills or generic "edit my video" prompting, this is a local, transcript-driven editorial pipeline that ends in a *Premiere Pro-importable cut sequence* — mistakes/retakes judged from the transcript, coherence-checked tightening to ≤60s, hook-first reorder, vertical sequence, and captions, all reviewable and reversible inside the user's own NLE.

## 6. Open questions / assumptions
- **Assumption:** single source file per run (retakes inside one recording); multi-file input is out of scope v1.
- **Assumption (user-confirmed):** over-60s → keep cutting weakest content automatically; core message is inviolable.
- Retake detection: near-duplicate sentences → keep the *last* complete take by default? Or judge "best delivery" from transcript signals (completeness, no mid-word restart)? → grill.
- Cut hygiene: how much padding around word boundaries to avoid clipped syllables; straight jump-cuts are the accepted short-form aesthetic (no B-roll patching) → confirm in grill.
- Hook reorder: always attempt, or only when a clearly stronger opener exists mid-clip? Reordering risks continuity (visual jump + verbal tense) → grill.
- 16:9 source into 9:16 sequence: default center-crop scale, user adjusts framing in Premiere afterward → confirm.
- Caption styling: SRT is plain by design (Premiere styles it); is that enough for "post-ready"? → grill.
