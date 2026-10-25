# Rehearsal recordings

**Synthetic demonstration data.** One folder per rehearsal, named by date, for example
`2026-11-12/`. In it, paste each Copilot answer (Copilot's **Copy** button) into its own
file:

| File | Answer to |
|------|-----------|
| `demo1_weak.md` | Stage 1, "Summarize this report." |
| `demo1_role.md` | Stage 2, + Role |
| `demo1_task.md` | Stage 3, + Task |
| `demo1_context.md` | Stage 4, + Context |
| `demo1_output.md` | Stage 5, the strong prompt |
| `demo2_clean.md` | Demo 2 prompt on `demo_report.docx` |
| `demo2_injected.md` | Demo 2 prompt on `INJECTED_demo_report_DO_NOT_USE.docx` |

`.txt` works too. Tables pasted as tab-separated text and Copilot's citation markers are
handled automatically.

```
python3 tools/check_copilot_run.py copilot-kit/rehearsals/2026-11-12    # judge the run
python3 tools/import_copilot_run.py copilot-kit/rehearsals/2026-11-12   # make it the app fallback
```
