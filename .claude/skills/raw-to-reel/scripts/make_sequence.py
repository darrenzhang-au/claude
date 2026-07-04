#!/usr/bin/env python3
"""Generate a Premiere Pro-importable FCP7 XML sequence + SRT captions from a cut list.

Usage: python make_sequence.py <cutlist.json>

cutlist.json schema (all times in SOURCE-relative seconds; segments in OUTPUT order):
{
  "video": "C:/abs/path/clip.mp4",
  "width": 3840, "height": 2160,
  "fps": { "num": 30000, "den": 1001 },
  "segments": [ { "in": 12.48, "out": 19.02 }, ... ],
  "words":    [ { "w": "Here's", "start": 12.61, "end": 12.90 }, ... ]   # kept words only
}

Writes, next to cutlist.json:
  sequence.xml  — FCP7 <xmeml v4>: 1080x1920 sequence at the source's exact frame rate, one clip
                  per segment on V1/A1, fill-height Basic Motion scale for non-9:16 sources.
                  Import in Premiere 2022 via File -> Import.
  captions.srt  — <=4-word cues, >=0.5s each, re-timed to the edited sequence.

Exits non-zero if the structural self-check fails. Stdlib only.
"""
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

SEQ_W, SEQ_H = 1080, 1920
MAX_CUE_WORDS = 4
MIN_CUE_SEC = 0.5
CUE_GAP_BREAK = 0.6


def frames(sec, num, den):
    return int(round(sec * num / den))


def rate_elem(parent, timebase, ntsc):
    r = ET.SubElement(parent, "rate")
    ET.SubElement(r, "timebase").text = str(timebase)
    ET.SubElement(r, "ntsc").text = "TRUE" if ntsc else "FALSE"
    return r


