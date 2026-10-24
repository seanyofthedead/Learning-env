# Runway: prompt-driven changes (proof of concept)

This adds a prompt bar to the client's `03_cr_scenario.html` ("Runway", the FY2027 CR scenario model). Analysts type a request such as *"Add a CR through Feb 28 at 95% of the FY26 rate"*. The page proposes the change, shows the before/after values and how the headline numbers move, and applies it only when the analyst clicks **Apply**. Every applied change goes in a change log and can be undone.

| File | What it is |
|---|---|
| `runway.html` | The client's page with the prompt bar added. It runs on its own in a browser. |
| `original_03_cr_scenario.html` | The file as received, for comparison. |
| `server/azure-openai-proxy.mjs` | A zero-dependency Node server that serves the page and forwards prompts to Azure OpenAI. |
| `test/e2e.mjs` | A browser test of the prompt bar (22 checks). Run it with `node test/e2e.mjs`. |

## The design rule: the model never produces a number

The page already kept data (`DATA`), calculations (`analyze()`) and display separate. The prompt bar works only on settings:

1. **One config object (`RUNWAY`)** holds everything a prompt may change. `fieldFor()` is the whitelist: each setting has a label, a type and an allowed range.
2. **The model returns operations, not answers.** `set`, `addScenario`, `removeScenario` and `show` (navigation).
3. **Every operation is validated** before the analyst sees it. Unknown settings, out-of-range values, dates outside FY2027, edits to built-in scenarios and weights that don't add up to 100% are refused, with the reason shown.
4. **The engine computes the impact.** The proposal card shows requests, anomaly total and (for lapse scenarios) unfunded payroll before and after. These figures come from `analyze()`, not from the model.
5. **Apply, then undo.** Applied changes go to the change log with before/after values, who answered (Claude, the client's model, or offline rules) and the time.

## What a prompt can change

| Area | Examples |
|---|---|
| Scenarios | Add a CR extension with any end date in FY2027 and its own funding rate; rename; remove added ones |
| Funding-rate switch | Add or remove rate options (50% to 150%) |
| Mandatory overlay | 070-1917 balance; assumed lapse length |
| Confidence scoring | The five weights (the rest rescale to keep 100%); margin days, weeks of data, burn-variation and coverage thresholds |
| Account inputs | FY26 enacted level, payroll share and law-enforcement share for each account |
| View | Show or hide ICE/CBP/TSA (filtering never changes any figure); sort order |
| Navigation | Open a scenario, the operating plan or the anomaly package |

Requests outside that list (new charts, layout, draft wording, moving the current CR end date, importing data) are answered with a short explanation and change nothing. Those belong in the product backlog, not the prompt bar.

## Where the answers come from

The page picks the first one available:

1. **The client's model.** If `window.RUNWAY_LLM = { endpoint }` is set, the prompt is POSTed there. `server/azure-openai-proxy.mjs` sets this and calls Azure OpenAI (works with Azure Government endpoints).
2. **Claude**, when the page is opened as a claude.ai artifact. The viewer is asked once to allow it.
3. **Offline rules.** A small built-in parser handles the example prompts, so the demo works without any model.

All three return the same JSON shape and go through the same validation:

```json
{"summary": "Adds a CR through Feb 28 at 95% of the FY2026 rate.",
 "ops": [{"op": "addScenario", "value": {"end": "2027-02-28", "rate": 0.95}}],
 "unsupported": null, "question": null}
```

## Next steps for a production build

- **Data in:** replace the embedded `DATA` with weekly extracts from FFMS, SAP and FSMS (Databricks Delta tables or Azure SQL), plus an upload path for the operating-plan workbook.
- **Saved and shared configs:** store each applied change server-side (Cosmos DB or Azure SQL) with the user's Entra ID, so the change log is an audit trail and scenarios can be shared.
- **Approvals:** require a second person to approve changes to scoring weights or account inputs before they affect the anomaly package.
- **Server-side validation:** run the same `applyOps()` checks on the server, not only in the browser.
- **Rebuild in React:** the current page is a fixed 1920×1080 presentation canvas, so it is small on phones. A responsive React rebuild keeps the look and works on any screen.
- **Evaluation set:** 50 to 100 real analyst requests with the expected operations, run against each model before an upgrade.
