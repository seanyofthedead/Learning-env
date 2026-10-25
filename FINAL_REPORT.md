# FINAL REPORT

**Synthetic demonstration data.** Built 24 October 2026 for "AI and the Federal Financial
Manager: From Curiosity to Capability" (SDFM event, 19 November 2026). Updated the same
day to make **Microsoft 365 Copilot the primary path** (Phase 9).

## Outcome

Both demos are ready to run live in Microsoft 365 Copilot, with a tested runbook, a
teleprompter, and an offline fallback app. `tools/preflight.py` (223 checks) passes,
three runs, identical output. What cannot be done from here is the Copilot run itself:
that needs your tenant, your approvals and three rehearsals (see "What you must confirm").

## How it runs on the day

| | Demo 1: From weak to strong (4:00) | Demo 2: Trust but verify (1:30) |
|---|---|---|
| Projector | Microsoft 365 Copilot Chat, report .xlsx attached, five pre-staged chats (one Enter per stage), then two windows snapped side by side | Copilot in Word on the clean and injected .docx; reveal in Word (Ctrl+A → font color Automatic) |
| Laptop | App presenter window (O), **Copilot live** script with timing marks, room questions, fallback lines | Same, with both endings: Copilot followed the hidden line / Copilot caught it |
| Fallback | Alt+Tab to the app at the same step; it shows your recorded Copilot rehearsal, labelled with its date | Same; Demo 2 runs from the app if three successful rehearsals were not reached |

Full steps: `copilot-kit/RUNBOOK.md`.

## Any major LLM chat tool (Phase 10)

The same demos run in ChatGPT, Claude, Gemini, Microsoft Copilot or any approved chat tool
(`chat-kit/RUNBOOK.md`). Demo 1 uses one paste block per stage (report + prompt), so no
upload is needed. Demo 2 uses copy-paste out of Word: the hidden sentence is invisible in
Word and sits unread at the bottom of the paste in the chat. Every tool has a reset
checklist and a card to fill in at rehearsal. Recordings are labelled with the tool and
model that produced them, and the presenter window has an **Any chat live** script. Rule:
Demo 2 live in a tool only after three successful rehearsals in that tool.

## What was built

| Deliverable | Where |
|-------------|-------|
| Copilot runbook (approvals, tenant prep, pre-staging, live steps, fallback, clean-up) | `copilot-kit/RUNBOOK.md` |
| Prompts, rehearsal log with the three-rehearsal rule, rehearsal recordings folder | `copilot-kit/prompts.txt`, `REHEARSAL_LOG.md`, `rehearsals/` |
| Rehearsal judge and fallback importer | `tools/check_copilot_run.py`, `tools/import_copilot_run.py` |
| Copilot-ready report: data rows are an Excel table `ExecutionReport` (A5:L30), as Copilot in Excel requires | `data/*.xlsx` (and identical copies) |
| Demo app: Demo 1 ladder + side-by-side; Demo 2 three steps + red reveal; presenter view with Copilot live, Full, 90 s and 45 s scripts; source label on every answer | `app/` |
| Synthetic report (.csv/.xlsx/.docx), five planted variances, answer key outside the files | `data/` |
| Injected copies (white 1-pt sentence in Word, white cell A36 in Excel) and REVEAL.md | `demo2/` |
| Preflight, integrity inspection, script timing check, cache regeneration, live mode | `tools/` |
| Design, assumptions, sign-offs, tasks | `CONCEPTS.md`, `ASSUMPTIONS.md`, `REVIEW.md`, `TASKS.md` |

## Which model generated the cache

**None yet.** No model API key was available, and Copilot has no API this build could
call. The app's answers are **representative pre-generated outputs**, and every answer
panel says "Representative example". After your first good Copilot rehearsal, run
`tools/import_copilot_run.py`: the app then shows the answers Copilot actually gave,
labelled "Recorded in Copilot · <date>", and ASSUMPTIONS/cache record it.

## Key assumptions (full list in ASSUMPTIONS.md)

- Demo 1 in Copilot Chat (file attached, new chat per stage); Demo 2 in Copilot in Word.
- The injected file keeps the name `INJECTED_demo_report_DO_NOT_USE` on the tenant as you
  specified. Copilot can see file names and may be more cautious because of it.
- No hidden-text variants were written to get past Copilot's injection protections; the
  script has an honest "Copilot caught it" ending instead.
- The app is never to be presented as live Copilot. It labels its source on every answer.

## What you must confirm

1. **Venue rules (9–10 November NSA check):** a disclosed prompt-injection demo is
   permitted; whether it may run live in Copilot or only from the recording; whether the
   injected files may come on site and onto the presentation machine.
2. **Copilot on the presentation tenant:** Microsoft 365 Copilot licence, Copilot Chat file
   upload enabled (admins can turn it off), synthetic files approved, ideally a dedicated
   demo account with Copilot memory/personalization off.
3. **Security team sign-off before the first Demo 2 rehearsal.** Microsoft Defender can
   raise a cross-prompt-injection (XPIA) alert when Copilot reads the injected file.
4. **Three successful Demo 2 rehearsals on the presentation tenant**, logged. Copilot's
   protections may ignore the hidden line. If they do, the honest "Copilot caught it" ending
   is ready, but the "AI followed it" moment then exists only as a labelled recording,
   and only if some rehearsal produced it.
5. **File name on the tenant:** keep `INJECTED_demo_report_DO_NOT_USE` (current rule), or
   allow a neutral name for the tenant copy, which is more realistic but less safe. Your call.
6. **DoD FMR chapter titles** in `data/answer_key.md` (Volume 3, Chapters 6 and 8); the DoD
   site blocked automated checks. Not shown on screen.
7. **Which chat tool(s)** are approved for the session and for rehearsal, if not Copilot,
   and that a personal or consumer account is acceptable under your policy (synthetic data
   alone does not settle that).
8. **Projector check** per the README day-of checklist, including Copilot zoom (about
   125–150%) so answers read from the back of the room.
