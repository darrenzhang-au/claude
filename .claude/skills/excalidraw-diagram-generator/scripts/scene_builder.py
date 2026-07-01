"""
Excalidraw scene builder — handles boilerplate, IDs, and binding correctly.

Usage:
    s = Scene()
    rect_id = s.add_rect("Login", x=300, y=100, w=200, h=80)
    diamond_id = s.add_diamond("Valid?", x=300, y=280, w=200, h=100)
    s.add_arrow(rect_id, diamond_id)  # auto-binds + computes points
    s.save("/path/to/file.excalidraw")
"""

import json
import random
import string
import time

BLACK = "#1e1e1e"
ACCENT_GREEN = "#2f9e44"
ACCENT_BLUE = "#1971c2"
ACCENT_RED = "#e03131"
DASHED = "dashed"


# Style presets. Default is "clean" — roughness 0, Helvetica, no fills.
# Pass a preset name or a dict of overrides to Scene(style=...).
STYLE_PRESETS = {
    "clean": {
        "roughness": 0,
        "font_family": 2,        # Helvetica
        "stroke_color": "#2d2d2d",
        "accent_color": "#1971c2",
        "fill": "transparent",
        "rounded": True,
        "stroke_width": 2,
    },
    "default": {
        "roughness": 1,
        "font_family": 1,        # Virgil (hand-drawn)
        "stroke_color": "#1e1e1e",
        "accent_color": "#2f9e44",
        "fill": "transparent",
        "rounded": True,
        "stroke_width": 2,
    },
    "whiteboard": {
        "roughness": 2,
        "font_family": 1,        # Virgil
        "stroke_color": "#1e1e1e",
        "accent_color": "#e8590c",
        "fill": "#ffec99",
        "rounded": False,
        "stroke_width": 2,
    },
    "mono": {
        "roughness": 0,
        "font_family": 2,        # Helvetica
        "stroke_color": "#000000",
        "accent_color": "#555555",
        "fill": "transparent",
        "rounded": False,
        "stroke_width": 2,
    },
}


def _resolve_style(style):
    """Accept a preset name, dict of overrides, or None. Returns full style dict."""
    if style is None:
        return dict(STYLE_PRESETS["clean"])
    if isinstance(style, str):
        if style not in STYLE_PRESETS:
            raise ValueError(f"Unknown style preset: {style}. "
                             f"Options: {list(STYLE_PRESETS)}")
        return dict(STYLE_PRESETS[style])
    if isinstance(style, dict):
        # Overlay on top of "clean"
        merged = dict(STYLE_PRESETS["clean"])
        merged.update(style)
        return merged
    raise TypeError(f"style must be a preset name, dict, or None — got {type(style)}")


def _id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def _seed():
    return random.randint(1, 2_000_000_000)


def _now_ms():
    return int(time.time() * 1000)


