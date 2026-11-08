# Wedding venue search: Sean & Leila, November 2027

This folder holds the plan, budget model and research for finding a wedding venue near DC. It's a starting point for Codex or any other assistant.

**Current plan:** [approved budget and implementation](output/approved_budget.md), then [vendor fulfillment plan](output/fulfillment_plan.md). The couple approved the review changes on November 8, 2026. [approved_plan.json](budget/approved_plan.json) controls the current allocations; the workbook extract remains historical evidence.

For task instructions, use `CODEX_PROMPT.md` together with the approved plan and latest output files.

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
- Shop toward a complete $30,000 venue-driven bill; $31,139 is the maximum for a financial “fits” result with at least $1,000 headroom. An incomplete quote or unresolved requirement cannot establish an overall fit.
- First-choice date: Sat 13 Nov 2027.

Run the budget model's tests:

```
python3 wedding/budget/wedding_budget_model.py
```
