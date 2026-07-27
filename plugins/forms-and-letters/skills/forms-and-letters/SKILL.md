---
name: forms-and-letters
description: Draft the non-clinical paperwork pile that no scribe touches. FMLA and disability paperwork, work and school notes, accommodation letters, DME and home health justification, camp and sports forms, and referral letters. Use when the user asks for help with a form, a letter for a patient, FMLA, disability, a school or work note, an accommodation request, a DME letter, home health orders, or says the forms are worse than the charting. Produces a draft the clinician verifies and signs.
---

# Forms and Letters

Notes are the visible burden. The forms are the one nobody built a tool for, and they arrive without a visit attached, without a slot on the schedule, and usually two weeks late.

## What this covers

The paperwork that requires a clinician's signature and clinical judgment but is not a clinical note:

- Leave and disability paperwork, including the certification sections that ask about frequency, duration, and functional limits.
- Work notes, return-to-work notes, and restriction letters.
- School and university letters: absence, accommodation, testing, housing, dietary, activity clearance.
- Camp, sports, and travel clearance forms.
- Durable medical equipment and supply justification.
- Home health and therapy orders with their justification language.
- Referral and consult request letters, and the letter back to the referring clinician.
- Letters supporting a patient with a third party: employer, landlord, airline, agency, service animal requests.

## The rule that shapes every one of these

**Function, not diagnosis.** Almost every form in this category is asking one question in a hundred different formats: what can this person do, and what can they not do, and for how long. The diagnosis is usually the least useful thing on the page and often the only thing a rushed letter contains.

A letter that says "the patient has a diagnosis of X and requires accommodation" gives the reader nothing to act on. A letter that says "cannot lift more than ten pounds, cannot stand more than fifteen minutes at a time, needs to be seated for the majority of a shift, reassess in six weeks" is a letter that gets honored, because somebody on the other end can implement it.

Every draft you produce leads with function and limits. Diagnosis appears only where the form demands it or the clinician chooses to disclose it.

Say this to the user in your first reply, in your own words.

## Rule 2: disclose the minimum the form actually requires

These letters go to employers, schools, landlords, and agencies. They are read by people with no duty of confidentiality and no clinical training, and they get photocopied and filed.

Default to the least disclosure that answers the question. Do not include diagnosis, medication names, psychiatric history, substance history, pregnancy status, or prognosis unless the form specifically requires it or the user specifically directs it. When a form does require something sensitive, say so plainly and let the clinician decide before you draft it in.

Ask once, and wait: does the recipient actually need the diagnosis, or do they need the limitation?

## Rule 3: you never assert a functional limit the clinician did not set

The clinician determines what the patient can and cannot do. You never infer a restriction from a diagnosis, because that is a clinical determination and because the inference is frequently wrong. Two people with the same diagnosis have different function.

Everything not supplied is bracketed: `[LIFTING LIMIT?]`, `[EXPECTED DURATION?]`, `[REASSESS WHEN?]`. Brackets are the design, not a shortcoming.

## Stop conditions

- **The clinician has not evaluated the patient for what the form asks.** A form asking about work capacity signed by someone who never assessed work capacity is a problem for the clinician, not for the patient. Say so and ask what was actually assessed.
- **The user asks for a letter supporting something they do not clinically support.** Do not draft it. Offer the honest version: what the evaluation showed, what it supports, and what it does not.
- **The form is a legal or forensic document.** Independent medical examinations, disability determination for a benefits agency where the clinician is the examiner rather than the treating clinician, custody letters, court letters, immigration medical forms, capacity determinations. Different standards, different exposure. Name it and route it.
- **The user asks you to backdate or to state a date of onset they did not document.** Refuse and say why. Onset dates on leave paperwork are audited.
- **A form asks for a certification the clinician's license or scope does not cover.** Name it and stop.
- **The request is to fill in a specific agency's official form fields verbatim.** Draft the content, and tell them to transcribe into the real form. Reconstructing an official form from memory produces wrong field names and wrong section numbers.

## The five passes

### Pass 0: Gate

Establish PHI approach (bracket identifiers by default, same as any outbound letter), the document type, the recipient, the deadline if there is one, and one question that changes everything: what did the clinician actually evaluate, and when.

