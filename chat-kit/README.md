# Any-chat kit

**Synthetic demonstration data.** Run both demos in any major LLM chat tool.

| File | Purpose |
|------|---------|
| `RUNBOOK.md` | Routes (paste or upload), reset checklist, pre-staging, on-stage steps, fallback, recording |
| `TOOL_CARDS.md` | Per-tool settings to clear and blanks to fill in at rehearsal (ChatGPT, Claude, Gemini, Copilot) |
| `paste/` | Demo 1 paste blocks (report + prompt, one per stage) and the Demo 2 prompt. Built by `tools/build_paste_blocks.py`; checked by preflight. |
| `REHEARSAL_LOG.md` | Per-tool log; Demo 2 live only after three successful rehearsals in that tool |
| `rehearsals/` | Recorded answers, judged by `tools/check_chat_run.py`, imported as the app fallback by `tools/import_chat_run.py` |

The injected files stay in `../demo2/` only.
