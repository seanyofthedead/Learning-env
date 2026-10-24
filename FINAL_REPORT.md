# FINAL REPORT

**Synthetic demonstration data.** Built 24 October 2026 for "AI and the Federal Financial
Manager: From Curiosity to Capability" (SDFM event, 19 November 2026).

## Outcome

Both demos are built, reviewed and passing. `scripts/preflight.py` was run three times
on the final build: **PASS** each time, with byte-identical verbose output (175 checks,
output hash `41d14b86adc404e0`) and no change to the repository.

## What was built

| Deliverable | Where | Notes |
|-------------|-------|-------|
| Demo app | `app/index.html`, `app/app.js`, `app/cache.json` | No build step. Opens from disk or `python -m http.server`. Cache schema in `app/SCHEMA.md`. |
| Demo 1, "From weak to strong" | app, key 1 | Title card + 5 ladder stages (weak → +Role → +Task → +Context → +Output) + side-by-side with the leadership table as a real HTML table. The new prompt words are highlighted green; a "What the AI has to guess" list loses one item per stage. |
| Demo 2, "Trust but verify" | app, key 2 | Title card + 3 presses: clean copy and correct answer; identical-looking copy and wrong answer; red reveal of the hidden line beside both answers under "Both files look identical to a human reader." |
| Presenter view | key P (or O for its own window) | Exact script per step, timing marks and a running timer, room questions, Full (4:00 / 1:30), 90 s and 45 s versions (V), reset (R). Every cue checked to fit at a calm speaking pace. |
| Synthetic report | `data/fy26_q3_execution_report.{csv,xlsx,docx}` | 25 `SYN-` lines; plan, obligations, expenditures; five planted variances (late contract award, one-time equipment buy, reprogramming, billing lag, duplicate posting). Totals look "on plan" (+1.5%) because the variances offset: the trap the weak prompt falls into. |
| Answer key | `data/answer_key.md`, `.json` | Kept out of the report files. |
| Injected copies | `demo2/INJECTED_demo_report_DO_NOT_USE.{xlsx,docx}` | One benign hidden sentence in white (1 pt in Word, cell A36 in Excel). Renders pixel-identical to the clean copy. Documented in `demo2/REVEAL.md`. |
| Preflight | `scripts/preflight.py` | Runs both demos headlessly through the app's own code; prints PASS or the first failure. Negative-tested. |
| Integrity inspection | `scripts/inspect_files.py` | Raw XML and metadata of every file; certifies Demo 1 files clean. |
| Cache regeneration and live mode | `scripts/regenerate_cache.py`, `scripts/live_server.py` | Standard library only. Live mode falls back to the cache on any error or after 5 s. |
| Copilot kit (optional) | `copilot-kit/` | Clean files, prompt list, rehearsal log with the three-rehearsal rule for Demo 2. |
| Docs | `README.md`, `CONCEPTS.md`, `REVIEW.md`, `ASSUMPTIONS.md`, `TASKS.md` | Setup, day-of checklist, responsible Demo 2 guidance, design choices, sign-offs. |

## How to run it

```
# on the presentation laptop, no network needed
open app/index.html                  # or: python -m http.server 8000 --directory app
python3 scripts/preflight.py         # must print PASS
```

Keys: → / PageDown next, ← back, 1 / 2 demos, P presenter, O presenter window, V script
version, End last step, R reset, T theme. Full checklist in `README.md`.

## Which model generated the cache

**None.** No project model API key (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`) was present.
The cached outputs are **representative pre-generated outputs** written for this demo;
the cache, the presenter view and the script say so. To use real model output, run
`scripts/regenerate_cache.py` with a key, then preflight. It records the model and
temperature used.

Note on temperature 0: since Anthropic API version 2026-10-21, current Claude models
accept only their default sampling. The script asks for temperature 0, falls back to the
default if refused, and records which was used (ASSUMPTIONS.md A11).

## Key assumptions (full list in ASSUMPTIONS.md)

- Kept the existing git repo instead of `git init` (it held two unrelated guides).
- Office files are written with Python's standard library, so every byte is inspectable
  and builds are repeatable.
- "Variance against plan" includes the expenditure plan, so the billing lag counts.
- Before the reveal, on-screen file names are "Copy A" / "Copy B". When a model is
  called, both files are sent under a neutral name so the safety label doesn't tip it off.
- The representative injected answer names the second-largest variance as largest and
  says "on plan": what the hidden line produces when followed literally.
- Supported screens: 1280x720 and up, light and dark, 18px minimum text.

## What you must confirm

1. **Venue rules for a live injection demo.** At the 9–10 November NSA check, confirm
   whether a disclosed prompt-injection demonstration is permitted, and whether it may
   run live or only from the app's cache. Also confirm the injected files may be brought
   onto the premises and the presentation machine.
2. **Whether the Microsoft 365 Copilot path is permitted** at the venue and on the
   presentation tenant. If yes, follow `copilot-kit/REHEARSAL_LOG.md`: Demo 2 runs live
   only after three successful rehearsals on that tenant.
3. **Real model output (recommended).** Run `scripts/regenerate_cache.py` with an
   approved model before the event so on-screen answers are real model output, then
   re-run preflight. If the model resists the hidden line, decide whether to present
   that honestly or keep the representative cache.
4. **DoD FMR chapter titles** in `data/answer_key.md` (Volume 3, Chapters 6 and 8). The
   DoD Comptroller site blocked automated checks. They are not shown on screen.
5. **Projector check:** run the day-of checklist in `README.md` on the venue projector
   (far-corner legibility of the Demo 1 table and the Demo 2 red line; theme choice).
