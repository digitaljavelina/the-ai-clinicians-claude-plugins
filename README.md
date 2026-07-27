# The AI Clinicians Claude Plugins

Claude Code plugins built for the [The AI Clinicians](https://www.skool.com/the-ai-clinicians-9405) community, published as a single marketplace.

## Installation

Add this marketplace to Claude Code:

```sh
/plugin marketplace add digitaljavelina/the-ai-clinicians-claude-plugins
```

Then install a plugin:

```sh
/plugin install bag-submission@the-ai-clinicians-claude-plugins
/plugin install em-code-advisor@the-ai-clinicians-claude-plugins
/plugin install phi-redactor@the-ai-clinicians-claude-plugins
```

## Available Plugins

| Plugin           | Version | Description                                                                                                                                                                                                                                                                                                                                                    |
| ---------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bag-submission` | 1.1.2   | Turn a prompt, skill, or workflow a clinician built into a finished "Bag Submission" post for The AI Clinicians' Medical Bag community library. Interviews one field at a time, enforces the three rules the bag runs on (returns a draft not a final artifact, bans invention, ends with a real verify), keeps every entry patient-data-free, tests it on a synthetic case, hands back a paste-ready post, and saves the entry as a markdown file. |
| `em-code-advisor` | 1.0.0 | Assign the correct E/M code from a clinical note and justify it element by element against the 2021/2023 CPT MDM grid and time thresholds, across office/outpatient, hospital inpatient/observation, emergency department, nursing facility, and home/residence settings. Codes the documentation rather than the encounter, binds every code and threshold to bundled reference tables instead of recalling them, and returns documentation gaps as provider queries rather than guesses. |
| `phi-redactor` | 1.0.0 | De-identify PHI in clinical text and documents entirely on the local machine. Uses Microsoft Presidio plus a clinical NER transformer (`obi/deid_roberta_i2b2`) that catches names in free-text prose that general models miss. Reads `.txt`, `.md`, `.pdf`, `.docx`, `.xlsx`, and `.pptx`. Model libraries are forced offline before they load, so a redaction run makes no network call. A reversible mode writes a local key so text can be de-identified, processed elsewhere, then restored. |

### Prerequisites

| Plugin | Requires |
| ------ | -------- |
| `bag-submission` | Nothing. Runs with no external dependencies. |
| `em-code-advisor` | Nothing. Reference tables are bundled; no network, no runtime. |
| `phi-redactor` | [uv](https://docs.astral.sh/uv/), plus a one-time model download of roughly 1.3 GB. Python itself is not required; uv provisions it. |

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
