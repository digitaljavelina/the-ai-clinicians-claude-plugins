# PHI Redactor (Claude Code skill)

phi-redactor removes patient information from a clinical note before you send it
anywhere. You give it a note (text, PDF, Word, Excel, or PowerPoint) and get back a copy with names,
dates, record numbers, phone numbers, and addresses replaced by plain labels like
`[NAME]` or `[DATE]`. It is built on Microsoft Presidio, an open-source
de-identification framework, which runs two kinds of detectors together: fixed
pattern rules that reliably catch structured items like Social Security and record
numbers, and a specialized AI model called `obi/deid_roberta_i2b2`, trained on real
medical de-identification data, that spots names and dates buried in sentences. It
deliberately errs toward blanking out too much, since a missed identifier is what
causes harm.

To check that it works, we ran it on fake patient notes that each had a known list
of identifiers planted in them, then counted how many it caught. The AI model
removed every one, 120 out of 120 in the test set, while the pattern-only version
caught about 88 percent and tended to miss names written into sentences and
facility names. Those numbers come from synthetic notes, so still skim each result
before trusting it.

Here is the part that matters for privacy: that AI model runs on your own computer.
It is a local program, not an online service, so it never sends your note across
the Internet to a server to be read. The tool is locked into offline mode while it
works, and we confirmed it runs the same with Wi-Fi turned off. The only time the
Internet is used at all is a one-time download when you install it. So when you
later share a note with Claude, the only version that leaves your machine is the
copy that already has the patient details removed.

## Do I need to install Python or anything technical?

No. You do not need to install Python, and you do not need to know what a terminal
is. This works the same on Windows and Mac. The one helper it uses (a tool called
uv) fetches the correct Python and everything else on its own, and Claude will
install that helper for you if it is not already there. You never type a command.

## Install it (the easy way, for everyone)

1. Open Claude Code (the app or the extension is fine, you do not need a terminal).
2. Give it this zip file and say, in your own words:

   > Install the skill in this zip file: `phi-redactor.zip`

3. Let it work. Claude installs the helper if needed, sets up its own Python, and
   **downloads the AI models in the background.** This one-time setup can take
   several minutes and needs an internet connection. You can keep chatting or step
   away; it only happens once, and after that the tool runs offline.

That is the whole install. Then just ask, for example:

> Redact the PHI in the file on my Desktop called note.pdf

Claude figures out where the file is and hands you back a redacted copy.

## Install it by hand (only if you want to)

You never have to do this; the easy way above covers it. If you prefer to run it
yourself, you need [uv](https://docs.astral.sh/uv/) (install commands for every OS
are on the uv site). Then, from a terminal:

```bash
# macOS / Linux
mkdir -p ~/.claude/skills
unzip phi-redactor.zip -d ~/.claude/skills/
cd ~/.claude/skills/phi-redactor
uv run scripts/bootstrap.py          # one-time setup, downloads the models
uv run redact.py inputs/sample_note.txt
```

```powershell
# Windows (PowerShell)
mkdir $HOME\.claude\skills -Force
Expand-Archive phi-redactor.zip -DestinationPath $HOME\.claude\skills\
cd $HOME\.claude\skills\phi-redactor
uv run scripts/bootstrap.py          # one-time setup, downloads the models
uv run redact.py inputs/sample_note.txt
```

The redacted copy lands in `outputs/sample_note.redacted.txt`.

## Using it

You do not type any commands. You talk to Claude in plain language and it runs
everything for you. For example:

- "Here is a PDF of a clinical note. Redact the PHI." → Claude gives you back a
  clean copy.
- "Redact this note, summarize it, then reverse the redaction." → Claude strips the
  PHI, does the summary on the safe version, and puts the real details back at the
  end, all on your machine.

The first time you use it, Claude runs a one-time setup on its own (that is the
model download). After that it is ready. The clinical engine is the default and the
output is plain text.

Under the hood Claude is running commands like `uv run redact.py <file>` and
`uv run unredact.py <file> --map <key>`. You never have to. They are documented
here only so a curious user can see what is happening.

## Reversible mode: redact, process somewhere else, then restore

