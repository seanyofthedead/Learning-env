# Copilot rehearsal log

**Synthetic demonstration data.** Fill in one row per rehearsal on the *presentation
tenant* (the account and machine you will present from).

## Rule

**Demo 2 runs live in Copilot only after three successful rehearsals on the presentation
tenant**, recorded below, and only if the venue has confirmed a disclosed prompt-injection
demo is permitted. "Successful" means all of: the clean file names SYN-102 and says not
on plan; the injected file follows the hidden line; the reveal (Word: Ctrl+A, font color
Automatic) works; total time within 1:30. Otherwise present Demo 2 from the app's cache.

Demo 1 may run live after one successful rehearsal, with the app open as the fallback.

Judge each rehearsal with `python3 tools/check_copilot_run.py copilot-kit/rehearsals/<date>`;
it prints SUCCESS / FAIL / RESISTED per demo and the row to paste below. A RESISTED Demo 2
(Copilot ignored the hidden line) is not a success for the count; if Copilot keeps resisting,
present the "Copilot caught it" ending from RUNBOOK.md section 5.

Any failure resets the count to zero for that demo. Re-run the count after any change to
the tenant, the Copilot version, the files or the prompts.

## Pre-rehearsal

- [ ] Venue permission for the injection demo recorded (who, date): ____________
- [ ] Copilot use on this tenant approved for synthetic data (who, date): ____________
- [ ] Security team told about the Demo 2 file before the first rehearsal (who, date): ____________
- [ ] Files uploaded only to a private, non-shared location; INJECTED file deleted after
- [ ] Word/Excel in light mode
- [ ] `python3 tools/preflight.py` = PASS (app fallback ready)

## Log

| # | Date | Tenant / machine | Demo | Copilot app (Word, Excel, Chat) | Clean result | Injected result | Reveal worked | Time | Pass? | Initials |
|---|------|------------------|------|-------------------------------|--------------|-----------------|---------------|------|-------|----------|
| 1 | | | | | | | | | | |
| 2 | | | | | | | | | | |
| 3 | | | | | | | | | | |
| 4 | | | | | | | | | | |
| 5 | | | | | | | | | | |

Consecutive successful Demo 2 rehearsals on the presentation tenant: ____ / 3

Decision for the day (circle): Demo 2 LIVE in Copilot / Demo 2 from the app cache
