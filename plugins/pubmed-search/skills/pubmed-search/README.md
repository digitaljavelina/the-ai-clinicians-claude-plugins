# PubMed Search with Trust Weights

Describe the literature search you want in plain English. Get back the most
relevant PubMed records with full citations, clickable links, and a 1-5
evidence-strength rating on every one.

Example of what you type:

> Perform a PubMed search for the use of blinatumomab in pediatric B-ALL, newly
> diagnosed, no earlier than 2025.

Example of what comes back, per article:

```
1. Blinatumomab in Standard-Risk B-Cell Acute Lymphoblastic Leukemia in Children
   N Engl J Med. 2025;392(9):875-891. · 27 Feb 2025
   Lead author Gupta S
   https://pubmed.ncbi.nlm.nih.gov/39651791/

   Trust weight: 🟢🟢🟢🟢🟢 5 of 5 · Strong weight
   Randomized phase 3 (COG AALL1731), n=1,440 at interim, DFS primary endpoint.
```

Ten results by default. Ask for a different number, a date range, a study type,
or a sort by date and it adapts.

## Installing

### Claude app (claude.ai, desktop, or mobile)

1. Open **Settings → Capabilities → Skills**.
2. Choose **Upload skill** and select `pubmed-search.zip`.
3. Start a new conversation and describe the search you want.

Skills require a paid Claude plan, and the setting that lets Claude run code must
be enabled, since the search runs a small Python script.

### Claude Code

```sh
/plugin marketplace add digitaljavelina/the-ai-clinicians-claude-plugins
/plugin install pubmed-search@the-ai-clinicians-claude-plugins
```

Or unzip the folder into `~/.claude/skills/` and restart Claude Code.

## What it actually does

**Builds a real query.** PubMed silently rewrites terms it does not recognize,
and the rewrite is frequently wrong. Searching the plain text `B-ALL` gets
remapped to `"burkitt lymphoma"[MeSH Terms]`, a completely different disease, and
nothing in the results tells you. The skill constructs a field-tagged query with
MeSH headings paired to text-word synonyms, then shows you the query PubMed
actually ran so you can audit it.

**Rates the evidence.** Every result's abstract is retrieved and judged against a
published appraisal rubric: 1 for animal, cell, or single-case work, up to 5 for a
large well-conducted randomized trial or a high-quality meta-analysis. The rubric
rates design and execution only. A dramatic result in a 20-patient single-arm
study is still a 2; a null result from a 3,000-patient trial is still a 5.

**Flags what does not belong.** Query syntax cannot tell newly diagnosed disease
from relapsed when both use the word "consolidation." Because the skill reads
every abstract anyway to rate it, it screens the population and setting at the
same time and marks anything off-target rather than quietly padding the list.

The rubric comes from Lantern, an iOS app that explains cancer clinical trials
and appraises studies in plain language. `references/weight-rubric.md` carries it
verbatim along with its calibration anchors.

## Requirements

Python 3 and an internet connection. Nothing to install: the script uses only the
Python standard library and calls NCBI E-utilities, which needs no API key. If a
sandbox blocks the network, the skill falls back to fetching the same E-utilities
endpoints with a web fetch tool.

Setting an `NCBI_API_KEY` environment variable raises the NCBI rate limit from 3
to 10 requests per second. Only worth doing for large result sets.

## Scope

This rates the strength of published evidence. It does not advise on care for any
individual patient, and it is not a substitute for reading the paper. Educational
and research use.

MIT licensed.
