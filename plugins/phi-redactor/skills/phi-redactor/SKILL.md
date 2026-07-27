---
name: phi-redactor
description: >-
  De-identify PHI in clinical text and documents. Removes patient and provider
  names, dates, MRNs, SSNs, phone numbers, addresses, emails, account/device/ID
  numbers, and other identifiers, replacing each with a category tag like [NAME]
  or [DATE]. Uses Microsoft Presidio plus a clinical NER transformer
  (obi/deid_roberta_i2b2) by default, which catches names in free-text prose that
  general models miss. Reads .txt, .md, .pdf, .docx, .xlsx, and .pptx; writes a
  redacted .txt.
  Use whenever the user asks to redact, de-identify, anonymize, scrub, or remove
  PHI / patient identifiers from a note, chart, report, or transcript. Also offers
  a reversible mode that writes a local key so the text can be de-identified,
  processed by another tool, and then restored (redact, process, un-redact).
---

# PHI Redactor

Runs a local de-identification pipeline. The document is read by models that run
on this machine, in-process; it is never sent to a remote service. Over-redaction
is the intended bias, a missed identifier is a breach, so the tool errs toward
removing too much and warns when something identifier-shaped survives.

**Offline guarantee.** `redact.py` forces the model libraries into offline mode
(`HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`) before they load, so a redaction run
cannot make any network call, not even the model-version check. The only step
that uses the network is the one-time `bootstrap.py` download. To prove it, run a
redaction with the network off; it still works. If setup has not run, `redact.py`
stops with a clear message rather than downloading anything on its own.

## How you operate this (the user never types commands)

The user speaks in plain language, for example: "here is a PDF clinical note,
redact the PHI, summarize it, then reverse the redaction." YOU run every command
with Bash on their behalf. Never ask them to run `uv`, open a terminal, or type a
path. Just do it and report back in plain language.

- **Assume a total beginner.** They may never have used a terminal and may have no
  Python installed. That is fine. They do not need Python (uv fetches its own), and
  they do not install anything by hand. You do all of it.
