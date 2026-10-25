# Copilot kit (primary path)

**Synthetic demonstration data.** Both demos run live in Microsoft 365 Copilot. Start with
[`RUNBOOK.md`](RUNBOOK.md). The app in `../app` is the teleprompter and the fallback.

| File | Purpose |
|------|---------|
| `fy26_q3_execution_report.xlsx` / `.docx` | Clean Demo 1 report, byte-identical to `../data/` (checked by preflight). No hidden content (see `../REVIEW.md`). |
| `prompts.txt` | Every prompt, exactly as in the app, with which file to use. |
| `RUNBOOK.md` | Approvals, tenant prep, pre-staging, live steps, fallback, after-session clean-up. |
| `REHEARSAL_LOG.md` | Rehearsal record and the rule: Demo 2 runs live only after three successful rehearsals on the presentation tenant. |
| `rehearsals/` | Copilot answers saved from each rehearsal; judged by `tools/check_copilot_run.py`, imported as the app fallback by `tools/import_copilot_run.py`. |

The Demo 2 injected file is deliberately **not** in this folder; it lives only in
`../demo2` with `REVEAL.md`.

Copilot's answers vary run to run and by version. Keep the app open as the fallback and
say what it is when you switch ("the same prompt, recorded in Copilot at rehearsal").
