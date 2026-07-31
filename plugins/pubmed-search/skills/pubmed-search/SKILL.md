---
name: pubmed-search
description: Run a PubMed literature search from a plain-English description of what to look for, then rate every result 1-5 on evidence strength using the Lantern app's appraisal rubric. Returns title, publication date, lead author, journal, volume, page numbers, a clickable PubMed link, and a green-sphere trust weight for each article. Use this whenever the user asks to search PubMed, find studies or papers or trials or literature on a clinical or biomedical topic, wants a literature search or lit review, mentions MeSH terms or PMIDs or E-utilities, asks "what's published on X", "find me studies about Y", "is there evidence for Z", "any recent trials of", or wants papers on a drug, disease, or intervention narrowed by date, age group, or study type. Prefer this over a general web search for anything biomedical, since it queries PubMed directly and grades the strength of what it finds.
---

# PubMed search with trust weights

Turn a described search into a properly constructed PubMed query, run it, and
return a ranked, citable list where every article carries a 1-5 evidence-strength
weight judged by the same rubric the Lantern iOS app uses.

Two things make this more than a wrapper around a search box. First, PubMed
silently rewrites terms it does not recognize, and the rewrite is often wrong in
ways that quietly return the wrong disease. Second, the weight is a real
appraisal of each abstract, not a lookup from the publication type tag.

## The workflow

1. Read the request for concepts, filters, and count.
2. Build a field-tagged query.
3. Run `scripts/pubmed_search.py`.
4. Audit what PubMed actually searched.
5. Judge each article against the rubric.
6. Render the list.

Work through them in order. Step 4 exists because skipping it is how a search
ends up describing the wrong disease with total confidence.

## Step 1: Read the request

Pull out the concepts to be ANDed together. A clinical question usually has two
to four: a disease, an intervention, a population, and sometimes a setting or an
outcome. "The use of blinatumomab in pediatric B-ALL, newly diagnosed, no
earlier than 2025" is four concepts plus a date floor.

Note the filters: date range, age group, study type, language, humans only.

Default to **10 results** unless the user names a number.

Default to **relevance** sort. Switch to date sort when the user asks for the
newest, the latest, or what just came out. Relevance is usually the better
default even for recent work, because a date floor already handles recency and
relevance ordering puts the pivotal paper first rather than the most recent
letter to the editor.

If the request is genuinely ambiguous in a way that changes which papers come
back, ask. If it is merely underspecified, choose a sensible reading, run the
search, and say what you assumed. A search that runs and shows its query is far
easier to correct than a question that stalls the work.

## Step 2: Build the query

Every concept becomes a parenthesized OR group of a MeSH term and its text-word
synonyms. Groups are joined with AND.

```
("Precursor B-Cell Lymphoblastic Leukemia-Lymphoma"[MeSH] OR "B-ALL"[tiab] OR "B-cell acute lymphoblastic leukemia"[tiab])
AND (blinatumomab[nm] OR blinatumomab[tiab])
AND ("child"[MeSH] OR "adolescent"[MeSH] OR pediatric*[tiab] OR paediatric*[tiab] OR children[tiab])
AND ("newly diagnosed"[tiab] OR "de novo"[tiab] OR frontline[tiab] OR "first-line"[tiab])
```

### Always pair a MeSH term with text words

MeSH indexing lags publication by weeks to months. A paper published last month
usually has no MeSH terms at all, so a MeSH-only query silently drops exactly the
recent work a date-floored search is asking for. Pairing every MeSH term with
`[tiab]` synonyms catches both the indexed back catalog and the fresh records.

The reverse also holds: text words alone miss papers that use different
vocabulary for the same concept, which is what MeSH exists to solve. Use both.

### Field tags worth knowing

