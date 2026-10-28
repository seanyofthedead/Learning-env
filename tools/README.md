# tools/: for whoever maintains the kit

**Presenters never need anything in this folder.** Presenting needs a browser, Word and
the approved chat tool. Everything here builds or checks the kit's files. It needs Python 3.8+
(standard library only) and, for one check, Node.js.

| When | Run | What it does |
|------|-----|--------------|
| After changing the report data (`report_data.py`) | `python3 tools/build_reports.py` | Rebuilds the .csv/.xlsx/.docx files (data/, demo2/, copilot-kit/), byte-for-byte repeatable |
| After changing prompts, outputs or presenter text (`../content/`) | `python3 tools/build_cache.py` | Rebuilds `app/cache.json` and the copy embedded in `app/index.html` |
| Same | `python3 tools/build_paste_blocks.py` | Rebuilds `chat-kit/paste/` |
| Same | `python3 tools/build_ladder.py` | Rebuilds `DEMO1_LADDER.html` in both kits |
| Same | `python3 tools/build_presenter_scripts.py` | Rebuilds the printable scripts (`SCRIPT.md`, `SCRIPT.html`) in both kits |
| Before handing the kit over, and after any change | `python3 tools/preflight.py` | Everything that must be true on the day; prints PASS or the first failure |
| To hand the kit to a presenter | `python3 tools/package_kit.py release` | Writes `release/SDFM_AI_demo_kit.zip` (committed; preflight checks it is current): both kits, Demo 2 files, fallback app, report files, START_HERE.txt; no Python inside |
| To audit the files | `python3 tools/inspect_files.py` | Raw XML and metadata of every file; certifies no hidden content in Demo 1 material |
| After editing presenter text | `python3 tools/check_script_timing.py` | Every cue fits its time slot at a calm speaking pace |

Optional, after a rehearsal (presenters can use the paper checklist instead):

| Run | What it does |
|-----|--------------|
| `python3 tools/check_chat_run.py <folder> --source "<tool, model>"` | Grades pasted rehearsal answers with the same rules as preflight |
| `python3 tools/import_chat_run.py <folder> --source "<tool, model>"` | Makes that rehearsal the app's labelled fallback |
| `check_copilot_run.py`, `import_copilot_run.py` | The same, with the source set to Microsoft 365 Copilot |

Optional, needs a model API key and network:

| Run | What it does |
|-----|--------------|
| `python3 tools/regenerate_cache.py` | Replaces the app's answers with a real model's output (records model and temperature) |
| `python3 tools/live_server.py` | Serves the app with live mode (`?live=1`), falling back to saved answers after 5 s |

Supporting modules: `report_data.py` (the single source of report numbers), `office_text.py`,
`output_checks.py`, `chat_run.py`, `model_client.py`, `headless_run.js`.
