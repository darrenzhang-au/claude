# Excalidraw scene JSON template

The complete schema for a paste-able Excalidraw scene. Mode B output should follow this structure.

## Wrapper

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

- `type` must be `"excalidraw"`. The importer rejects anything else.
- `version` is `2` for the current schema.
- `source` is informational; `"https://excalidraw.com"` is the safe default.
- `appState.gridSize` can be `null` (no grid) or an integer (e.g., `20`).
- `files` is for embedded images, usually `{}`.

## Element common fields

Every element — rectangle, ellipse, diamond, arrow, line, text, frame — needs these base fields:

```json
{
  "id": "Wx7kL2nQ",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": 1234567,
  "version": 1,
  "versionNonce": 987654321,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false
}
```

Notes:

- `id` is an 8–12 char alphanumeric string. Random is fine; Excalidraw normalizes it.
- `seed` and `versionNonce` should be random integers. Plausible values are enough — the importer doesn't validate them.
- `updated` is a Unix timestamp in ms. Any recent value works.
- `roundness: { "type": 3 }` gives rectangles their rounded corners. Set to `null` for sharp corners. Omit on ellipses/diamonds.
- `boundElements` lists the IDs of child text labels and connected arrows. Important for binding (see below).

## Text elements

```json
{
  "id": "Tx9mP3rS",
  "type": "text",
  "x": 130,
  "y": 130,
  "width": 140,
  "height": 25,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "seed": 1111111,
  "version": 1,
  "versionNonce": 2222222,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "text": "Login",
  "fontSize": 20,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "baseline": 18,
  "containerId": "Wx7kL2nQ",
  "originalText": "Login",
  "lineHeight": 1.25
}
```

- `fontFamily`: `1` = Virgil (hand-drawn), `2` = Helvetica, `3` = Cascadia (mono). Default to `1`.
- `fontSize`: 16 for body, 20 for labels, 28+ for titles.
- **`containerId` is how you bind text to a shape.** Set it to the parent shape's `id`, and add this text's `id` to the parent's `boundElements` array as `{ "id": "Tx9mP3rS", "type": "text" }`.

## Arrows (with binding)

```json
{
  "id": "Ar5nK8pQ",
  "type": "arrow",
  "x": 200,
  "y": 180,
  "width": 0,
  "height": 100,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "seed": 3333333,
  "version": 1,
  "versionNonce": 4444444,
  "isDeleted": false,
  "boundElements": [],
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "points": [[0, 0], [0, 100]],
  "lastCommittedPoint": null,
  "startBinding": {
    "elementId": "Wx7kL2nQ",
    "focus": 0,
    "gap": 1
  },
  "endBinding": {
    "elementId": "Yz3pR7mN",
    "focus": 0,
    "gap": 1
  },
  "startArrowhead": null,
  "endArrowhead": "arrow",
  "elbowed": false
}
```

- `points` is an array of `[x, y]` offsets from the arrow's `x`/`y`. First point is always `[0, 0]`.
- **`startBinding.elementId` and `endBinding.elementId` are how arrows follow shapes.** Always bind unless the arrow is intentionally floating.
- Also add the arrow's `id` to both connected shapes' `boundElements`: `{ "id": "Ar5nK8pQ", "type": "arrow" }`.
- `endArrowhead: "arrow"` for a normal arrow; `null` for a plain line; `"triangle"`, `"dot"`, etc. for variants.

## Frames (for presentations and grouping)

```json
{
  "id": "Fr2mK4pL",
  "type": "frame",
  "x": 0,
  "y": 0,
  "width": 854,
  "height": 480,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 0,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": 5555555,
  "version": 1,
  "versionNonce": 6666666,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1700000000000,
  "link": null,
  "locked": false,
  "name": "Slide 1"
}
```

- Elements inside the frame set `frameId` to the frame's `id`.
- Frames default to `roughness: 0` for clean slide edges.

## Binding checklist

Whenever you connect a text label to a shape, or an arrow to two shapes, you have **two** updates to make:

1. The child sets its parent ref (`containerId` for text, `startBinding`/`endBinding` for arrows).
2. The parent adds the child to `boundElements`.

Miss either side and the binding silently fails. The shape will move and leave the text/arrow behind.

## Minimal working example: 2-step flowchart

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "id": "shape1", "type": "rectangle", "x": 300, "y": 100,
      "width": 200, "height": 80, "angle": 0,
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "groupIds": [], "frameId": null,
      "roundness": { "type": 3 }, "seed": 1, "version": 1,
      "versionNonce": 1, "isDeleted": false,
      "boundElements": [{ "id": "label1", "type": "text" }, { "id": "arrow1", "type": "arrow" }],
      "updated": 1700000000000, "link": null, "locked": false
    },
    {
      "id": "label1", "type": "text", "x": 330, "y": 125,
      "width": 140, "height": 30, "angle": 0,
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "groupIds": [], "frameId": null,
      "seed": 2, "version": 1, "versionNonce": 2, "isDeleted": false,
      "boundElements": [], "updated": 1700000000000, "link": null, "locked": false,
      "text": "Sign up", "fontSize": 20, "fontFamily": 1,
      "textAlign": "center", "verticalAlign": "middle", "baseline": 18,
      "containerId": "shape1", "originalText": "Sign up", "lineHeight": 1.25
    },
    {
      "id": "shape2", "type": "rectangle", "x": 300, "y": 280,
      "width": 200, "height": 80, "angle": 0,
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "groupIds": [], "frameId": null,
      "roundness": { "type": 3 }, "seed": 3, "version": 1,
      "versionNonce": 3, "isDeleted": false,
      "boundElements": [{ "id": "label2", "type": "text" }, { "id": "arrow1", "type": "arrow" }],
      "updated": 1700000000000, "link": null, "locked": false
    },
    {
      "id": "label2", "type": "text", "x": 320, "y": 305,
      "width": 160, "height": 30, "angle": 0,
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "groupIds": [], "frameId": null,
      "seed": 4, "version": 1, "versionNonce": 4, "isDeleted": false,
      "boundElements": [], "updated": 1700000000000, "link": null, "locked": false,
      "text": "Verify email", "fontSize": 20, "fontFamily": 1,
      "textAlign": "center", "verticalAlign": "middle", "baseline": 18,
      "containerId": "shape2", "originalText": "Verify email", "lineHeight": 1.25
    },
    {
      "id": "arrow1", "type": "arrow", "x": 400, "y": 180,
      "width": 0, "height": 100, "angle": 0,
      "strokeColor": "#1e1e1e", "backgroundColor": "transparent",
      "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
      "roughness": 1, "opacity": 100, "groupIds": [], "frameId": null,
      "seed": 5, "version": 1, "versionNonce": 5, "isDeleted": false,
      "boundElements": [], "updated": 1700000000000, "link": null, "locked": false,
      "points": [[0, 0], [0, 100]], "lastCommittedPoint": null,
      "startBinding": { "elementId": "shape1", "focus": 0, "gap": 1 },
      "endBinding": { "elementId": "shape2", "focus": 0, "gap": 1 },
      "startArrowhead": null, "endArrowhead": "arrow", "elbowed": false
    }
  ],
  "appState": { "viewBackgroundColor": "#ffffff", "gridSize": null },
  "files": {}
}
```

Paste this into excalidraw.com and you should see two rounded rectangles ("Sign up" → "Verify email") connected by an arrow.
