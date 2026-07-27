---
name: discharge-summary-builder
description: Assemble a discharge summary, transfer note, or service handoff from fragmented source documents, with a dedicated pass for what is still unresolved and who owns it after the patient leaves. Use when the user asks for help with a discharge summary, D/C summary, transfer note, sign-out, service change handoff, or says the auto-generated summary needs too much fixing. Produces a structured draft plus an open-loop list, never a signed summary.
---

# Discharge Summary Builder

The discharge summary is the one document that gets read by someone who was not there. Everything it leaves out becomes a phone call, a repeated test, or a readmission.

## What this does differently

Auto-generated summaries are decent at the retrospective narrative and bad at the forward-looking part, because the narrative lives in the notes and the forward-looking part lives in people's heads. The pending culture, the medication that was held and never restarted, the imaging finding that needs a six-week repeat, the consultant recommendation that was accepted but never ordered.

So the center of this skill is the open-loop pass. Everything else is assembly.

Say this to the user in your first reply, in your own words: you are building the draft and hunting the open loops, and the summary is not correct until they confirm what is still running.

## Rule 1: the patient does not have to be in it

A hospital course pulled from real notes is dense PHI.

- Consumer environment with no BAA: stop, and have them scrub the source documents by hand first.
- Institutional covered environment: proceed and say so.
- Learning the workflow: build a synthetic multi-day course together with two deliberately buried open loops, and let them find them.

Keep relative timing when scrubbing. "Hospital day 4," "post-op day 2," "48 hours after the second dose" is the spine of a hospital course and identifies nobody.

## Rule 2: you assemble what you were given, and you say what you were not

A discharge summary built from partial sources is partial, and the danger is that it does not look partial. A fluent summary of days one through three reads exactly like a fluent summary of the whole stay.

Track your sources explicitly. State at the top what you were given and what you were not, and mark any period of the stay you cannot account for. Never bridge a gap with a plausible course.

## Stop conditions

- **The user gives you a one-line summary and asks for a full discharge summary.** Say what you would need. A summary assembled from four words is fiction with headers.
- **The user asks you to state a discharge diagnosis they have not stated.** The discharge diagnosis is a clinical determination and it drives coding, follow-up, and the next clinician's assumptions. Ask.
- **You are asked to reconcile medications.** You cannot. You do not have the pre-admission list, the inpatient list, the dose changes, or the pharmacy record, and a medication reconciliation performed by a model that is guessing is worse than none. Build the structure, mark every slot, and say plainly that reconciliation is theirs.
- **The user asks what the follow-up interval should be.** Clinical decision. Bracket it.
- **The patient died, or the summary is a death summary.** Different document, different requirements, and often institution-specific and legally sensitive. Offer the structure, and tell them to check it against their institution's template.

## The six passes

### Pass 0: Gate

Establish PHI status, document type (discharge summary, transfer to another facility, service-to-service handoff, or shift sign-out), and inventory the sources: admission H&P, daily progress notes and which days, consultant notes and which services, operative or procedure notes, discharge orders, medication list, results. Name what is missing before you write a word.

### Pass 1: The one-paragraph course

Write the hospital course as one paragraph first, before any headers. Why they came, what was found, what was done, how they responded, why they are leaving now.

Doing this first is what keeps the summary from becoming a chronological transcript of every day. A day-by-day course is easy to generate and nearly useless to the reader, because the reader is a clinician with four minutes who needs the arc.

Then expand only where a reader would have a question the paragraph does not answer.

### Pass 2: Open loops

The pass this skill exists for. Sweep the sources for every thread that is still running at the moment of discharge, and give each an owner and a timeframe.

Categories, and hunt each one separately:

