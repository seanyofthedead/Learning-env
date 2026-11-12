# Demo 3: reconcile the property subledger to the general ledger

Synthetic demonstration data. Requested by the client in the 12 November planning call: a
general ledger to subledger reconciliation for property accounts, run in Gemini (or any
approved chat tool that takes file uploads). About 5 minutes on stage.

**The story:** two reports that should agree and don't. The AI combines them, totals each
account, finds what's off and drafts a research list. People research, correct and sign.
Nothing is hidden in these files; every break is in the numbers.

## Files

| File | What it is |
|---|---|
| `property_subledger_fy26_q3.xlsx` / `.csv` | Property system extract: 40 asset records in 1730, 1750, 1820 |
| `general_ledger_fy26_q3.xlsx` / `.csv` | GL posting detail for the same accounts: 38 postings |
| `prompts.txt` | The demo prompt, the arithmetic follow-up and an optional weak contrast |
| `paste_block.txt` | Both files as text plus the prompt, for tools that can't take uploads |

The answer key is in `../data/recon_answer_key.md` (presenter only: never upload it).

## The five breaks (what a good answer finds)

| Account | Difference (SL - GL) | Explained by |
|---|---:|---|
| 1750 Equipment | 241,950.00 | duplicate generator record D26-0117 (+186,400), two assets bought 29-30 June not yet in the GL (+114,250), a truck in the GL with no property record D26-0158 (-58,700) |
| 1730 Buildings | -328,000.00 | roof D26-0133 keyed 481,600 instead of 418,600 (-63,000; divides by 9), suite 210 build-out D26-0142 posted to 1730 (-265,000) |
| 1820 Leasehold | 265,000.00 | the same build-out, which belongs here (+265,000): 1730 and 1820 offset |

## On stage

1. New chat. Attach both .xlsx files. Paste the prompt from `prompts.txt`. Send.
2. Read the account table, then the five breaks.
3. Verify by hand: open the subledger, Ctrl+F `D26-0117`, two rows. Five seconds.
4. Optional: the arithmetic follow-up in the same chat.
5. Close: it drafts the research list; your team researches, corrects and signs.

The full talk track and the scorecard are in `test-kit/TEST_GUIDE.html` (Demo 3 section).

Rebuild after editing `tools/recon_data.py`: `python3 tools/build_recon.py`, then
`python3 tools/build_test_guide.py`, `python3 tools/package_test_kit.py`, `python3 tools/preflight.py`.