Normally the tool is one-way: every name becomes `[NAME]`, so there is no way
back. Reversible mode is for a different job. You want to strip the PHI out of a
note, run the safe version through a task, then put the real details back into the
result. You do not manage any of this yourself. You just tell Claude, in plain
words, something like "redact this note, summarize it, then reverse the redaction,"
and Claude runs the whole sequence for you.

Here is what Claude does behind the scenes. It makes a safe copy of the note in
which each identifier becomes a unique tag like `[[NAME_1]]` or `[[DATE_2]]` (the
same person is the same tag throughout, so the text still reads sensibly), and it
writes a small key file that records which real value each tag stands for. It does
the task on the safe copy only, keeping the tags in place, then uses the key to put
the real values back at the end. The key never leaves your machine, and the real
identifiers are never shown to the task step.

**Where is the key kept?** On your computer, next to the redacted copy. By default
that is the skill's own `outputs/` folder, as `outputs/<name>.redacted.map.json`
(for example `~/.claude/skills/phi-redactor/outputs/note.redacted.map.json`). It is
an ordinary local file. It is never uploaded, and it is the one file you must not
share, because it is what re-links the tags to real people. Once a restore looks
right, the key can be deleted; ask Claude to remove it and the link is gone.

Two things to keep in mind. While the key exists, the note is pseudonymized, not
fully de-identified, so the key file deserves the same protection as the original
note. And restoring depends on the task step leaving the `[[...]]` tags intact. If
something rewrites or drops them, Claude's round-trip check catches it and tells
you exactly which values could not be put back, rather than failing silently.

## Read the result, do not just trust it

- **Open the redacted file and skim it.** Over-redaction (an ordinary word tagged)
  is harmless. A missed identifier is not. No redactor is perfect on a chart
  format it has never seen.
- **If you see a WARNING**, the tool thinks an identifier-shaped fragment survived
  (usually a PDF that wrapped an email or phone number across two lines). Open that
  file and fix it by hand. For sensitive work, feed plain `.txt` rather than `.pdf`.
- **Scanned PDFs (pictures of pages) are refused**, not silently passed through. If
  a PDF has no real text in it, run OCR first.
- **Excel and PowerPoint have blind spots.** The tool reads cell values, sheet
  names, text boxes, tables, and speaker notes. It does not read embedded charts,
  cell comments, or slide headers/footers, so check those by hand if a file might
  hide identifiers there.

## Prove it works

The bundled lab generates fake patient notes (with Faker, never real data) and
measures how much PHI each engine removes:

```bash
uv run evaluate.py --engine both     # baseline vs clinical recall, side by side
uv run evaluate.py --sample          # look at one fully redacted fake note
```

Watch the name rows. The general model leaks names in prose; the clinical model
catches them. That gap is the whole reason the clinical engine is the default.

A full end-to-end run, 25 fake files across all six formats through both engines
and both modes, with recall, extraction coverage, and reversible round-trip
results, is written up in [TEST_REPORT.md](TEST_REPORT.md).

## What is in the box

```
SKILL.md          instructions Claude follows to install and run this
redact.py         redact a real document (the tool you use)
unredact.py       restore originals after reversible redaction
engine.py         the redaction engine (Presidio + clinical NER + regex)
scripts/bootstrap.py   one-time installer (downloads the models, once)
notes.py          synthetic fake-PHI note generator (for the lab)
evaluate.py       recall scoring harness (for the lab)
TEST_REPORT.md    results of a full end-to-end test run
inputs/sample_note.txt   a fake note to try it on
pyproject.toml, uv.lock  pinned dependencies
```

## Requirements and notes

- **Windows and Mac.** Runs the same on Windows 10/11 (64-bit) and macOS. No Python
  install needed: uv fetches the correct Python (3.14) and every dependency itself.
  (Windows on ARM is the one gap, since a required piece may lack a wheel there.)
- **No manual setup for the user.** The only helper is uv, and Claude installs it
  for you if it is missing. You never touch a terminal or install Python.
- **Disk and first download:** PyTorch and the models total a few gigabytes and
  download in the background on first setup. This is normal for a local AI model.
- **Offline after setup:** the first run downloads the models into shared caches on
  your machine. After that it runs without a network, and the downloads are not
  repeated even if the environment is rebuilt.
- **Fake data only in this package.** The sample note and everything the lab
  generates are invented. Never commit real patient data into this folder.