| Tag | Matches |
|-----|---------|
| `[MeSH]` | Indexed subject heading, includes narrower terms automatically |
| `[MeSH:NoExp]` | The heading only, without narrower terms |
| `[majr]` | MeSH term flagged as a major topic of the paper |
| `[tiab]` | Title or abstract text |
| `[ti]` | Title only, useful to tighten a noisy result set |
| `[nm]` | Substance name, how new drugs are indexed before they get a MeSH heading |
| `[pt]` | Publication type, e.g. `"Randomized Controlled Trial"[pt]` |
| `[la]` | Language, e.g. `english[la]` |
| `[au]` | Author, e.g. `"Gupta S"[au]` |
| `[ta]` | Journal, e.g. `"N Engl J Med"[ta]` |

Truncation with `*` works on text words (`pediatric*` catches pediatrics,
pediatrician). It does not work inside quoted phrases, and PubMed will not
expand a stem that matches more than 600 terms.

### Traps that produce a confidently wrong search

**Acronyms map to the wrong disease.** This is the big one. `B-ALL` expands to
`"burkitt lymphoma"[MeSH Terms]`, which is a mature B-cell lymphoma, not
precursor B-ALL. Nothing in the results announces the substitution. Other
acronyms behave just as badly. Always spell out the disease in the MeSH term and
keep the acronym as a `[tiab]` alternate, never as a bare word.

**New drugs have no MeSH heading.** Recently approved agents live as
supplementary concepts, reachable with `[nm]`. Search `drugname[nm] OR
drugname[tiab]` and the query works whether or not a heading exists yet.

**"Pediatric" is not one MeSH term.** PubMed splits age into `"infant"[MeSH]`
(to 23 months), `"child, preschool"[MeSH]` (2-5), `"child"[MeSH]` (6-12), and
`"adolescent"[MeSH]` (13-18). `"child"[MeSH]` alone quietly excludes teenagers,
which matters enormously in diseases with an adolescent peak. Use the union of
the ranges the request implies, plus `pediatric*[tiab]`.

**Bare words get auto-mapped invisibly.** An untagged word runs through PubMed's
Automatic Term Mapping, which may expand it to a MeSH term, a journal name, or an
author. Tagging every term keeps control.

**Adolescent MeSH drags in adult trials.** `"adolescent"[MeSH]` is applied to any
study that enrolled even one 13-18 year old, so adult trials that open enrollment
at 15 or 16 satisfy a pediatric age filter. A pediatric blinatumomab search built
this way came back 40% adult: hyper-CVAD in young adults, GIMEMA LAL2317,
GRAALL-2014. When the request is specifically pediatric, exclude adult-only
records:

```
NOT ("adult"[MeSH:NoExp] NOT "child"[MeSH])
```

That keeps records indexed for both adults and children, which is what a genuine
adolescent or AYA study looks like, while dropping the adult-only ones.
`[MeSH:NoExp]` matters here, because `"adult"[MeSH]` with expansion pulls in
narrower headings and over-excludes.

**Broad synonym groups leak across clinical settings.** A "newly diagnosed"
concept built from `induction[tiab] OR consolidation[tiab]` also matches relapse
protocols, which use the same words for their own blocks. The same search
returned the COG AALL1331 relapse trial under a newly-diagnosed filter. Keep the
synonym group, since tightening it loses real papers, and catch the leakage at
the screening step instead, where the abstract makes the setting unambiguous.

**Over-constraining returns nothing.** Four AND groups on a niche topic can drop
the count to zero. If the result count comes back very low, drop the weakest
concept, note that you did, and rerun. A "newly diagnosed" or setting concept is
usually the first to cut, since that detail is often in the full text rather than
the abstract.

### Dates

Pass dates as script flags, not inside the query string:

```
--mindate 2025 --maxdate 3000 --datetype pdat
```

The script fills in the open end when only one bound is given, so "no earlier
than 2025" is just `--mindate 2025`.