class Scene:
    def __init__(self, background="#ffffff", style=None):
        """
        Args:
            background: Canvas background hex color.
            style: Either a preset name ("clean", "default", "whiteboard", "mono")
                   or a dict of overrides. Defaults to "clean".
        """
        self.elements = []
        self.background = background
        self.style = _resolve_style(style)
        self._by_id = {}

    # --- internal -----------------------------------------------------------

    def _base(self, type_, x, y, w, h, **overrides):
        el = {
            "id": _id(),
            "type": type_,
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "angle": 0,
            "strokeColor": self.style["stroke_color"],
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": self.style["stroke_width"],
            "strokeStyle": "solid",
            "roughness": self.style["roughness"],
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "seed": _seed(),
            "version": 1,
            "versionNonce": _seed(),
            "isDeleted": False,
            "boundElements": [],
            "updated": _now_ms(),
            "link": None,
            "locked": False,
        }
        el.update(overrides)
        return el

    def _add_label(self, container_id, text, font_size=20):
        c = self._by_id[container_id]
        # Center label inside container
        approx_text_w = min(len(text) * font_size * 0.55, c["width"] - 20)
        label = self._base(
            "text",
            x=c["x"] + (c["width"] - approx_text_w) / 2,
            y=c["y"] + (c["height"] - font_size * 1.25) / 2,
            w=approx_text_w,
            h=font_size * 1.25,
            frameId=c.get("frameId"),  # inherit container's frame
        )
        label["text"] = text
        label["fontSize"] = font_size
        label["fontFamily"] = self.style["font_family"]
        label["textAlign"] = "center"
        label["verticalAlign"] = "middle"
        label["baseline"] = int(font_size * 0.9)
        label["containerId"] = container_id
        label["originalText"] = text
        label["lineHeight"] = 1.25
        self.elements.append(label)
        self._by_id[label["id"]] = label
        c["boundElements"].append({"id": label["id"], "type": "text"})
        return label["id"]

    # --- public shape adders ------------------------------------------------

    def add_rect(self, label, x, y, w=200, h=80, *, rounded=None, frame_id=None,
                 stroke_color=None, stroke_style="solid", font_size=20,
                 background=None, accent=False):
        if rounded is None:
            rounded = self.style["rounded"]
        if stroke_color is None:
            stroke_color = self.style["accent_color"] if accent else self.style["stroke_color"]
        if background is None:
            background = self.style["fill"]
        el = self._base("rectangle", x, y, w, h,
                        roundness={"type": 3} if rounded else None,
                        strokeColor=stroke_color,
                        backgroundColor=background,
                        fillStyle="hachure" if background != "transparent"
                                  and self.style["roughness"] >= 2 else "solid",
                        strokeStyle=stroke_style,
                        frameId=frame_id)
        self.elements.append(el)
        self._by_id[el["id"]] = el
        if label:
            self._add_label(el["id"], label, font_size=font_size)
            # Color label to match if accent
            if accent:
                for lbl in [e for e in self.elements if e.get("containerId") == el["id"]]:
                    lbl["strokeColor"] = stroke_color
        return el["id"]

    def add_diamond(self, label, x, y, w=220, h=110, *, frame_id=None,
                    font_size=18, stroke_color=None, stroke_style="solid",
                    accent=False):
        if stroke_color is None:
            stroke_color = self.style["accent_color"] if accent else self.style["stroke_color"]
        el = self._base("diamond", x, y, w, h, frameId=frame_id,
                        strokeColor=stroke_color, strokeStyle=stroke_style)
        self.elements.append(el)
        self._by_id[el["id"]] = el
        if label:
            self._add_label(el["id"], label, font_size=font_size)
            if accent:
                for lbl in [e for e in self.elements if e.get("containerId") == el["id"]]:
                    lbl["strokeColor"] = stroke_color
        return el["id"]

    def add_ellipse(self, label, x, y, w=180, h=70, *, frame_id=None,
                    font_size=20, stroke_color=None, stroke_style="solid",
                    accent=False):
        if stroke_color is None:
            stroke_color = self.style["accent_color"] if accent else self.style["stroke_color"]
        el = self._base("ellipse", x, y, w, h, frameId=frame_id,
                        strokeColor=stroke_color, strokeStyle=stroke_style)
        self.elements.append(el)
        self._by_id[el["id"]] = el
        if label:
            self._add_label(el["id"], label, font_size=font_size)
            if accent:
                for lbl in [e for e in self.elements if e.get("containerId") == el["id"]]:
                    lbl["strokeColor"] = stroke_color
        return el["id"]

    def add_text(self, text, x, y, *, w=None, h=None, font_size=20,
                 text_align="left", frame_id=None, color=None, accent=False):
        if w is None:
            w = max(int(len(text) * font_size * 0.55), 60)
        if h is None:
            h = int(font_size * 1.25)
        if color is None:
            color = self.style["accent_color"] if accent else self.style["stroke_color"]
        el = self._base("text", x, y, w, h, frameId=frame_id, strokeColor=color)
        el["text"] = text
        el["fontSize"] = font_size
        el["fontFamily"] = self.style["font_family"]
        el["textAlign"] = text_align
        el["verticalAlign"] = "top"
        el["baseline"] = int(font_size * 0.9)
        el["containerId"] = None
        el["originalText"] = text
        el["lineHeight"] = 1.25
        self.elements.append(el)
        self._by_id[el["id"]] = el
        return el["id"]

    def add_frame(self, name, x, y, w, h):
        el = self._base("frame", x, y, w, h, roughness=0)
        el["name"] = name
        el["boundElements"] = None
        self.elements.append(el)
        self._by_id[el["id"]] = el
        return el["id"]

    # --- arrows / lines ------------------------------------------------------

    def _anchor_points(self, start, end):
        """Compute arrow start and end points from shape centers/edges."""
        sx = start["x"] + start["width"] / 2
        sy = start["y"] + start["height"] / 2
        ex = end["x"] + end["width"] / 2
        ey = end["y"] + end["height"] / 2

        # Snap to nearest edge of each shape
        dx, dy = ex - sx, ey - sy
        if abs(dx) > abs(dy):
            # Horizontal-dominant
            sx_edge = start["x"] + start["width"] if dx > 0 else start["x"]
            ex_edge = end["x"] if dx > 0 else end["x"] + end["width"]
            return (sx_edge, sy), (ex_edge, ey)
        else:
            sy_edge = start["y"] + start["height"] if dy > 0 else start["y"]
            ey_edge = end["y"] if dy > 0 else end["y"] + end["height"]
            return (sx, sy_edge), (ex, ey_edge)

    def add_arrow(self, start_id, end_id, *, stroke_color=None,
                  stroke_style="solid", arrowhead="arrow", frame_id=None,
                  accent=False):
        if stroke_color is None:
            stroke_color = self.style["accent_color"] if accent else self.style["stroke_color"]
        start = self._by_id[start_id]
        end = self._by_id[end_id]
        (sx, sy), (ex, ey) = self._anchor_points(start, end)
        el = self._base(
            "arrow",
            x=sx, y=sy,
            w=abs(ex - sx), h=abs(ey - sy),
            strokeColor=stroke_color,
            strokeStyle=stroke_style,
            frameId=frame_id,
        )
        el["points"] = [[0, 0], [ex - sx, ey - sy]]
        el["lastCommittedPoint"] = None
        el["startBinding"] = {"elementId": start_id, "focus": 0, "gap": 4}
        el["endBinding"] = {"elementId": end_id, "focus": 0, "gap": 4}
        el["startArrowhead"] = None
        el["endArrowhead"] = arrowhead
        el["elbowed"] = False
        self.elements.append(el)
        self._by_id[el["id"]] = el
        # bidirectional binding
        start["boundElements"].append({"id": el["id"], "type": "arrow"})
        end["boundElements"].append({"id": el["id"], "type": "arrow"})
        return el["id"]

    def add_line(self, start_id, end_id, *, stroke_color=None,
                 stroke_style="solid", frame_id=None, accent=False):
        """Like add_arrow but no arrowhead and no binding (use for mind maps, ERDs)."""
        return self.add_arrow(start_id, end_id, stroke_color=stroke_color,
                              stroke_style=stroke_style, arrowhead=None,
                              frame_id=frame_id, accent=accent)

    # --- output -------------------------------------------------------------

    def to_dict(self):
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.elements,
            "appState": {
                "viewBackgroundColor": self.background,
                "gridSize": None,
            },
            "files": {},
        }

    def save(self, path):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        return path
