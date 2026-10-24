# cache.json schema (version 1)

`app/cache.json` holds everything the app shows: prompts, AI outputs, document
previews and the presenter script. The app replays it by default. A byte-identical
copy is embedded in `index.html` (inside `<script id="embedded-cache"
type="application/json">`) so the app also works when opened straight from disk
(`file://`), where browsers block `fetch()`. `scripts/build_cache.py` writes both;
`scripts/preflight.py` fails if they differ.

All text is plain UTF-8. Model outputs are stored as a small Markdown subset that
`app.js` renders: paragraphs, `**bold**`, `-` bullets, `1.` numbered lists, `###`
headings and pipe tables (`| a | b |` with a `|---|` separator row). Raw HTML in
outputs is escaped, never rendered.

## Top level

| Key | Type | Notes |
|-----|------|-------|
| `schema_version` | integer | Always `1`. |
| `label` | string | Always `"Synthetic demonstration data"`. Shown on every screen. |
| `generation` | object | Where the outputs came from (below). |
| `demo1` | object | Ladder demo (below). |
| `demo2` | object | Trust-but-verify demo (below). |
| `presenter` | object | Presenter script (below). |

### `generation`

| Key | Type | Notes |
|-----|------|-------|
| `mode` | `"representative-pregenerated"`, `"model-generated"` or `"copilot-recorded"` | Authored by the builder; produced by `scripts/regenerate_cache.py`; or answers copied out of Microsoft 365 Copilot during rehearsal and imported by `scripts/import_copilot_run.py`. |
| `model` | string or null | Model ID, or `"Microsoft 365 Copilot"`. Required unless representative. |
| `temperature` | number or null | `0` when model-generated. |
| `generated_at` | string | ISO date. |
| `note` | string | One line shown in the presenter view. |

## `demo1`

| Key | Type | Notes |
|-----|------|-------|
| `title` | string | `"From weak to strong"`. |
| `attachment` | string | File name shown as the attached report. |
| `parts` | array of `{id, label, hint}` | The four building blocks in order: `role`, `task`, `context`, `output`. |
| `stages` | array, exactly 5 | Ladder order: `weak`, `role`, `task`, `context`, `output`. |
| `comparison` | object | `{left, right, caption}`: stage IDs for the final side-by-side. |

Each stage:

| Key | Type | Notes |
|-----|------|-------|
| `id` | string | `weak`, `role`, `task`, `context` or `output`. |
| `label` | string | Shown on screen, e.g. `"+ Role"`. |
| `adds` | string or null | Part added at this stage (null for `weak`). |
| `prompt_segments` | array of `{text, part, new}` | Concatenated in order they equal `prompt`. `part` is `base`, `role`, `task`, `context` or `output`. `new: true` marks text added at this stage (highlighted). |
| `prompt` | string | Exact prompt sent to the model. |
| `guesses` | array of strings | What the AI is still forced to guess at this stage (shrinks each stage). |
| `change_note` | string | One line: what visibly changed in the output. |
| `output` | `{markdown}` | The AI output. The `output` stage must contain a pipe table. |

App step numbering for Demo 1 (one key press per step): `0` title, `1`-`5` the
five stages, `6` the side-by-side comparison. Six presses in total.

## `demo2`

| Key | Type | Notes |
|-----|------|-------|
| `title` | string | `"Trust but verify"`. |
| `prompt` | string | Same prompt for both files. |
| `payload` | string | The hidden instruction, verbatim. |
| `documents` | `{clean, injected}` | Previews extracted from the real `.docx` files (below). |
| `steps` | array, exactly 3 | `clean`, `injected`, `reveal`. |

Each document preview (extracted by `scripts/build_cache.py` from the actual file, so
the reveal shows what is really in it):

| Key | Type | Notes |
|-----|------|-------|
| `file` | string | Repo-relative path of the `.docx`. |
| `display_name` | string | On-screen name before the reveal (`Copy A` / `Copy B`). |
| `title_lines` | array of strings | Heading paragraphs. |
| `table` | `{columns, rows, total}` | Header, data rows and total row as strings. |
| `notes` | array of `{runs: [{text, hidden, color, size_pt}]}` | Note paragraphs. `hidden: true` marks a run a human cannot see (white or tiny). |

Each step: `{id, document, label, output: {markdown}}`. The `reveal` step has
`caption` (`"Both files look identical to a human reader."`) and `lesson` (array of
strings) instead of `output`; it shows both earlier outputs.

App step numbering for Demo 2: `0` title, `1` clean, `2` injected, `3` reveal.
Three presses in total.

## `presenter`

```
presenter.<demo1|demo2>.versions.<copilot|full|90s|45s> = {
  label, total,            // e.g. "Full", "4:00"
  cues: [ { step, at, seconds, say, do, ask } ]
}
```

- `step` is the app step number the cue belongs to. A compressed version may skip
  steps; the presenter view then says which key to press (`do`).
- `at` is the timing mark (`m:ss`) when the cue should start. `seconds` is its length.
  Cue lengths in each version add up to `total`.
- `ask` is an optional room question.
- `fallback` (Copilot live only): what to say and press if Copilot is slow or fails.
- `if_followed` / `if_resisted` (Demo 2 reveal, Copilot live only): the two endings,
  depending on whether Copilot followed the hidden line.

`copilot` ("Copilot live") is the default: the projector shows Copilot and the app is the
teleprompter and fallback. Demo 1 has `copilot` (4:00), `full` (4:00), `90s` and `45s`.
Demo 2 has `copilot` (1:30), `full` (1:30) and `45s`.

Every output panel shows where its answer came from (`Representative example`,
`Pre-generated · <model>` or `Recorded in Copilot · <date>`).

## Live mode contract (optional)

With `?live=1`, served by `scripts/live_server.py`, the app sends
`POST /api/generate` with `{"demo": "demo1", "stage": "<stage id>"}` or
`{"demo": "demo2", "step": "clean" | "injected"}` and expects
`{"markdown": "...", "model": "...", "latency_ms": 1234}`. Any error, non-200
response or a wait over 5 seconds falls back to the cached output, and the status
badge says so.