`pdat` is the publication date and is almost always what someone means. `edat`
is the date the record entered PubMed. They diverge more than people expect: the
NEJM blinatumomab trial carries a publication date of 2025 Feb 27 but was
published online 2024 Dec 7. A reader asking for "2025 onward" wants that paper,
which `pdat` includes. Use `edat` only when the user is explicitly asking what
has newly appeared in the database.

### Study type filters

Only add these when the user asks for them, since publication type tags are
missing on many recent records and filtering on them drops good papers:

```
AND ("Randomized Controlled Trial"[pt] OR "Clinical Trial, Phase III"[pt])
AND ("Meta-Analysis"[pt] OR "Systematic Review"[pt])
```

If the user wants "only strong evidence," it is usually better to search broadly
and let the trust weights do the filtering, since the weight reads the abstract
while the tag does not.

## Step 3: Run the search

`scripts/pubmed_search.py` sits next to this file. Run it from the skill's own
directory so the relative path resolves wherever the skill is installed, which
differs between a personal skill, a plugin, and an uploaded skill:

```bash
cd "$(dirname "$(find ~ -name pubmed_search.py -path '*pubmed-search*' 2>/dev/null | head -1)")/.."
python3 scripts/pubmed_search.py \
  --term '<the query>' \
  --mindate 2025 \
  --retmax 10 \
  --sort relevance \
  --out /tmp/pubmed-results.json
```

If you already know the skill directory, just `cd` there and run
`python3 scripts/pubmed_search.py`. Single-quote the term so brackets and
parentheses survive the shell. Write to `--out` and read the file rather than
piping a large JSON blob through stdout.

Flags: `--retmax` (default 10), `--retstart` for paging, `--sort relevance|date`,
`--mindate` / `--maxdate` / `--datetype`, `--no-enrich` to skip PMC full-text
lookups, `--out` for the JSON path.

The script is Python 3 standard library only: no pip install, no API key, no
third-party package. Setting `NCBI_API_KEY` in the environment raises the rate
limit from 3 to 10 requests per second, which only matters for large result sets.

Each article in the JSON carries `pmid`, `title`, `journal`, `journalFull`,
`pubdate`, `year`, `volume`, `issue`, `pages`, `doi`, `leadAuthor`, `authors`,
`authorCount`, `publicationTypes`, `citation`, `url`, `abstract`,
`abstractMissing`, `fullTextAdded`, and `pmcid`.

For thin abstracts and reviews the script pulls open-access full text from PMC
and appends it to `abstract`, flagging `fullTextAdded`. This mirrors what the app
does before appraising, and it matters: a review's actual synthesis lives in the
body, not the abstract, so without it reviews get systematically underrated.

### When there is no shell, or the sandbox has no network

