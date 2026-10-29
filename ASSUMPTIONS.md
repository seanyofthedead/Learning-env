# ASSUMPTIONS

Decisions made without asking. Each is reversible.

## Environment and repo
- A1. The workspace was not empty: it already held a git repo with two unrelated guides
  (`autonomous-claude-code.md`, `mobile-claude-code-features.md`). I kept them and the
  existing branch instead of re-running `git init`. The project lives at the repo root.
- A2. Model API key check: no `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` or `AZURE_OPENAI_API_KEY`
  was present. The sandbox exposes internal variables (`API_KEY`, `ANTHROPIC_BASE_URL`) that
  belong to the build tool itself, not to this project; I did not treat them as a project model
  key. Therefore all cached outputs are **representative pre-generated outputs** authored by
  the builder, and `tools/regenerate_cache.py` is provided to regenerate them with a key.
- A3. Office files (.xlsx/.docx) are written with Python's standard library only (`zipfile` +
  hand-written XML) so the files contain nothing a library might add silently, the integrity
  review can read every byte, and builds are byte-for-byte repeatable (fixed zip timestamps).
  `openpyxl`/`python-docx`/LibreOffice were used only during development to verify the files
  open; they are not needed to run anything.

## Data
- A4. Report figures are in $K, cumulative FY26 through 30 June 2026 (end of Q3). Codes
  use the made-up prefix `SYN-`; the directorate is "Demonstration Directorate". O&M is
  treated as a one-year appropriation expiring 30 September 2026.
- A5. "Variance against plan" covers both the obligation plan and the expenditure plan,
  so the billing lag (obligations on plan, expenditures far behind) counts. This is
  written down in `data/answer_key.md`.
- A6. The one-time equipment buy is workstations below the expense/investment threshold
  so that it is legitimately O&M; a skeptical FM would otherwise flag it as Procurement.
- A7. The CSV uses plain numbers (no thousands separators) for machine-readability; the
  .xlsx stores real numbers with formulas for variances and totals; the .docx shows
  formatted strings. All three hold identical values.

## Demo 2
- A8. A clean copy of the report sits in `./demo2/demo_report.*` (byte-identical to
  `./data/`) so both Demo 2 files can be opened side by side. Hidden text uses the
  simplest technique: white font (and 1-pt size in Word).
- A9. On screen the files are called "Copy A" and "Copy B" until the reveal, which
  shows the real file name. When a model is called, both files are sent under the
  neutral name `demo_report.docx` so the safety label in the file name does not tip
  off the model.
- A10. The representative injected output names the *second*-largest variance as the
  largest and says execution is on plan. That is what "ignore the largest variance"
  produces when followed literally, and it is more instructive than a blank answer.
  Live models may or may not follow the hidden line; the presenter script says so.

## Model calls
- A11. Temperature: since Anthropic API version 2026-10-21 (three days before this
  build) sampling parameters are removed, and current Claude models accept only their
  default sampling. `tools/model_client.py` asks for temperature 0 (using the older
  `2023-06-01` API version header), retries once without it if the model refuses, and
  records the temperature actually used in `cache.json` and ASSUMPTIONS.md.
- A12. Model calls use Python's `urllib` rather than a vendor SDK, to keep the "standard
  tooling only, no dependencies" rule. Default model when `ANTHROPIC_API_KEY` is set:
  `claude-opus-5-5` (override with `DEMO_MODEL`). `OPENAI_API_KEY` + `DEMO_MODEL` is also
  supported, to stay tool-agnostic.
- A13. The model receives the report as text: the CSV export for Demo 1 (same data as
  the .xlsx shown on screen) and the text extracted from the .docx for Demo 2 (which
  includes the hidden run, as any text extractor would).

## App
- A14. The app opens straight from disk (`file://`), where browsers block `fetch()`, so
  `tools/build_cache.py` embeds a byte-identical copy of `cache.json` inside
  `index.html`. Over HTTP the app fetches `cache.json` and falls back to the embedded copy.
  Preflight fails if the two differ.
- A15. Live mode is opt-in (`?live=1`) and needs `tools/live_server.py`, which keeps the
  API key server-side. The browser aborts after 5 s and shows the saved output, labelled.
