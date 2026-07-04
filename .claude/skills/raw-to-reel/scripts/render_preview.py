#!/usr/bin/env python3
"""Render a low-res phone-preview MP4 of the edited cut, captions burned in.

Usage: python render_preview.py <cutlist.json> [captions.srt]

Reads the same cutlist.json used by make_sequence.py, applies the segments in output
order with ffmpeg trim/concat, scales to 540x960 (fill-height crop to 9:16), burns in
captions.srt when present, and writes preview.mp4 next to the cutlist.

This is a GUT-CHECK artifact for pacing review on a phone — never the deliverable.
The deliverable stays the non-destructive sequence.xml. Requires ffmpeg on PATH.
"""
import json
import os
import shutil
import subprocess
import sys

PREVIEW_W, PREVIEW_H = 540, 960


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cutlist_path = os.path.abspath(sys.argv[1])
    out_dir = os.path.dirname(cutlist_path)
    srt_path = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.join(out_dir, "captions.srt")

    if shutil.which("ffmpeg") is None:
        print("ffmpeg not found on PATH — install it to render previews.", file=sys.stderr)
        return 1

    with open(cutlist_path, encoding="utf-8-sig") as f:
        cl = json.load(f)
    segments = cl["segments"]
    if not segments:
        print("cutlist.json has no segments", file=sys.stderr)
        return 1

    # trim each kept span, then concat in output order (handles hook reorders)
    parts, vf_labels, af_labels = [], [], []
    for i, s in enumerate(segments):
        parts.append(
            f"[0:v]trim=start={s['in']}:end={s['out']},setpts=PTS-STARTPTS[v{i}];"
            f"[0:a]atrim=start={s['in']}:end={s['out']},asetpts=PTS-STARTPTS[a{i}];"
        )
        vf_labels.append(f"[v{i}]")
        af_labels.append(f"[a{i}]")
    n = len(segments)
    post = f"scale={PREVIEW_W}:{PREVIEW_H}:force_original_aspect_ratio=increase,crop={PREVIEW_W}:{PREVIEW_H}"
    if os.path.isfile(srt_path):
        # ffmpeg subtitles filter needs forward slashes and an escaped drive colon on Windows
        srt_esc = srt_path.replace("\\", "/").replace(":", "\\:")
        post += f",subtitles='{srt_esc}'"
    graph = (
        "".join(parts)
        + "".join(vf_labels) + f"concat=n={n}:v=1:a=0[vc];"
        + "".join(af_labels) + f"concat=n={n}:v=0:a=1[ac];"
        + f"[vc]{post}[vout]"
    )

    out_path = os.path.join(out_dir, "preview.mp4")
    cmd = [
        "ffmpeg", "-y", "-i", cl["video"],
        "-filter_complex", graph,
        "-map", "[vout]", "-map", "[ac]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
        "-c:a", "aac", "-b:a", "96k",
        out_path,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr[-2000:], file=sys.stderr)
        return proc.returncode
    dur = sum(s["out"] - s["in"] for s in segments)
    print(f"preview.mp4 OK: {n} segments, ~{dur:.1f}s, {PREVIEW_W}x{PREVIEW_H}, "
          f"captions {'burned in' if os.path.isfile(srt_path) else 'not found — skipped'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