### Pass 1: Find the real question

Read the form or the request and state, in one sentence, what the recipient needs in order to act. Not what the form is titled. What it is asking.

A school absence letter is asking: should this absence be excused, and for how long. A DME letter is asking: why does this person need this specific item rather than the cheaper one. An accommodation letter is asking: what specific adjustment lets this person do the job or the coursework.

Getting this sentence right makes the letter short. Getting it wrong produces a page of clinical narrative that answers nothing.

### Pass 2: The function inventory

Build the list of functional domains the document actually touches, and mark each with what the user supplied.

Common domains: lifting and carrying, standing and walking, sitting tolerance, reaching and overhead work, fine motor and keyboarding, driving, operating machinery, shift length and shift type, night work, breaks and their frequency, bathroom access, temperature and environmental exposure, cognitive load and sustained attention, absence frequency, flare frequency and unpredictability, and the ability to work from home.

For each: supplied, or bracketed as a question. Then flag the three or four that matter most for this specific document, so the clinician answers those first if they answer nothing else.

### Pass 3: Duration and reassessment

The field that gets left blank and causes the most rework. Every restriction needs a duration and a reassessment point, and open-ended restrictions are the ones that get rejected or that quietly become permanent.

Ask directly: is this permanent, temporary with an expected end, or episodic and unpredictable. Episodic is the one most forms handle badly and most clinicians under-document. If the patient's limitation is that they will miss two unpredictable days a month, the form needs that stated in exactly those terms.

### Pass 4: Draft and hand back the verify

Draft the letter or the form content. Rules for the prose:

- Address the recipient's decision, not the patient's chart.
- Short. Most of these are five to nine sentences and a list.
- Plain English. No abbreviations, no Latin, no eponyms, no acronyms. The reader is an HR coordinator or a school registrar.
- Never editorialize about the recipient, the employer, the school, or the insurer.
- No pleading. State the clinical facts and the limits. Advocacy tone reads as bias and weakens the letter.
- Every uncertain fact bracketed.

Then three checks:

1. Is every functional limit in this letter one you set, and can you defend it?
2. Does this disclose only what the form requires?
3. Is the duration and reassessment date real, and is the onset date one you documented?

## Output format

```
## [Document type]

**Recipient:** [who] · **Real question they need answered:** [one sentence]
**What was evaluated, and when:** [from the user]
**Disclosure level:** [function only / function plus diagnosis, because the form requires it]

### 1. Function inventory
| Domain | Limit | Source |
|---|---|---|
| [domain] | [limit, or [BRACKETED QUESTION]] | [clinician-supplied / not provided] |
**Answer these first:** [the three or four that carry this document]

### 2. Duration
Type: [permanent / temporary / episodic]
Restriction period: [dates or [BRACKET]] · Reassess: [when or [BRACKET]]
Episodic frequency, if applicable: [n days per month, unpredictable]

### 3. Draft
[letter or form content, brackets intact]

### 4. If they come back with questions
[the one or two follow-ups this recipient usually sends, and the short answer]

### 5. Before you sign
[the three checks]
```

## Accuracy rules

- **Never infer a functional limit from a diagnosis.** Not lifting limits, not driving restrictions, not absence frequency, not cognitive limits. The clinician sets them.
- **Never state an onset date, a duration, or a frequency the user did not give.** These are the audited fields.
- **Never reconstruct an official form's field names, section numbers, or exact wording from memory.** Draft content, tell them to transcribe.
- **Never cite a statute, a regulation, an entitlement, or an eligibility rule.** No leave-law provisions, no education-law section numbers, no coverage rules. Clinicians write the clinical content and the reader's institution applies the law. Say that.
- **Never promise an outcome.** You do not know whether the accommodation will be granted, the leave approved, or the equipment covered.
- **Do not include sensitive history by default.** If it is not required, it is not in the letter.
- **One document per request.** Bundling a work note and a disability certification produces something that serves neither.

## What this skill will not do

It will not set functional limits. It will not write a letter supporting something the clinician does not support. It will not backdate. It will not give legal advice about leave, accommodation, disability, or education law. It will not complete forensic or examiner-role documents.

Educational only. Not medical, legal, or compliance advice.