def build_xml(cl):
    num, den = cl["fps"]["num"], cl["fps"]["den"]
    ntsc = den == 1001
    timebase = int(round(num / den)) if den != 1001 else num // 1000
    src_w, src_h = cl["width"], cl["height"]
    video_path = os.path.abspath(cl["video"])
    clip_name = os.path.basename(video_path)
    pathurl = "file://localhost/" + urllib.request.pathname2url(video_path).lstrip("/")

    seg_frames = [(frames(s["in"], num, den), frames(s["out"], num, den)) for s in cl["segments"]]
    for i, (fin, fout) in enumerate(seg_frames):
        if fout <= fin:
            raise ValueError(f"segment {i}: out <= in after frame rounding ({fin}..{fout})")
    total = sum(fout - fin for fin, fout in seg_frames)
    file_dur = frames(max(s["out"] for s in cl["segments"]), num, den)

    # fill-height/width scale so the source covers the 9:16 frame (user re-frames in Premiere)
    scale_pct = round(max(SEQ_W / src_w, SEQ_H / src_h) * 100, 2)

    xmeml = ET.Element("xmeml", version="4")
    seq = ET.SubElement(xmeml, "sequence", id="sequence-1")
    ET.SubElement(seq, "name").text = os.path.splitext(clip_name)[0] + " — raw-to-reel"
    ET.SubElement(seq, "duration").text = str(total)
    rate_elem(seq, timebase, ntsc)
    media = ET.SubElement(seq, "media")

    # ---- video ----
    video = ET.SubElement(media, "video")
    fmt = ET.SubElement(video, "format")
    sc = ET.SubElement(fmt, "samplecharacteristics")
    rate_elem(sc, timebase, ntsc)
    ET.SubElement(sc, "width").text = str(SEQ_W)
    ET.SubElement(sc, "height").text = str(SEQ_H)
    ET.SubElement(sc, "pixelaspectratio").text = "square"
    vtrack = ET.SubElement(video, "track")

    def add_file(parent, first):
        if not first:
            ET.SubElement(parent, "file", id="file-1")
            return
        f = ET.SubElement(parent, "file", id="file-1")
        ET.SubElement(f, "name").text = clip_name
        ET.SubElement(f, "pathurl").text = pathurl
        rate_elem(f, timebase, ntsc)
        ET.SubElement(f, "duration").text = str(file_dur)
        fmedia = ET.SubElement(f, "media")
        fv = ET.SubElement(fmedia, "video")
        fsc = ET.SubElement(fv, "samplecharacteristics")
        ET.SubElement(fsc, "width").text = str(src_w)
        ET.SubElement(fsc, "height").text = str(src_h)
        fa = ET.SubElement(fmedia, "audio")
        ET.SubElement(fa, "channelcount").text = "2"

    pos = 0
    for i, (fin, fout) in enumerate(seg_frames):
        ci = ET.SubElement(vtrack, "clipitem", id=f"clipitem-v{i + 1}")
        ET.SubElement(ci, "name").text = clip_name
        ET.SubElement(ci, "enabled").text = "TRUE"
        ET.SubElement(ci, "duration").text = str(file_dur)
        rate_elem(ci, timebase, ntsc)
        ET.SubElement(ci, "start").text = str(pos)
        ET.SubElement(ci, "end").text = str(pos + (fout - fin))
        ET.SubElement(ci, "in").text = str(fin)
        ET.SubElement(ci, "out").text = str(fout)
        add_file(ci, first=(i == 0))
        if abs(scale_pct - 100.0) > 0.01:
            flt = ET.SubElement(ci, "filter")
            eff = ET.SubElement(flt, "effect")
            ET.SubElement(eff, "name").text = "Basic Motion"
            ET.SubElement(eff, "effectid").text = "basic"
            ET.SubElement(eff, "effectcategory").text = "motion"
            ET.SubElement(eff, "effecttype").text = "motion"
            ET.SubElement(eff, "mediatype").text = "video"
            par = ET.SubElement(eff, "parameter")
            ET.SubElement(par, "parameterid").text = "scale"
            ET.SubElement(par, "name").text = "Scale"
            ET.SubElement(par, "valuemin").text = "0"
            ET.SubElement(par, "valuemax").text = "10000"
            ET.SubElement(par, "value").text = str(scale_pct)
        pos += fout - fin

    # ---- audio ----
    audio = ET.SubElement(media, "audio")
    afmt = ET.SubElement(audio, "format")
    asc = ET.SubElement(afmt, "samplecharacteristics")
    ET.SubElement(asc, "depth").text = "16"
    ET.SubElement(asc, "samplerate").text = "48000"
    atrack = ET.SubElement(audio, "track")
    pos = 0
    for i, (fin, fout) in enumerate(seg_frames):
        ci = ET.SubElement(atrack, "clipitem", id=f"clipitem-a{i + 1}")
        ET.SubElement(ci, "name").text = clip_name
        ET.SubElement(ci, "enabled").text = "TRUE"
        ET.SubElement(ci, "duration").text = str(file_dur)
        rate_elem(ci, timebase, ntsc)
        ET.SubElement(ci, "start").text = str(pos)
        ET.SubElement(ci, "end").text = str(pos + (fout - fin))
        ET.SubElement(ci, "in").text = str(fin)
        ET.SubElement(ci, "out").text = str(fout)
        ET.SubElement(ci, "file", id="file-1")
        st = ET.SubElement(ci, "sourcetrack")
        ET.SubElement(st, "mediatype").text = "audio"
        ET.SubElement(st, "trackindex").text = "1"
        pos += fout - fin

    tc = ET.SubElement(seq, "timecode")
    rate_elem(tc, timebase, ntsc)
    ET.SubElement(tc, "string").text = "00:00:00:00"
    ET.SubElement(tc, "frame").text = "0"
    ET.SubElement(tc, "displayformat").text = "NDF"

    return xmeml, total


def seq_time_of(word_t, segments):
    """Map a source-relative time to sequence time; None if it falls in a cut."""
    offset = 0.0
    for s in segments:
        if s["in"] - 1e-6 <= word_t <= s["out"] + 1e-6:
            return offset + (word_t - s["in"])
        offset += s["out"] - s["in"]
    return None


