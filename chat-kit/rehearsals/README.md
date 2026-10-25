# Rehearsal recordings (any chat tool)

**Synthetic demonstration data.** One folder per rehearsal, named `<YYYY-MM-DD>-<tool>`,
for example `2026-11-12-chatgpt/`. Paste each answer (the tool's Copy button) into:

`demo1_weak.md`, `demo1_role.md`, `demo1_task.md`, `demo1_context.md`, `demo1_output.md`,
`demo2_clean.md`, `demo2_injected.md`   (`.txt` also works)

```
python3 tools/check_chat_run.py  chat-kit/rehearsals/<folder> --source "<tool, model>"
python3 tools/import_chat_run.py chat-kit/rehearsals/<folder> --source "<tool, model>"
```