- **Install uv if it is missing.** Run `uv --version`. If that fails, install uv
  yourself, then continue:
  - macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows (PowerShell): `powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **Auto-setup.** Before the first redaction, check for `.installed` in this
  folder. If it is missing, run `uv run scripts/bootstrap.py` yourself. Tell the
  user that setup is downloading the AI models in the background, that this is a
  one-time step that can take several minutes, and that they can keep chatting or
  step away. Do not make them do it.
- **Pick the mode from intent.** If they only want a clean copy, run one-way
  (no flag). If they want to do a task and then get the real details back
  ("un-redact", "reverse it", "put the names back", "redact, do X, then restore"),
  use `--reversible`.
- **Protect PHI in the round trip.** This is the important rule. When the flow is
  redact then task then restore:
  1. Redact with `redact.py <their file> --reversible`. The script reads the
     original note. Do NOT open or read the original note's text yourself, so the
     real PHI never enters this conversation or the cloud model.
  2. Do the requested task on the SAFE text only. Read the `.redacted.txt` (it has
     placeholders like `[[NAME_1]]`, no real PHI) and work from that. Keep every
     `[[...]]` tag exactly as written in whatever you produce, and save your output
     to a file.
  3. Restore with `unredact.py <your output file> --map <the .map.json>`. This puts
     the real values back on the machine and checks the round trip.
  4. Tell the user where the final restored file is. It contains real PHI, so do
     not paste its contents into the chat unless they ask. Offer to delete the
     `.map.json` key once they confirm the restore looks right.
- The whole point is that the identifiers stay on the machine while the task still
  gets done. The local scripts read the note; you only ever read the placeholdered
  version.

## Working directory

All commands run from **this skill's own folder** (the directory that contains
this `SKILL.md`, `redact.py`, and `pyproject.toml`). `cd` into it first, or pass
`uv --directory <that folder>`. Everything uses [uv](https://docs.astral.sh/uv/),
which also provisions the correct Python (3.14) on its own, so the user does not
need Python installed. Install uv first if `uv --version` fails (see the commands
in the operating section above). This works the same on macOS, Linux, and
Windows x64.

## Step 1 - one-time install (only if `.installed` is absent)

Check whether the marker file `.installed` exists in this folder.

- If it exists, setup is done. Skip to Step 2.
- If it does not, run the bootstrap once:

  ```bash
  uv run scripts/bootstrap.py
  ```

  This installs the Python dependencies, downloads the large spaCy model and the
  clinical transformer (a few hundred MB, once), runs a smoke test, and writes
  `.installed`. It can take several minutes the first time. Every later run reads
  from cache and does not download again, even if the virtual environment is
  rebuilt. Re-run with `--force` only to repeat the checks deliberately.

## Step 2 - redact a document

Clinical engine is the default. Redacted output is always plain `.txt`.

```bash
uv run redact.py <path>                 # a file: .txt .md .pdf .docx .xlsx .pptx
uv run redact.py <folder>               # every supported file in a folder
uv run redact.py <path> -o clean.txt    # choose the exact output path
uv run redact.py <path> --engine baseline   # lighter spaCy+regex engine, no transformer
cat note.txt | uv run redact.py -       # stdin -> stdout, for piping
```

Output lands in `outputs/<name>.redacted.txt` unless `-o` is given. The run
prints, per file, how many spans were redacted **by category count only** - it
never echoes the detected PHI values.

## Reversible mode (redact -> process elsewhere -> restore)

Use this when the user wants to strip PHI, run the safe text through another AI or
tool, then put the real values back. Add `--reversible`:

```bash
uv run redact.py note.txt --reversible
```

It writes two files: `outputs/note.redacted.txt` (identifiers become unique tags
like `[[NAME_1]]`, consistent per value) and `outputs/note.redacted.map.json` (the
key mapping each tag to its original value).

The `.map.json` is the re-identification key and **contains PHI**. Handle it as
strictly as the original note:
- Send **only** the `.redacted.txt` to any external AI or service. **Never** send,
  paste, upload, or print the `.map.json`.
- When you pass the redacted text to another model, instruct that model to keep
  the `[[...]]` tags verbatim and not renumber or reword them.

To restore after the external step returns text:

```bash
uv run unredact.py <ai_output.txt> --map outputs/note.redacted.map.json
```

This writes `<ai_output>.restored.txt` and runs a round-trip check. It exits with
an error and warns if any tag in the key did not come back (that value cannot be
restored) or if the output contains a tag not in the key (the model altered one).
`unredact.py` needs no models or network; it is plain text substitution.

Note for the user: while the key exists the data is pseudonymized, not fully
de-identified. The default (no `--reversible`) stays one-way so no key is created
by accident.

## Step 3 - read the output honestly

- **Always open the redacted file and skim it.** The tool cannot promise perfect
  recall on a chart template it has never seen.
- **Heed the residual WARNING.** If a run prints `WARNING: ... may still contain
  email-/ssn-/phone-like text`, a line-wrap (common in PDF extraction) probably
  split an identifier so it slipped past detection. Open that file and fix it by
  hand. For anything high-stakes, prefer feeding clean `.txt` over `.pdf`.
- **Scanned/image PDFs are refused.** If a PDF is a picture of a page, extraction
  yields no text; the tool fails that file closed rather than writing an
  empty-but-clean-looking output while the original still holds everything. OCR
  it to text first.
- **Office blind spots.** For `.xlsx` and `.pptx` the tool reads cell values, sheet
  names, text boxes, tables, and speaker notes. It does NOT read embedded chart
  data, cell comments, or headers/footers. If the source might hide identifiers
  there, tell the user to check those spots by hand.

## Optional - prove the quality with numbers

The measurement lab generates synthetic notes full of fake PHI (via Faker, no
real patient) and scores how much each engine removes. This is how you justify
trusting the redactor instead of taking it on faith.

```bash
uv run notes.py                       # see one synthetic note and its answer key
uv run evaluate.py --engine baseline  # recall of the general model
uv run evaluate.py --engine both      # baseline vs clinical, side by side
uv run evaluate.py --sample           # print one fully redacted synthetic note
```

Recall is the safety number. Watch the name-in-prose rows: the clinical engine
should lift them from the sixties/seventies into the high nineties. The leaked
values printed by the lab are synthetic and safe to display.

## What it detects

Names (patient, provider, family), dates, ages (incl. the HIPAA over-89 rule),
MRNs, SSNs, phone/fax, email, URLs, IP addresses, street addresses and unit
numbers, ZIPs, account/policy/insurance IDs, medical licenses and NPIs, device
and vehicle identifiers, biometric IDs, and relationship terms. Unknown clinical
labels fall through to a generic redaction tag rather than being left in.
