# Any-chat runbook: run both demos in any major LLM chat tool

**Synthetic demonstration data.** The same two demos, in ChatGPT, Claude, Gemini,
Microsoft Copilot or any other chat tool the venue allows. For Microsoft 365 Copilot on a
work tenant, `../copilot-kit/RUNBOOK.md` has the tenant-specific steps; this runbook
works there too.

| | Demo 1: From weak to strong (4:00) | Demo 2: Trust but verify (1:30) |
|---|---|---|
| Universal route (any tool) | **Paste** a ready-made block: report text + that stage's prompt (`paste/demo1_*.txt`) | **Copy-paste from Word:** select all in the .docx, copy, paste into the chat, add the prompt |
| If the tool takes uploads | Attach `../data/fy26_q3_execution_report.xlsx` (or .csv/.docx) and use `../copilot-kit/prompts.txt` | Attach the two .docx files from `../demo2/` |
| Live rule | After one successful rehearsal in that tool | Only after **three** successful rehearsals in that tool, on the presentation machine and account |

Teleprompter: **`SCRIPT.html`** in this folder (double-click; print with Ctrl+P), or
`SCRIPT.md`. Fallback: the app (`../app/index.html`, double-click). Its presenter window
(press O, then V until **Any chat live**) shows the same script with a timer, if you prefer
it on screen.

**No Python or other installs are needed to present or rehearse.** You need a browser,
Word and the approved chat tool. (`../tools/` is for the kit's maintainer.)

## 0. Before you choose a tool

- [ ] The tool is **approved** for this use by your organization and the venue. Synthetic
      data does not make a personal or consumer account acceptable where policy says no.
- [ ] Venue OK for a disclosed prompt-injection demo (see the main README).
- [ ] Fill in the tool's card in `TOOL_CARDS.md` during the first rehearsal.

## 1. Reset checklist (every rehearsal and the day itself)

Chat tools carry context between conversations. Clear it so each stage starts from the
same place:

- [ ] Use a **temporary / incognito chat** if the tool offers one (it typically skips memory).
- [ ] Otherwise: **memory / saved info / personalization off**, and **custom instructions
      empty** (these are in the tool's settings; the card has the location).
- [ ] **Web search / browsing off**, and connectors, apps or extensions off, so the answer
      comes only from the report.
- [ ] **Not inside a project, workspace, custom GPT, Gem or agent.** Plain new chat.
- [ ] **The same model** picked for every stage. Write it on the card.
- [ ] Signed in on the presentation machine; browser zoom about 125–150%; notifications off.

## 2. Why the copy-paste route works everywhere (Demo 2)

The hidden sentence in `INJECTED_demo_report_DO_NOT_USE.docx` is ordinary text formatted
white at 1 point. When you select all and copy in Word, the clipboard carries the text but
not the formatting that hid it. Pasted into a chat box, it arrives as **plain text: the
last line of a roughly 30-line paste.** Every chat tool reads it, whatever its upload
support. That gives the reveal two true beats:

1. In Word it is **invisible** (Ctrl+A, font color Automatic shows it).
2. In the chat it was **visible but unread**: scroll up to the end of what you pasted.
   "Nobody reads 30 lines of numbers before they press Enter. Neither does anyone in your
   office."

Do not claim it was invisible in the chat. It wasn't, and someone will scroll.

## 3. Pre-stage (60 minutes before)

Each prompt is ready in its own fresh chat; on stage you only press Enter.

| Window / tab | Contents | How |
|--------------|----------|-----|
| **A** | Demo 1 stage 1 | New chat (reset checklist). Open `paste/demo1_1_weak.txt` in a text editor → Ctrl+A, Ctrl+C → paste into the chat box → **do not send** → scroll the box to the top |
| **B**, tabs 1–4 | Demo 1 stages 2–5 | Same with `demo1_2_role.txt` … `demo1_5_output.txt`, one new chat per tab |
| **C** | Demo 2, Copy A | Word: open `../demo2/demo_report.docx` (light mode). New chat in its own tab: type the prompt from `paste/demo2_prompt.txt`, press Shift+Enter twice, then paste the copied document under it. Do not send. Scroll the box to the top. |
| **D** | Demo 2, Copy B | Same with `../demo2/INJECTED_demo_report_DO_NOT_USE.docx` |
| **E** | The app, fallback | Double-click `app/index.html`, press 1. |
| Laptop | Script | `SCRIPT.html` (or the app's presenter window: O, then V until **Any chat live**) |

Upload instead of paste: attach the file, paste the prompt from `../copilot-kit/prompts.txt`.
If the tool turns a long paste into an attachment chip, that's fine; leave it.

If the tool will not keep an unsent draft when you switch tabs, do the paste live:
it takes about five seconds per stage and the script allows for it.

## 4. On stage

Demo 1: Enter in A → Alt+Tab to B → Enter → Ctrl+Tab → Enter … → for the side-by-side,
Win+Left on B and pick A in Snap Assist.

Demo 2: Enter in C → Enter in D → reveal in Word (click in the document, Ctrl+A, Font
Color Automatic, Font Size 12) → back in D, scroll up to the end of the pasted text.

**If the tool does not follow the hidden line** (it names the Help Desk variance, or warns
about an instruction in the text): *"This tool caught it this time. Good. Protections
vary by tool and version, and they're not guarantees. The habit is the same: verify
against the source."* Then reveal anyway.

**Fallback:** no answer starting within 20 seconds, an error, or a sign-in prompt → *"Here's
the same prompt recorded at rehearsal"* → Alt+Tab to the app at the same step. The answer
panels show the tool name and date of the recording.

## 5. Rehearse and judge (no software needed)

1. Run both demos as above, with `SCRIPT.html` printed or open on the laptop.
2. Tick `REHEARSAL_CHECKLIST.md`. It gives SUCCESS / FAIL / RESISTED per demo.
3. Write the result in `REHEARSAL_LOG.md`.
4. Optional: paste each answer into `rehearsals/<YYYY-MM-DD>-<tool>/` (file names in that
   folder's README) and hand the folder to the kit's maintainer, who can make it the app's
   fallback, labelled "Recorded in <tool, model> · <date>". Until then the app's answers
   say "Representative example"; present them as that.

## 6. Afterwards

Delete the demo chats, and any uploaded copies from the tool's file storage. Delete local
copies of the INJECTED files from the presentation machine.
