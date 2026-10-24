# Copilot kit (optional)

**Synthetic demonstration data.** Use only if the venue permits Microsoft 365 Copilot.
The app in `../app` is the default and needs no network.

| File | Purpose |
|------|---------|
| `fy26_q3_execution_report.xlsx` / `.docx` | Clean Demo 1 report, byte-identical to `../data/` (checked by preflight). No hidden content (see `../REVIEW.md`). |
| `prompts.txt` | Every prompt, exactly as in the app, with which file to use. |
| `REHEARSAL_LOG.md` | Rehearsal record and the rule: Demo 2 runs live only after three successful rehearsals on the presentation tenant. |

The Demo 2 injected file is deliberately **not** in this folder; it lives only in
`../demo2` with `REVEAL.md`.

Live model output varies run to run and by tool version. Keep the app open as a
fallback, and say the app outputs are pre-generated if you switch to it.