- **Pending results.** Cultures with days to finalize, pathology, cytology, send-out labs, imaging without a final read, genetics. Each needs: what, when it results, who is watching for it, and what to do with an abnormal one.
- **Medications held and not restarted.** The single most dangerous open loop in the document. Anticoagulation, antihypertensives held for a soft pressure, diuretics, immunosuppressants, home psychiatric medications, metformin held for contrast. Each needs an explicit restart instruction or an explicit statement that it is stopped and why.
- **New medications with a stop date or a taper.** Antibiotic courses, steroid tapers, pain medication with a planned reduction. Each needs the end date, not the duration alone.
- **Findings that need an interval follow-up.** The incidental nodule, the mildly abnormal value, the finding deferred to outpatient. Each needs the interval and the responsible clinician, or it disappears.
- **Consultant recommendations.** Split them: accepted and done, accepted and pending, and considered but not followed with the reason. Recommendations that were accepted and never ordered are a classic gap.
- **Equipment, therapy, and home services.** Ordered versus arranged versus pending. Not the same.
- **Follow-up appointments.** Scheduled versus recommended. Also not the same, and the summary should say which.

Every open loop gets a named owner. "Follow up as an outpatient" with no owner is how loops close on nobody.

### Pass 3: Discharge medications, structured but unreconciled

Build the table with columns for continued, changed, new, and stopped, and put the reason beside every change. Then leave it explicitly unreconciled and mark it. State plainly that reconciliation against the pre-admission list is the clinician's, and that you did not do it and cannot.

Include a "changed from home" column. The next clinician's most common question about a discharge summary is what is different from before, and most summaries make them derive it.

### Pass 4: The patient-facing version

Most people discharge with instructions written for clinicians. Produce a short parallel version in plain language: what happened, what changed about your medicines, what to watch for and exactly when to call, and what appointments to keep.

Sixth to eighth grade, short sentences, no abbreviations. Return precautions with specific thresholds, never "if it gets worse."

### Pass 5: Hand back the verify

Three checks:

1. Every open loop: does it have a name and a date on it?
2. Every held medication: does the summary say restart, or say stopped and why?
3. The medication list: have you reconciled it against the pre-admission list yourself?

## Output format

```
## Discharge Summary Draft

**Type:** [discharge / transfer / service handoff]
**Sources given:** [list] · **Sources missing:** [list, or "none"]
**Unaccounted period:** [days, or "none"]
**PHI status:** [de-identified / covered environment / synthetic]

### 1. Hospital course
[one paragraph, then expansions only where needed]

### 2. Open loops
| Loop | Type | Owner | When | If abnormal |
|---|---|---|---|---|
| [thread] | pending result / held med / taper / interval follow-up / consult rec / service | [name or [WHO?]] | [date or [WHEN?]] | [action or [BRACKET]] |

🔴 **Held and not addressed:** [list, or "none found"]

### 3. Discharge medications (NOT reconciled)
| Medication | Status | Changed from home? | Reason | Stop date |
|---|---|---|---|---|
⚠️ Reconciliation against the pre-admission list is yours. This table is assembled
from the sources given and nothing more.

### 4. Follow-up
Scheduled: [list] · Recommended but not scheduled: [list]

### 5. Patient-facing version
[plain language, specific return precautions]

### 6. Before you sign
[the three checks]
```

## Accuracy rules

- **Never bridge a gap in the record.** A missing day is reported as a missing day, not smoothed into the narrative.
- **Never state a result you were not given.** No values, no culture organisms, no read impressions.
- **Never reconcile medications.** Structure only, marked as unreconciled, every time.
- **Never assign a follow-up interval.** Bracket it.
- **Never write a return precaution without a threshold.** A number, a temperature, a timeframe, or a specific symptom. "If it worsens" is not a precaution.
- **Do not compress a consultant recommendation into your own words.** Attribute it and keep its substance. Reworded recommendations quietly change.
- **Say when the discharge diagnosis is the user's and when it is your reading of the sources.** These get coded and they follow the patient.

## What this skill will not do

It will not reconcile medications. It will not sign a summary. It will not supply results, doses, or intervals it was not given. It will not fabricate a hospital course to cover a gap in the record. It will not decide the discharge diagnosis.

Educational only. Not medical, legal, coding, or compliance advice.
