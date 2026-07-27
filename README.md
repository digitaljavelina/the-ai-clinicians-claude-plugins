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
```

## Available Plugins

| Plugin           | Version | Description                                                                                                                                                                                                                                                                                                                                                    |
| ---------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bag-submission` | 1.1.2   | Turn a prompt, skill, or workflow a clinician built into a finished "Bag Submission" post for The AI Clinicians' Medical Bag community library. Interviews one field at a time, enforces the three rules the bag runs on (returns a draft not a final artifact, bans invention, ends with a real verify), keeps every entry patient-data-free, tests it on a synthetic case, hands back a paste-ready post, and saves the entry as a markdown file. |

### Prerequisites

None. `bag-submission` runs with no external dependencies.

## Usage

Run `/bag-submission` and answer the interview questions. The skill walks each field of the Bag Submission template, checks the entry against the three rules the bag runs on, tests it on a synthetic case, and returns a post you can paste straight into the community feed. It also saves the entry as a markdown file so you keep a copy.

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
