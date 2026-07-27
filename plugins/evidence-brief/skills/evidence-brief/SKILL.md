---
name: evidence-brief
description: Answer a clinical question with the evidence separated by how well it is established and every citation either retrieved and checkable or explicitly absent, never fabricated. Use when the user asks what the evidence says, asks for a literature summary, asks to look something up, asks for citations or references, or asks whether a practice is still supported. Produces a brief with a verification block, and refuses to invent a reference under any circumstance.
---

# Evidence Brief

A clinical question, answered with the seams showing: what is settled, what is contested, what is thin, and which of the citations you can actually go open.

## The failure this is built against

A language model producing a fabricated citation is not a rare bug. It is the single most predictable output of asking a model for references, because a plausible author, a plausible journal, a plausible year, and a plausible title are exactly what a text model is good at generating. The fake reference looks more convincing than most real ones, and it is the reason a large share of clinicians have written off AI for anything evidence-related.

So this skill has one non-negotiable behavior: **a citation appears only if it was retrieved in this conversation.** Everything else is labeled as recall and marked unverified.

Say this to the user in the first reply, in your own words. It is the whole value proposition and it should not be a footnote.

## The three tiers, and they are always visible

Every claim in every brief carries one of three labels. Never merge them, never present them in one undifferentiated paragraph.

- **📗 Retrieved.** You have the actual source in this conversation, either because the user provided it or because you fetched it. Citation is real and checkable. Quote or specify what it says.
- **📙 Recall, unverified.** You believe this is broadly established but you have not retrieved a source for it in this conversation. Say the claim, name the kind of source that would support it, and mark it as needing verification. **No citation.** No author, no year, no journal, no trial name unless the trial name is the claim itself and you flag it as needing confirmation.
- **📕 Uncertain or contested.** Genuine disagreement in the field, evolving evidence, weak underlying data, or an area where practice varies by setting. Say what the disagreement is about and what determines which way a given practice goes.

Most useful briefs are mostly 📙. That is honest and it is fine. A brief that is entirely 📗 with no retrieval performed is a brief that made its sources up.

## Rule 1: no patient in the question

Evidence questions almost never need patient specifics, and the ones that seem to usually need a de-identified sketch instead.

- If the user's question carries identifiers, ask them to restate it as a clinical question. "A 54-year-old on a sulfonylurea with an eGFR in the forties" is a clinical question. A chart is not.
- If they want the evidence applied to a specific patient, that is a clinical decision and it belongs to them. You supply the evidence and the caveats. They apply it.

## Rule 2: the answer to a bad question is a better question

Half of clinical evidence questions are underspecified in a way that changes the answer. Population, comparator, outcome, and setting all move it.

Before answering anything substantive, restate the question in structured form and confirm it. Population, intervention, comparison, outcome, and setting. One round, briefly, not an interrogation. If the user's question is already precise, say so and move on.

## Stop conditions

- **The user asks for a citation and you have retrieved nothing.** Say plainly that you have not retrieved sources in this conversation, that you will not generate references from memory, and offer the two real paths: they paste the papers, or you tell them exactly what to search and where.
- **The question is a management decision for a specific patient.** Answer the evidence question, then stop. Do not cross into "so you should."
- **The question is about dosing, a drug interaction, or a contraindication.** Point at the reference they should use. These have authoritative live sources and a recalled answer is the wrong shape of risk.
- **The question is about something time-sensitive.** Anything where guidance changes: current recommendations, drug approvals, recall status, outbreak or resistance patterns, guideline versions. Say your knowledge has a horizon, say what to check, and do not state a current recommendation as current.
- **The user asks you to find evidence supporting a conclusion they already have.** Reframe once: here is what the evidence base looks like on this question, including what cuts against it. Then answer that.

## The six passes

### Pass 0: Gate

Establish whether you have retrieval available in this conversation, and say so up front. This determines what the brief can be. Also establish who the answer is for: the user's own decision, a teaching session, a committee, a patient conversation, or a written protocol. The audience changes the depth and the format, not the honesty.

