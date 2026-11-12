# Demo 3 answer key: subledger to general ledger reconciliation

Synthetic demonstration data. **Presenter only:** never put this file in front of the AI tool.

FY26 Q3, as of 30 June 2026. Subledger minus general ledger (GL). Dollars.

| Account | Subledger | General ledger | Difference |
|---|---:|---:|---:|
| 1730 Buildings, Improvements and Renovations | 1,803,500.00 | 2,131,500.00 | -328,000.00 |
| 1750 Equipment | 1,712,560.00 | 1,470,610.00 | 241,950.00 |
| 1820 Leasehold Improvements | 702,450.00 | 437,450.00 | 265,000.00 |
| **Total** | 4,218,510.00 | 4,039,560.00 | 178,950.00 |

## The five breaks

| # | Type | Account | Document(s) | Effect (SL - GL) | What it is | Research step |
|---|---|---|---|---:|---|---|
| B1 | Duplicate record | 1750 | D26-0117 | 1750: 186,400.00 | Same document and cost recorded twice in the property system (asset IDs PA-26-0117 and PA-26-0124, recorded 2 June and 26 June). The GL has it once. | Property team: confirm one physical generator and retire the duplicate record PA-26-0124. |
| B2 | Cutoff / timing | 1750 | D26-0125, D26-0126 | 1750: 114,250.00 | Acquired 29 and 30 June and recorded in the property system, but not posted in the Q3 GL. | Accounting: confirm the July postings; report as a timing difference, or accrue if material. |
| B3 | Missing property record | 1750 | D26-0158 | 1750: -58,700.00 | Utility truck posted to Equipment in the GL with no asset record in the property system. | Property team: locate and tag the truck and add the asset record, or reverse the posting if it isn't ours. |
| B4 | Transposition (keying error) | 1730 | D26-0133 | 1730: -63,000.00 | Roof replacement is 418,600.00 in the subledger and 481,600.00 in the GL. The 63,000.00 difference divides evenly by 9, the classic sign of transposed digits. | Accounting: check the invoice and correct the GL posting. |
| B5 | Misclassification | 1730 / 1820 | D26-0142 | 1820: 265,000.00; 1730: -265,000.00 | Leased suite 210 build-out is in 1820 Leasehold Improvements in the subledger but posted to 1730 Buildings in the GL. Equal and opposite differences; no net effect. | Accounting: reclassify 265,000.00 from 1730 to 1820 in the GL. |

Equipment (1750): 186,400.00 duplicate + 114,250.00 cutoff - 58,700.00 missing record = 241,950.00.
Buildings (1730): -63,000.00 transposition - 265,000.00 misclassification = -328,000.00.
Leasehold (1820): +265,000.00 misclassification. 1730 and 1820 offset: the total hides it.

## What a strong answer does

1. Account table with all three differences right (241,950.00; -328,000.00; 265,000.00).
2. Names all five breaks by document number, with the right reason.
3. Equipment: shows three items netting to 241,950.00 (the one people find hard by hand).
4. Spots that 1730 and 1820 offset (same document, wrong account), not two separate problems.
5. Notes the 63,000.00 difference divides by 9 (transposed digits), or names it a keying error.
6. Research list a reviewer can act on. It shouldn't claim to have fixed anything.

## Verify on stage

- Ctrl+F `D26-0117` in the subledger: two rows, same generator. That's the duplicate, checked by a person in five seconds.
- If the AI gets a total wrong, say so: that's the point. Select the Acquisition cost column in Excel and read the sum in the status bar.
