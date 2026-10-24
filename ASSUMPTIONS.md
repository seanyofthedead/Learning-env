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
  the builder, and `scripts/regenerate_cache.py` is provided to regenerate them with a key.
- A3. Office files (.xlsx/.docx) are written with Python's standard library only (`zipfile` +
  hand-written XML) so the files contain nothing a library might add silently, the integrity
  review can read every byte, and builds are byte-for-byte repeatable (fixed zip timestamps).
  `openpyxl`/`python-docx`/LibreOffice were used only during development to verify the files
  open; they are not needed to run anything.
