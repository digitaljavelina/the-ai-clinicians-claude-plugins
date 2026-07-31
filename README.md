# The AI Clinicians Claude Plugins

Claude Code plugins built for the [The AI Clinicians](https://www.skool.com/the-ai-clinicians-9405) community, published as a single marketplace.

## Installation

Add this marketplace to Claude Code:

```sh
/plugin marketplace add digitaljavelina/the-ai-clinicians-claude-plugins
```

Then install a plugin:

```sh
# Community and privacy
/plugin install bag-submission@the-ai-clinicians-claude-plugins
/plugin install phi-redactor@the-ai-clinicians-claude-plugins

# Documentation
/plugin install scribe-note-audit@the-ai-clinicians-claude-plugins
/plugin install interval-note-builder@the-ai-clinicians-claude-plugins
/plugin install discharge-summary-builder@the-ai-clinicians-claude-plugins

# Administrative load
/plugin install inbox-reply-drafter@the-ai-clinicians-claude-plugins
/plugin install prior-auth-packet@the-ai-clinicians-claude-plugins
/plugin install forms-and-letters@the-ai-clinicians-claude-plugins
/plugin install em-code-advisor@the-ai-clinicians-claude-plugins

# Reasoning and evidence
/plugin install evidence-brief@the-ai-clinicians-claude-plugins
/plugin install pubmed-search@the-ai-clinicians-claude-plugins
/plugin install differential-challenger@the-ai-clinicians-claude-plugins

# Adoption and policy
/plugin install ai-tool-evaluator@the-ai-clinicians-claude-plugins
/plugin install ai-consent-and-policy@the-ai-clinicians-claude-plugins
```

### Using these in the Claude app instead

If you use Claude in the browser, desktop, or mobile app rather than Claude Code, install
a plugin's skill by uploading it as a `.zip` under **Settings → Capabilities → Skills**.

`pubmed-search` is packaged and ready to upload:

[**Download pubmed-search.zip**](https://github.com/digitaljavelina/the-ai-clinicians-claude-plugins/releases/download/pubmed-search-v1.0.0/pubmed-search.zip)

1. Download the file. Do not unzip it.
2. Open Claude, then **Settings → Capabilities → Skills**.
3. Choose **Upload skill** and pick the `.zip`.
4. Start a new chat and describe the search you want.

Skills need a paid Claude plan, and the setting that lets Claude run code must be on,
since the search runs a small Python script.

For any other plugin here, zip the folder at `plugins/<name>/skills/<name>/` and upload
that. Anything requiring a local install, `phi-redactor` in particular, is Claude Code
only.

## Available Plugins

| Plugin           | Version | Description                                                                                                                                                                                                                                                                                                                                                    |
| ---------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bag-submission` | 1.1.2   | Turn a prompt, skill, or workflow a clinician built into a finished "Bag Submission" post for The AI Clinicians' Medical Bag community library. Interviews one field at a time, enforces the three rules the bag runs on (returns a draft not a final artifact, bans invention, ends with a real verify), keeps every entry patient-data-free, tests it on a synthetic case, hands back a paste-ready post, and saves the entry as a markdown file. |
| `em-code-advisor` | 1.0.0 | Assign the correct E/M code from a clinical note and justify it element by element against the 2021/2023 CPT MDM grid and time thresholds, across office/outpatient, hospital inpatient/observation, emergency department, nursing facility, and home/residence settings. Codes the documentation rather than the encounter, binds every code and threshold to bundled reference tables instead of recalling them, and returns documentation gaps as provider queries rather than guesses. |
| `phi-redactor` | 1.0.0 | De-identify PHI in clinical text and documents entirely on the local machine. Uses Microsoft Presidio plus a clinical NER transformer (`obi/deid_roberta_i2b2`) that catches names in free-text prose that general models miss. Reads `.txt`, `.md`, `.pdf`, `.docx`, `.xlsx`, and `.pptx`. Model libraries are forced offline before they load, so a redaction run makes no network call. A reversible mode writes a local key so text can be de-identified, processed elsewhere, then restored. |
| `scribe-note-audit` | 1.0.0 | Audit an AI scribe's draft note before signing it, hunting for invented specifics, normals nobody examined, misattributed statements, and flattened medical decision-making. Returns a line-level correction list, never a rewritten note. |
| `interval-note-builder` | 1.0.0 | Build the carry-forward scaffold for a progress, rounding, or follow-up note so active problems do not vanish when nobody mentions them out loud today. Returns a problem scaffold and status questions, never a finished note. |
| `inbox-reply-drafter` | 1.0.0 | Triage a stack of patient portal messages and draft replies at the right reading level, separating what can be answered in a message from what needs a call, a visit, or the emergency department today. |
| `prior-auth-packet` | 1.0.0 | Build a prior authorization request or letter of medical necessity around the payer's own coverage criteria, mapping each criterion to the documentation that meets it and naming the ones that are not, plus a peer-to-peer prep sheet. |
| `forms-and-letters` | 1.0.0 | Draft the non-clinical paperwork pile no scribe touches. FMLA and disability forms, work and school notes, accommodation letters, DME and home health justification, camp and sports forms, and referral letters. |
| `discharge-summary-builder` | 1.0.0 | Assemble a discharge summary, transfer note, or service handoff from fragmented source documents, with a dedicated pass for what is still unresolved and who owns it after the patient leaves. |
| `evidence-brief` | 1.0.0 | Answer a clinical question with the evidence separated by how well it is established and every citation either retrieved and checkable or explicitly marked absent. Refuses to invent a reference under any circumstance. |
| `pubmed-search` | 1.0.0 | Run a PubMed search from a plain-English description and rate every result 1-5 on evidence strength. Returns title, date, lead author, journal, volume, pages, a clickable link, and a trust weight per article. Builds a field-tagged MeSH query rather than a keyword string (searching plain `B-ALL` gets silently remapped to Burkitt lymphoma), shows the query PubMed actually ran so it can be audited, reads every abstract to score it, and flags results whose population or clinical setting does not match the question. |
| `differential-challenger` | 1.0.0 | Argue against a clinician's working diagnosis or plan instead of answering for them, testing for anchoring, premature closure, and the demographic gaps where evidence stops transferring. Never produces a diagnosis. |
| `ai-consent-and-policy` | 1.0.0 | Build the patient-facing script for disclosing an AI scribe, handle the opt-out gracefully, and assemble the questions a practice must answer before recording encounters. Produces scripts and a question list for counsel, never a legal determination. |
| `ai-tool-evaluator` | 1.0.0 | Design a real trial of a clinical AI tool before buying it, with a baseline measured first, a decision rule written in advance, and the questions that separate a demo from a workflow. Never recommends a specific product. |

### Prerequisites

Two plugins need something. The rest are prompt-only: no runtime, no network, no
install beyond the plugin itself.

| Plugin | Requires |
| ------ | -------- |
| `phi-redactor` | [uv](https://docs.astral.sh/uv/), plus a one-time model download of roughly 1.3 GB. Python itself is not required; uv provisions it. |
| `pubmed-search` | Python 3 and an internet connection. No packages to install: the bundled script is standard library only, and NCBI E-utilities needs no API key. |
| Everything else | Nothing. Reference tables, where a plugin uses them, are bundled. |

`phi-redactor` runs a one-time setup that downloads the spaCy model and the clinical
transformer, then writes an `.installed` marker. Claude runs this for you on first use.
Every later run reads from cache. After setup, redaction works with the network off,
which is the intended way to verify the offline claim.

## Usage

### bag-submission

Run `/bag-submission` and answer the interview questions. The skill walks each field of the Bag Submission template, checks the entry against the three rules the bag runs on, tests it on a synthetic case, and returns a post you can paste straight into the community feed. It also saves the entry as a markdown file so you keep a copy.

### em-code-advisor

Paste or point at encounter documentation and ask what it supports. The skill reads its
bundled MDM grid and code tables, then returns the level with each element tied to a line
it can quote from your note. Where the documentation does not settle a level, it hands
back a provider query instead of a guess. It never reports a confidence percentage and
never asserts what a payer will pay.

### phi-redactor

Describe what you want de-identified and Claude runs the commands for you. Two modes:

- **One-way** (default): identifiers become category tags like `[NAME]` and `[DATE]`.
- **Reversible**: identifiers become unique tags like `[[NAME_1]]` alongside a local
  `.map.json` key, so the safe text can be processed elsewhere and then restored.

The `.map.json` is the re-identification key and contains PHI. Send only the redacted
text to any external service, never the key. The repo `.gitignore` excludes `*.map.json`
and `outputs/` so neither is committed by accident.

Read the redacted output before trusting it. The tool biases toward over-redaction, and
it prints a warning when something identifier-shaped survives, which usually means a
PDF line-wrap split a value. Scanned or image-only PDFs are refused rather than written
out empty-but-clean-looking.

### pubmed-search

Describe the search in plain English. Say what you are looking for, in what population,
over what time window, and how many results you want.

> Perform a PubMed search for the use of blinatumomab in pediatric B-ALL, newly
> diagnosed, no earlier than 2025.

Ten results by default, each returned with title, publication date, lead author, journal,
volume, page numbers, a clickable PubMed link, and a 1-5 trust weight shown as green
spheres.

The weight rates design and execution, never the direction of the finding. A dramatic
result in a 20-patient single-arm study is still a 2. A null result from a
3,000-patient randomized trial is still a 5.

Two things it does that a search box will not:

**It shows you the query it ran.** PubMed silently rewrites terms it does not recognize,
and the rewrite is often wrong. The plain text `B-ALL` gets remapped to
`"burkitt lymphoma"[MeSH Terms]`, a different disease entirely, and nothing in the
results tells you. The skill builds a field-tagged MeSH query and prints the translation
so you can audit it before trusting the list.

**It flags what does not belong.** Query syntax cannot separate newly diagnosed from
relapsed disease when both use the word "consolidation," and a pediatric age filter still
admits adult trials that enrolled one adolescent. Because every abstract is read anyway to
score it, the population and setting get checked at the same time and off-target results
are marked in place rather than quietly padding the list.

Pairs with `evidence-brief`, which answers a clinical question from evidence you already
have. `pubmed-search` goes and gets the evidence, then rates it.

### The ten clinical workflow plugins

These ten need no command. Each one carries a description written in the words a tired
clinician actually types, so Claude loads the right one when you describe the problem.
Say "my scribe note is wrong again" and the audit runs. Say "this prior auth is eating my
day" and the packet builder runs.

Each was built against a pain point clinicians described in their own words, and each one
holds the same rules:

1. **The patient does not have to be in it.** Every one gates on PHI before it reads
   content, and every one offers a synthetic path for learning.
2. **The output is a draft, never the artifact.** No signed note, no submitted claim,
   no sent message, no diagnosis, no consent form, no product recommendation.
3. **No fabricated citations, codes, statutes, doses, or numbers.** What was not
   retrieved or supplied is marked absent.
4. **No fake precision.** No accuracy percentages, no confidence scores, no simulated
   audit outcomes, no invented ROI figures.
5. **Every deliverable ends with three checks.** Not a disclaimer. Three specific things
   to look at, because the clinician is the one who catches the model.

Four of them are worth running as pairs rather than alone:

**The documentation chain.** `interval-note-builder` runs before the encounter and builds
the problem scaffold. Your scribe drafts. `scribe-note-audit` runs before you sign. The
second one catches what the first one predicted would go missing.

**The verify chain.** `differential-challenger` attacks the reasoning and hands off to
`evidence-brief` the moment a challenge turns on what the literature actually says.
Neither one answers the clinical question, by design.

**The adoption chain.** `ai-tool-evaluator` designs the pilot and stops at the privacy
question. `ai-consent-and-policy` covers what has to be settled before a single encounter
gets recorded.

**The billing pair.** `scribe-note-audit` checks the note is true before it is signed.
`em-code-advisor` then reads that note and says what it supports as a code. The audit
protects the record, the coder protects the claim, and neither one bills for you.

The remaining four stand alone: `inbox-reply-drafter` for the portal pile,
`prior-auth-packet` for coverage criteria and peer-to-peer prep, `forms-and-letters` for
the paperwork no scribe touches, and `discharge-summary-builder` for handoffs and the
open loops that follow the patient out the door.

Run any of them against a synthetic case first. They are new, and the output formats will
want tightening against your own workflow before you lean on them.

## Repo layout

```
.claude-plugin/marketplace.json   # marketplace manifest, lists all plugins
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<skill>/SKILL.md
bump-version.sh                   # bump a plugin version in plugin.json + marketplace.json
```

Bump a plugin version:

```sh
./bump-version.sh <plugin-name> [patch|minor|major]
```

## License

MIT