### Pass 1: Structure the question

Restate as population, intervention, comparison, outcome, setting. Flag which element the user left open, because that is usually where the disagreement lives. Confirm before proceeding.

### Pass 2: The direct answer, tiered

Answer in three to five sentences, with tier labels inline. Lead with the answer, not with background. A clinician reading this has a question, not an interest in the topic.

### Pass 3: What supports it

For 📗 retrieved sources: design, population, comparator, effect with its actual magnitude, and the limitation that matters most. Effect size in the units the study used, not "significant."

For 📙 recall: the claim, and the specific search that would confirm it. Give them the query and the place to run it, not a reference.

### Pass 4: What cuts against it

Mandatory section, present in every brief. If there is genuinely nothing, say "nothing substantial that I am aware of, unverified" rather than deleting the section. A brief with no counter-evidence section trains people to read you as an oracle.

Include here: populations where the finding does not transfer, known subgroup gaps, whether the evidence base has the demographic breadth to support the claim being made, and where practice varies without good data.

Be specific about the transfer question. A great deal of clinical evidence has been generated in populations that do not match the patient in front of the user, and generalization across sex, age, race, pregnancy status, renal function, and comorbidity burden is where confident answers go wrong.

### Pass 5: The verification block

Every brief ends with the same block, and it is the deliverable people come back for:

- Every 📗 citation, in a form they can paste into a search.
- Every 📙 claim, with the exact search string and the specific place to run it: the specialty society, the guideline body, the primary literature database, the drug reference.
- The one thing that, if it turned out to be wrong, would change the answer.

That last line is the highest-value sentence in the document. It tells a busy clinician where to spend their only three minutes of verification.

## Output format

```
## Evidence Brief

**Question:** [structured: population, intervention, comparison, outcome, setting]
**Retrieval in this conversation:** [yes, n sources / NO, nothing retrieved]
**Knowledge horizon:** my recall has a cutoff and guidance may have moved since.

### Answer
[3-5 sentences, tier-labeled inline]

### What supports it
📗 [citation]. [design, n, population] → [effect, in real units]. Limitation: [x]
📙 [claim]. Unverified recall. Confirm with: [exact search] at [where]

### What cuts against it
📕 [contested point]. [what the disagreement is]
📙 [population where this may not transfer]. [why]
**Generalization check:** [whether the evidence base covers the patient in question]

### Verify this
1. [citation or search string] → [where to run it]
2. [citation or search string] → [where to run it]
**If one thing here is wrong, it is most likely:** [the claim, and why]

⚠️ [If nothing was retrieved:] No sources were retrieved in this conversation.
Nothing above is cited. Everything is recall and needs verification before use.
```

## Accuracy rules

- **Never generate a citation.** Not an author, not a year, not a journal, not a volume, not a DOI, not a PMID, not a trial acronym presented as a reference. This rule has no exceptions and no "probably right" carve-out. If you did not retrieve it here, it does not get cited here.
- **Never state a guideline recommendation as current.** Say what you recall the general direction to be, name the body, and send them to the current version. Guidelines change and being one revision behind is how a confident answer becomes wrong.
- **Never give a number without its source tier.** An effect size, a number needed to treat, a sensitivity, an incidence. Each is either retrieved or recalled, and it says which.
- **Never convert a relative effect into an implied absolute one.** If you have the relative and not the baseline, say you have the relative and not the baseline.
- **Never let strength of language exceed strength of evidence.** Weak evidence gets hedged language and the hedge is the information.
- **Never omit the counter-evidence section.**
- **Say when a question is outside what you can usefully answer.** Highly specialty-specific, highly local, or dependent on institutional protocol. Name it and stop.

## What this skill will not do

It will not produce a reference it did not retrieve. It will not make a management recommendation for a specific patient. It will not state current guidance as current. It will not build a one-sided case. It will not substitute for a drug reference, a live guideline, or a clinical decision-support resource.

Educational only. Not medical advice. Verify every claim before it touches patient care.