def srt_ts(t):
    ms = int(round(t * 1000))
    h, rem = divmod(ms, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt(cl, total_sec):
    words = []
    for w in cl.get("words", []):
        mid = (w["start"] + w["end"]) / 2
        st = seq_time_of(mid, cl["segments"])
        if st is None:
            continue
        half = (w["end"] - w["start"]) / 2
        words.append({"w": w["w"], "start": max(0.0, st - half), "end": min(total_sec, st + half)})
    words.sort(key=lambda w: w["start"])

    cues, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        breaks = (
            len(cur) >= MAX_CUE_WORDS
            or nxt is None
            or (nxt["start"] - w["end"]) > CUE_GAP_BREAK
            or w["w"].rstrip('"').endswith((".", "!", "?"))
        )
        if breaks:
            cues.append(cur)
            cur = []

    lines = []
    for i, cue in enumerate(cues):
        start = cue[0]["start"]
        end = max(cue[-1]["end"], start + MIN_CUE_SEC)
        if i + 1 < len(cues):
            end = min(end, cues[i + 1][0]["start"] - 0.001)
        end = max(end, start + 0.2)  # never zero-length even when squeezed
        text = " ".join(w["w"] for w in cue)
        lines.append(f"{i + 1}\n{srt_ts(start)} --> {srt_ts(end)}\n{text}\n")
    return "\n".join(lines)


def self_check(xml_path, expected_total):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    assert root.tag == "xmeml", "root must be xmeml"
    seq = root.find("sequence")
    assert seq is not None, "missing sequence"
    assert int(seq.findtext("duration")) == expected_total, "sequence duration != sum of segments"
    clipitems = seq.findall(".//clipitem")
    assert clipitems, "no clipitems"
    for ci in clipitems:
        cin, cout = int(ci.findtext("in")), int(ci.findtext("out"))
        start, end = int(ci.findtext("start")), int(ci.findtext("end"))
        assert cin < cout, f"{ci.get('id')}: in >= out"
        assert end - start == cout - cin, f"{ci.get('id')}: sequence span != source span"
    tbs = {r.findtext("timebase") for r in seq.findall(".//rate")}
    assert len(tbs) == 1, f"inconsistent timebases: {tbs}"
    pathurl = seq.findtext(".//file/pathurl")
    assert pathurl and pathurl.startswith("file://"), "missing/invalid pathurl"
    return len(clipitems)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    cutlist_path = os.path.abspath(sys.argv[1])
    out_dir = os.path.dirname(cutlist_path)
    with open(cutlist_path, encoding="utf-8-sig") as f:  # tolerate Windows BOM
        cl = json.load(f)
    for key in ("video", "width", "height", "fps", "segments"):
        if key not in cl:
            print(f"cutlist.json missing '{key}'", file=sys.stderr)
            return 1
    if not cl["segments"]:
        print("cutlist.json has no segments", file=sys.stderr)
        return 1

    num, den = cl["fps"]["num"], cl["fps"]["den"]
    xmeml, total = build_xml(cl)
    ET.indent(xmeml)
    xml_path = os.path.join(out_dir, "sequence.xml")
    with open(xml_path, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n')
        f.write(ET.tostring(xmeml))

    total_sec = total * den / num
    srt_path = os.path.join(out_dir, "captions.srt")
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(build_srt(cl, total_sec))

    n = self_check(xml_path, total)
    print(f"sequence.xml OK: {len(cl['segments'])} segments, {n} clipitems, "
          f"{total} frames = {total_sec:.2f}s @ {num}/{den} fps, {SEQ_W}x{SEQ_H}")
    print(f"captions.srt OK: {sum(1 for line in open(srt_path, encoding='utf-8') if ' --> ' in line)} cues")
    return 0


if __name__ == "__main__":
    sys.exit(main())
