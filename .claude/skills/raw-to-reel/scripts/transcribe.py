#!/usr/bin/env python3
"""Transcribe a video with word-level timestamps using faster-whisper.

Usage: python transcribe.py <video> <out_words.json> [model_size]

Output JSON:
{
  "language": "en", "duration": 183.4,
  "segments": [
    { "start": 0.0, "end": 4.2, "text": "...", "avg_logprob": -0.21,
      "words": [ { "w": "Hey", "start": 0.12, "end": 0.31, "p": 0.98 } ] }
  ]
}
avg_logprob is the confidence signal: segments below ~-0.8 should be treated as
low-confidence (keep, don't cut; flag in the report).
"""
import json
import sys


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    video, out_path = sys.argv[1], sys.argv[2]
    model_size = sys.argv[3] if len(sys.argv) > 3 else "small"

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print("faster-whisper is not installed. Run: pip install faster-whisper", file=sys.stderr)
        return 1

    def _run(device):
        model = WhisperModel(model_size, device=device, compute_type="auto")
        return model.transcribe(video, word_timestamps=True, vad_filter=True)

    try:
        segments, info = _run("auto")
    except Exception as e:  # GPU present but CUDA/cuBLAS/cuDNN runtime missing -> fall back to CPU
        msg = str(e).lower()
        if any(k in msg for k in ("cuda", "cublas", "cudnn", "gpu", "nvidia")):
            print(f"GPU path unavailable ({e}); falling back to CPU.", file=sys.stderr)
            segments, info = _run("cpu")
        else:
            raise

    out = {"language": info.language, "duration": round(info.duration, 3), "segments": []}
    for seg in segments:
        out["segments"].append({
            "start": round(seg.start, 3),
            "end": round(seg.end, 3),
            "text": seg.text.strip(),
            "avg_logprob": round(seg.avg_logprob, 3),
            "words": [
                {"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3),
                 "p": round(w.probability, 3)}
                for w in (seg.words or [])
            ],
        })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"wrote {out_path}: {sum(len(s['words']) for s in out['segments'])} words, "
          f"{len(out['segments'])} segments, {out['duration']}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