- A16. Supported screens: 1280x720 and up. Verified with no clipped content at 1280x720,
  1280x800, 1366x768 and 1920x1080, light and dark. Body text never drops below 18px. On
  screens 740px tall or less the footer is hidden; the header pill keeps the
  "Synthetic demonstration data" label on screen.
- A17. Demo 1 = 6 key presses (5 ladder stages + side-by-side) after a title card; Demo 2 =
  3 key presses after a title card. Clicker PageDown/PageUp map to next/previous.

## Copilot-first (Phase 9, after you said "This must be run in Copilot")
- A18. Microsoft 365 Copilot is now the primary path; the app is the fallback and the
  presenter teleprompter. Original rules still hold: Demo 2 runs live only after three
  successful rehearsals on the presentation tenant.
- A19. Every .xlsx now holds the 25 data rows as an Excel table named `ExecutionReport`
  (A5:L30). Microsoft's guidance says Copilot in Excel needs an Excel table or a range
  with a single header row, and our sheet has title rows above the header. Totals and
  notes sit outside the table. Clean and injected copies still render identically.
- A20. Demo 1 runs in Microsoft 365 Copilot Chat with the .xlsx attached (one new chat per
  stage, pre-staged). Demo 2 runs in Copilot in Word on the two .docx files, so the
  reveal can be done in the same Word window.
- A21. The injected file keeps its required name `INJECTED_demo_report_DO_NOT_USE` on the
  tenant too. Copilot can see file names, and the name may make it more cautious. I did not
  rename it, because the name is a safety label you specified; whether a tenant copy
  may use a neutral name is your call (FINAL_REPORT).
- A22. I did not write variants of the hidden text designed to get past Copilot's
  prompt-injection protections. If Copilot ignores the hidden line, the script has a
  "Copilot caught it" branch that is still a true lesson.

## Any chat tool (Phase 10)
- A23. Universal routes: Demo 1 by pasting a ready-made block (report CSV text + prompt);
  Demo 2 by copying the Word document into the chat. Uploads are used where a tool supports
  them, but nothing depends on uploads.
- A24. With copy-paste, the hidden sentence arrives as plain text, the last of about 30
  pasted lines. It is visible in the chat if anyone scrolls. The script says so and turns it
  into the second beat of the reveal ("visible but unread"), never claiming it was invisible
  there.
- A25. Tool cards name the settings to clear, not exact click paths, because menus change
  often. Whether each tool follows the hidden line is left blank until a real rehearsal.
- A26. The three-rehearsal rule applies per tool, machine and account. A recording is
  labelled with the tool and model given by `--source`; the app never shows a recording
  under another tool's name.

## Presenter path without Python (Phase 11)
- A27. The `scripts/` folder your original spec named was moved to `tools/` and marked
  maintainers-only, so presenters can ignore it. `tools/preflight.py` is the same file.
  Presenting needs only a browser, Word and the approved chat tool.
- A28. A downloadable copy of the presenter kit is committed as
  `release/SDFM_AI_demo_kit.zip` (built by `tools/package_kit.py release`; preflight fails if it
  is out of date). It contains copies of the Demo 2 files, so "INJECTED files live only in
  ./demo2" now means: loose files only in ./demo2, plus that packaged copy.
- A29. The GitHub repository is public, so everything pushed, including the INJECTED
  files, is publicly visible. Making it private is the owner's decision (see FINAL_REPORT).

## Live-demo optimization (Phase 13)
- A30. The strong prompt now ends with one added sentence: "The Director will read this in
  30 seconds: start with a one-sentence bottom line, then the table, with no more than 12
  words per cell and nothing else." Your original wording is otherwise unchanged and kept
  in `tools/build_cache.py` as `ORIGINAL_STRONG`. Reverting is a one-line change.
- A31. Live on stage, Demo 1 runs three prompts (stages 1, 4 and 5); the app and the ladder
  page keep all five stages. Your room question "what is the AI being forced to guess here?"
  stays, asked after the weak answer.
- A32. Demo 2 adds a follow-up prompt asking the AI to quote every sentence outside the table.
  It asks the AI to report the hidden line, not obey it; the hidden line itself is unchanged.
- A33. The representative weak answer was rewritten to match what modern models produce
  (competent but long), so the app no longer overstates how bad a weak prompt is.
