# The trust weight rubric

This is the appraisal methodology from the Lantern iOS app, copied so the skill's
numbers and the app's numbers mean the same thing. The source of truth is
`ios/Lantern/Models/Appraisal.swift` (the `weight` field guide) and
`ios/Lantern/Services/Prompts.swift` (the appraisal prompt). If the app's rubric
changes, change this file too, or the two will drift apart silently.

## The rubric, verbatim from the app

> A whole number from 1 to 5 that matches the verdict above: how much weight a
> reader should place on this one study, judged only by how strong its evidence
> is. Rubric: 1 = very early or anecdotal, lean on it very little (a study in
> animals or cells, a single case report, or a tiny study); 2 = weak (a small
> observational study, or an early-phase trial with few people); 3 = moderate,
> useful but with real limits (a mid-sized observational study, or a
> small-to-mid randomized trial); 4 = strong (a well-designed randomized trial
> of good size, or a solid systematic review); 5 = very strong (a large,
> well-conducted randomized trial, or a high-quality meta-analysis of several
> such trials). Never raise or lower the number because the result was
> encouraging or discouraging.

That last sentence is the one most likely to be violated in practice. A dramatic
survival benefit in a 20-patient single-arm study is still a 2. A null result
from a 3,000-patient randomized trial is still a 5. The number rates the design
and its execution, never the direction or the size of the finding.

## The judging principles that sit behind it

Also verbatim from the app's appraisal prompt:

- A study in animals or in cells in a lab often does not carry over to people.
- A study that only watches what happens (observational) can show a link but
  usually cannot prove that one thing caused another. A randomized trial can say
  more about cause.
- A single case report (one person) or a very small study is a weak basis for
  any conclusion.
- A review or a meta-analysis pulls together other studies; it can be stronger,
  but only as strong as the studies inside it.
- More people, and people rather than animals, usually means a result you can
  lean on more.

## Labels for each value

The app pairs the number with a label. Use the same words so a weight of 3 reads
the same in both places.

| Weight | Label |
|--------|-------------------|
| 1 | Very little weight |
| 2 | A little weight |
| 3 | Moderate weight |
| 4 | Considerable weight |
| 5 | Strong weight |

## Calibration anchors

These are the two worked examples the app ships in its prompt, compressed to the
part that fixes the scale. Anchor new judgments against them.

**Weight 5.** A randomized trial of 1,200 adults with stage III colon cancer
across 30 centers, comparing standard chemotherapy with and without an added
drug, reporting three-year disease-free survival with a p-value, publicly
funded. Large, randomized, multicenter, hard endpoint.

**Weight 4.** A systematic review of checkpoint inhibitors in advanced melanoma.
It gathers earlier studies and gives a fuller picture than any one trial, which
is why it outranks a single small study. It does not reach 5 because the
abstract never describes the quality or the number of the studies it pulled in,
so its strength cannot be confirmed.

The gap between those two is the useful part: a review is not automatically a 4,
and a randomized trial is not automatically a 5. What separates them is whether
the record actually lets you confirm size and rigor.

## Applying it to a search result list

The app appraises one study at a time, from the abstract plus, for a thin
abstract or a review, the open-access full text. `scripts/pubmed_search.py`
assembles that same input for every result, so judge from the `abstract` field
it returns and nothing else. Do not reach for outside knowledge about a trial,
and do not infer rigor from the journal's reputation. A weak study in a famous
journal is still weak, and the app would score it that way.

Work through each article in this order, because the number has to follow the
reasoning rather than lead it:

1. **Design.** What kind of study is this actually? Read the abstract, not just
   the publication type tags. PubMed tags are frequently absent on recent
   records and occasionally wrong. A record tagged only "Review" that turns out
   to be a narrative overview is not the same as a systematic review.
2. **Population and size.** How many participants, and were they people? Note
   when the abstract gives no number, which is itself a limit on how far the
   result can be trusted.
3. **Execution.** Randomized or single-arm? Controlled or uncontrolled? Blinded?
   Phase 1, 2, or 3? Pre-registered endpoints or post-hoc? Interim or final?
4. **The honest verdict**, in one or two sentences: how strong is this evidence,
   and what limits it. Write this before choosing the number.
5. **The number**, chosen to match the verdict you just wrote.

Common cases and where they land:

| What the record describes | Typical weight |
|---------------------------|----------------|
| In vitro, animal model, or a single case report | 1 |
| Case series, phase 1, small single-arm phase 2, tiny retrospective chart review | 2 |
| Mid-sized observational or registry study, small or early randomized trial, large well-run single-arm phase 2 | 3 |
| Well-designed randomized trial of good size, solid systematic review, large well-conducted prospective cohort | 4 |
| Large multicenter randomized phase 3 with a hard endpoint, high-quality meta-analysis of such trials | 5 |

Records that resist scoring:

- **No abstract** (`abstractMissing: true`). Editorials, comments, and letters
  often carry only a title. Do not guess a weight from the title. Mark it as not
  rateable and say why.
- **Conference abstract or preprint.** Not peer reviewed and usually missing
  methods detail. Cap at 2 and say that is the reason.
- **Interim analysis or early readout.** Score the evidence as it stands, not as
  the finished trial will read.
- **Retracted or subject to an expression of concern.** If the record says so,
  lead with that rather than the number.

## The boundary this inherits from the app

The app's hard boundary is that it explains and appraises public information and
never tells anyone whether a study applies to their own situation. This skill
keeps it. Rating evidence strength is in bounds. Recommending a treatment,
telling a reader what to do for a particular patient, or reading a result as
guidance for one person's care is not. That holds even when the person running
the search is a clinician: the output rates studies, and the clinical judgment
stays with the reader.
