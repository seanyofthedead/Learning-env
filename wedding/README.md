# Wedding venue search: Sean & Leila, November 2027

This folder holds the plan, budget model and research for finding a wedding venue near DC. It's a starting point for Codex or any other assistant.

**Start here:** paste `CODEX_PROMPT.md` into Codex. It has the locked decisions, budget rules, leads found so far, and the next steps.

| Path | What it is |
|---|---|
| `CODEX_PROMPT.md` | The prompt for resuming the work |
| `budget/` | The budget model, the 10 categories and line items, and the excluded-venue list |
| `specs/` | Venue inputs for the budget model, one folder per search |
| `data/` | Research results from rounds 2 and 3, with sources |
| `plan/` | The full plan: budget explanation, agent design, timeline |
| `leila_page/` | Source of Leila's planning page (it runs only on claude.ai) |

**Key numbers:**
- 185 guests.
- $60,000 total, which includes a 10% reserve, so the spend limit is $54,545.
- The venue, food, drink and rentals must come to $32,139 all-in or less.
- First-choice date: Sat 13 Nov 2027.

Run the budget model's tests:

```
python3 wedding/budget/wedding_budget_model.py
```