Some environments run skills without a shell, or in a sandbox that cannot reach
the internet. The script will fail there with a network error. E-utilities is
plain HTTP, so fetch the same three endpoints directly with whatever web fetch
tool is available and carry on from Step 4 with the same data:

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<urlencoded>&retmax=10&sort=relevance&mindate=2025&maxdate=3000&datetype=pdat&retmode=json&tool=lantern-skill
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=<comma,separated,pmids>&retmode=json&tool=lantern-skill
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<comma,separated,pmids>&rettype=abstract&retmode=xml&tool=lantern-skill
```

esearch gives the PMIDs, the match count, and `querytranslation` for the Step 4
audit. esummary gives the citation fields. efetch gives the abstracts the weights
are judged from. Skip the PMC enrichment on this path and note that reviews were
scored from the abstract alone, since that omission tends to understate them.

## Step 4: Audit what PubMed actually searched

Read `queryTranslation` and `translationSet` in the JSON before reading a single
result. `translationSet` lists every term PubMed rewrote. Check each rewrite
against what you meant.

If a term was mapped to the wrong concept, fix the query and rerun rather than
reporting results from a search that asked the wrong question. Also check
`warnings`, which is where PubMed reports terms it could not match at all: a
misspelled drug name lands there, and the search silently proceeds without it.

Report the final translated query to the user. They can only trust the list if
they can see what was asked.

## Step 5: Screen and judge each article

You are about to read every abstract anyway to score it, so screen the population
and setting at the same time. It costs nothing extra and it catches what a query
cannot.

**Screen first.** For each article, check the abstract against what was actually
asked: the right age group, the right disease, the right clinical setting. Query
syntax cannot separate newly diagnosed from relapsed when both use the word
"consolidation," and it cannot tell a pediatric trial from an adult trial that
enrolled a few adolescents. The abstract can.

When something is off-target, say so on its line rather than dropping it
silently. A reader who can see that result 4 is a relapse trial learns something
about the query; a reader who just gets nine results learns nothing. Keep the
flagged item in place with a short note on what makes it off-target.

If more than two or three of ten are off-target, the query needs work. Tighten
it, rerun, and tell the user what you changed. A list that needed a second pass
is a better deliverable than a list padded with near-misses.

**Then judge.** Read `references/weight-rubric.md` and apply it to every article.
That file
carries the rubric verbatim from the app, the judging principles behind it, the
calibration anchors, and the cases that resist scoring.

The short version: read the abstract, work out the design, the population, the
size, and how well it was run, write the honest one-line verdict, and pick the
number that matches the verdict. Judge only from the `abstract` field the script
returned. Never move a number because the finding was impressive or
disappointing, and never infer rigor from the journal's name.

## Step 6: Render the list

Lead with the search summary, then the numbered results, then the boundary note.

The weight renders as five spheres, filled to the score:

| Score | Spheres |
|-------|---------|
| 1 | 🟢⚪⚪⚪⚪ |
| 2 | 🟢🟢⚪⚪⚪ |
| 3 | 🟢🟢🟢⚪⚪ |
| 4 | 🟢🟢🟢🟢⚪ |
| 5 | 🟢🟢🟢🟢🟢 |

Keep all five positions so the meter reads at a glance, the way the app's
five-rung meter always draws five rungs.

Use this structure:

```
**Search:** <what was searched, in a sentence>
**Query:** `<the translated query PubMed actually ran>`
**Matches:** <total> · showing <n> by <relevance|date>

---

**1. <Full article title>**
<Journal abbreviation>. <Year>;<Volume>(<Issue>):<Pages>. · <Pub date>
<Lead author> et al.
https://pubmed.ncbi.nlm.nih.gov/<pmid>/

Trust weight: 🟢🟢🟢🟢🟢 5 of 5 · Strong weight
<One line of clinician-grade justification: design, n, phase, endpoint, and the
limit that held it back if it is not a 5.>

---

**2. <next>**
```

Write the justification for a clinician. Real terms, real numbers: "randomized
phase 3, n=1,440, DFS primary endpoint" rather than a plain-language paraphrase.
The rubric is the app's; the reading level is not.

After the list, add one line noting the range of evidence strength found, and
whether anything notable was excluded by the filters. If several results scored
1 or 2, say so plainly. A list where the top hit is a 2 is telling the user
something real about the state of the literature.

Close with a brief note that the weights rate evidence strength only, not
applicability to any individual patient.

Then offer, in one line, to publish the list as a shareable page with real
rendered spheres. Offer it; do not publish unasked. A result set worth keeping is
usually one the user wants to send to someone, and an artifact survives the
terminal scrollback.

## The boundary

This rates published evidence. It does not advise on care for a specific person.
Weighting a study's design is in bounds; reading a result as guidance for one
patient is not, and that holds even when the person searching is a clinician.
The output rates studies. The clinical judgment stays with the reader.

## Notes

- **No results.** Report the count honestly, show the query, and suggest the
  specific relaxation most likely to help rather than a generic retry.
- **More than 20 results.** Each one needs its abstract read and judged, so say
  what that will take before starting.
- **A specific PMID.** Search `<pmid>[uid]` to pull one record through the same
  pipeline.
- **Paging.** `--retstart 10` gets results 11-20 with the same query.
