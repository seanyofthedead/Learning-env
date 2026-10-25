# TASKS

Status values: todo / doing / done. Resume from the first task not marked done.
Re-read ASSUMPTIONS.md before resuming.

| ID | Phase | Role | Task | Status |
|----|-------|------|------|--------|
| 0.1 | 0 Setup | builder | Use existing git repo, create folder structure (app, data, demo2, scripts, copilot-kit) | done |
| 0.2 | 0 Setup | builder | Write TASKS.md with every task | done |
| 0.3 | 0 Setup | builder | Write ASSUMPTIONS.md | done |
| 0.4 | 0 Setup | builder | Write cache JSON schema in app/SCHEMA.md | done |
| 1.1 | 1 Concept | demo designer | CONCEPTS.md: 3 ladder concepts, 2 reveal concepts, skeptical-FM scoring, pick one of each | done |
| 2.1 | 2 Data | synthetic data designer | scripts/build_reports.py: stdlib-only generator for .csv/.xlsx/.docx with 25 lines and 5 planted variances | done |
| 2.2 | 2 Data | synthetic data designer | Generate data/ report files; verify they open (openpyxl/python-docx/LibreOffice render) | done |
| 2.3 | 2 Data | synthetic data designer | Write data/answer_key.md (outside the report files) | done |
| 3.1 | 3 Injected file | security demo builder | Build demo2 clean copies and INJECTED_demo_report_DO_NOT_USE.xlsx/.docx with simple hidden text | done |
| 3.2 | 3 Injected file | security demo builder | Render clean vs injected to images and confirm they look identical | done |
| 3.3 | 3 Injected file | security demo builder | Write demo2/REVEAL.md (exact location, how to show it) | done |
| 4.1 | 4 Prompts/cache | prompt engineer | Write the 5 ladder stages and Demo 2 prompt (content/demo1.json, content/demo2.json) | done |
| 4.2 | 4 Prompts/cache | prompt engineer | Author representative outputs; iterate until each stage is visibly better | done |
| 4.3 | 4 Prompts/cache | prompt engineer | scripts/build_cache.py (assemble cache.json, extract doc previews from real files) | done |
| 4.4 | 4 Prompts/cache | prompt engineer | scripts/regenerate_cache.py (live model calls at temperature 0) + shared model client | done |
| 5.1 | 5 App | front-end builder | app/index.html + app/app.js: Demo 1 ladder and side-by-side | done |
| 5.2 | 5 App | front-end builder | Demo 2 three-step flow with reveal | done |
| 5.3 | 5 App | front-end builder | Cache replay, embedded fallback for file://, optional live mode with 5 s fallback (scripts/live_server.py) | done |
| 5.4 | 5 App | front-end builder | Presenter view (P), separate presenter window, reset (R), themes; screenshot QA at projector sizes | done |
| 6.1 | 6 Script | presentation coach | Full scripts with timing marks (4:00 and 1:30), room questions | done |
| 6.2 | 6 Script | presentation coach | 90-second and 45-second compressed versions; cut until it fits | done |
| 7.1 | 7 Review | reliability engineer | scripts/preflight.py (+ headless app run) passing | done |
| 7.2 | 7 Review | integrity reviewer | scripts/inspect_files.py; inspect raw XML/metadata of all Demo 1 files; certify | done |
| 7.3 | 7 Review | skeptical NSA financial manager | Check every number, term, DoD FMR reference; fix findings | done |
| 7.4 | 7 Review | all three | REVIEW.md with sign-offs after fixes repeat clean | done |
| 7.5 | 7 Review | builder | README.md (setup, offline run, cache regen, day-of checklist, responsible Demo 2) | done |
| 7.6 | 7 Review | builder | copilot-kit (clean files, prompts list, rehearsal log template + 3-rehearsal rule) | done |
| 8.1 | 8 Report | builder | Run preflight three times, confirm identical results | done |
| 8.2 | 8 Report | builder | FINAL_REPORT.md | done |

## Phase 9: Microsoft 365 Copilot as the primary path (requested after Phase 8)

| ID | Phase | Role | Task | Status |
|----|-------|------|------|--------|
| 9.1 | 9 Copilot | synthetic data designer | Copilot-ready .xlsx: data as an Excel table (ExecutionReport, A5:L30); update integrity inspection | done |
| 9.2 | 9 Copilot | security demo builder | copilot-kit/RUNBOOK.md: tenant prep, pre-staged chats, click paths, live and fallback branches, injection-resisted branch | done |
| 9.3 | 9 Copilot | presentation coach + front-end builder | "Copilot live" presenter versions (4:00 / 1:30), default in presenter view; footer states where outputs came from | done |
| 9.4 | 9 Copilot | reliability engineer | check_copilot_run.py (judge a rehearsal) and import_copilot_run.py (recorded Copilot answers become the app fallback) | done |
| 9.5 | 9 Copilot | builder | README, REHEARSAL_LOG, ASSUMPTIONS, REVIEW addendum, FINAL_REPORT updated for Copilot-first | done |
| 9.6 | 9 Copilot | builder | Preflight three times, identical PASS; push | done |

## Phase 10: Same demo on any major LLM chat (requested after Phase 9)

| ID | Phase | Role | Task | Status |
|----|-------|------|------|--------|
| 10.1 | 10 Any chat | prompt engineer | Paste blocks for Demo 1 (prompt + report text, one file per stage), generated and checked | done |
| 10.2 | 10 Any chat | security demo builder | chat-kit/RUNBOOK.md: tool-agnostic run, reset checklist, pre-staged chats, Demo 2 copy-paste route | done |
| 10.3 | 10 Any chat | builder | chat-kit/TOOL_CARDS.md (ChatGPT, Claude, Gemini, Copilot) + REHEARSAL_LOG with tool column | done |
| 10.4 | 10 Any chat | reliability engineer | Generic check_chat_run.py / import_chat_run.py --source; app and cache label any tool; Copilot scripts become wrappers | done |
| 10.5 | 10 Any chat | presentation coach | "Any chat live" presenter versions (4:00 / 1:30) incl. copy-paste reveal | done |
| 10.6 | 10 Any chat | all three reviewers | Preflight/inspection extended; REVIEW addendum; README, ASSUMPTIONS, FINAL_REPORT; preflight x3; push | done |

## Phase 11: Presenter path with no Python (requested after Phase 10)

| ID | Phase | Role | Task | Status |
|----|-------|------|------|--------|
| 11.1 | 11 No Python | builder | Move scripts/ to tools/ (maintainers only); fix every reference; tools/README.md | done |
| 11.2 | 11 No Python | presentation coach | Printable presenter scripts (SCRIPT.md + SCRIPT.html) in chat-kit and copilot-kit, generated from content/presenter.json | done |
| 11.3 | 11 No Python | reliability engineer | Manual rehearsal checklist with plain pass/fail criteria; rehearsal logs use it | done |
| 11.4 | 11 No Python | builder | Runbooks, README, day-of checklist free of Python; maintainer steps marked optional | done |
| 11.5 | 11 No Python | all three reviewers | Preflight covers new files; REVIEW addendum; FINAL_REPORT; preflight x3; push | todo |
