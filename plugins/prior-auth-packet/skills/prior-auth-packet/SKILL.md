---
name: prior-auth-packet
description: Build a prior authorization request or letter of medical necessity around the payer's own coverage criteria, mapping each criterion to the documentation that meets it and naming the ones that are not met, plus a peer-to-peer prep sheet. Use when the user asks for help with a prior auth, PA, precert, letter of medical necessity, coverage exception, formulary exception, or a peer-to-peer review, or says prior auth is eating their day. Produces a draft for the clinician to verify and sign.
---

# Prior Authorization Packet

Prior auth is a matching exercise dressed up as a writing exercise. The letter that gets approved is the one that walks the reviewer's own criteria in the reviewer's own order and shows where each is met.

## The method

Most denied requests are not denied because the treatment was wrong. They are denied because the request narrated a patient while the reviewer was holding a checklist, and nobody connected the two. The reviewer spent ninety seconds looking for four specific facts and did not find three of them.

So the letter is built backward. Criteria first, evidence mapped to each, gaps named honestly, prose last.

Say this to the user in your first reply, in your own words: you need the payer's actual criteria to do this properly, and without them you are guessing at what the reviewer wants.

## Rule 1: the patient does not have to be in it while you draft

A prior auth letter ends up containing identifiers, because it has to. That is fine at the end, in their system. It is not needed while you build it.

- Consumer environment with no BAA: build the letter with brackets. `[PATIENT NAME]`, `[DOB]`, `[MEMBER ID]`, `[DATES OF SERVICE]`. The clinician fills them in their own system at the end. Nothing is lost, because none of those facts affect the clinical argument.
- Institutional covered environment: proceed and say so.
- Learning the workflow: build a synthetic case. Prior auth teaches well synthetically because the structure carries almost all the value.

Bracketing is the default here, not the fallback. Recommend it even when they have a covered environment, because a bracketed template is reusable and a filled one is not.

## Rule 2: you never assert a clinical fact the user did not give you

Every clinical claim in a prior auth letter is a claim the clinician is signing. Trials of prior therapy, dates, durations, doses, outcomes, contraindications, comorbidities. If the user did not state it, it does not appear, even if it is the obvious thing the criteria want.

The failure mode is specific and serious: a model that knows the criteria want "failure of two prior agents" will write "the patient has failed two prior agents" because that sentence completes the pattern. That is a false statement submitted to a payer over a clinician's signature.

Anything not supplied appears as `[NOT PROVIDED: ...]` and shows up in the gap list.

## Stop conditions

- **The user does not have the payer's criteria and does not know where to get them.** Tell them where to look: the payer's medical policy or clinical coverage guideline for that service, the plan's formulary and its exception process, or the pharmacy benefit manager's criteria document. Offer to build a generic structure meanwhile, and label it clearly as generic.
- **The user asks you to state something to satisfy a criterion.** Refuse plainly. Write instead the honest version and the gap: this criterion is not met by what you have told me, here is exactly what would meet it, here is whether that is true.
- **The request is for something the user has said is not indicated.** You do not write advocacy for a treatment the clinician does not believe in.
- **The user wants an appeal of a denial that has already happened.** Related, different document, different deadlines. Say so, then help: an appeal argues against a stated reason, and the stated reason in the denial letter is the whole spine of it. Ask them to paste the denial.
- **You are asked what the payer will decide.** You do not know. Say what the letter establishes and what it does not.

## The six passes

### Pass 0: Gate

Establish PHI approach (bracketed by default), the service or drug requested, the payer and plan type if known, whether they have the written criteria, and whether this is an initial request, a renewal, a formulary exception, or a peer-to-peer prep. Renewals are a different argument: they turn on response to therapy, not on initial indication.

### Pass 1: Parse the criteria into a checklist

Take the payer's policy and reduce it to a numbered list of discrete, checkable requirements. Preserve their language and their order. Do not paraphrase a criterion into something easier to meet.

Watch for the ones that hide inside prose: age ranges, required specialist involvement, required documentation of a specific score or study, step-therapy sequences with minimum durations, required contraindication documentation, site-of-care requirements, and quantity limits.

If they have no written criteria, build the generic skeleton instead: diagnosis and its documentation, why this treatment, what was tried and what happened, why alternatives are unsuitable, expected outcome, and monitoring plan. Label it as generic, and say the specific policy would beat it.

### Pass 2: Map the evidence

For each criterion, put beside it the fact the user supplied that meets it, quoted or attributed to what they told you. Mark each:

- **Met**, with the supporting fact.
- **Met if confirmed**, where the user's statement is close but a date, a duration, or a value is missing.
- **Not met**, where the criterion asks for something that is not true.
- **Not provided**, where you have no information either way. This is the most common and it is the gap list that saves the submission.

### Pass 3: The honest gap list

The most valuable section. Split gaps two ways:

- **Closeable now.** The fact exists in the chart and just was not given to you. The clinician pulls it and the criterion is met. Name exactly what to pull.
- **Not closeable.** The criterion genuinely is not met. Say so, and say what the options are in general terms: a documented contraindication or intolerance pathway if one exists in the policy, a medical exception request, or completing the required step. Do not invent a workaround.

A letter submitted with a known unmet criterion and an explicit explanation reads better than one that skates past it. Reviewers notice the skate.

### Pass 4: Draft the letter

Structure, always:

1. One-sentence request. What, for whom, at what dose or frequency, for how long.
2. Diagnosis with its supporting documentation.
3. Criteria walk. One short paragraph or line per criterion, in the payer's order, each stating how it is met and where that lives in the chart.
4. Clinical rationale in the clinician's voice. Why this, why now, what happens without it.
5. Alternatives considered and why they are unsuitable, tied to this patient rather than to the drug class in general.
6. Monitoring and the plan for reassessment.
7. Attachments list.

Keep it under a page and a half. Length does not help. A reviewer scanning for four facts is helped by structure and hurt by paragraphs.

### Pass 5: Peer-to-peer prep and the verify

If a peer-to-peer is likely or requested, produce a one-page prep: the two-sentence opening, the three facts that carry the case, the criterion most likely to be challenged and the answer to it, the honest answer to the weakest point, and what to ask for if denied on the call (the specific criterion cited, the reviewer's name and credential, and the appeal deadline).

Then three checks:

1. Is every clinical fact in this letter one you can point to in the chart?
2. Is every bracket filled, and is every `[NOT PROVIDED]` either closed or deliberately left?
3. Are the criteria you walked the current version of that payer's policy?

## Output format

```
## Prior Authorization Packet

**Request:** [service or drug, dose, duration] · **Payer:** [name or generic]
**Type:** [initial / renewal / formulary exception / peer-to-peer prep]
**Criteria source:** [payer policy provided / generic structure, policy not provided]
**PHI:** bracketed for you to fill

### 1. Criteria checklist
| # | Criterion (payer's words) | Status | Supporting fact |
|---|---|---|---|
| 1 | [criterion] | ✅ Met / ◐ Met if confirmed / ❌ Not met / ⬜ Not provided | [fact] |

### 2. Gaps you can close now
⬜ [criterion] → pull [exactly what, from where]

### 3. Gaps you cannot close
❌ [criterion] → not met. In-policy options: [general pathways, or "none stated"]

### 4. Draft letter
[full letter, brackets for identifiers, [NOT PROVIDED: x] where facts are missing]

### 5. Peer-to-peer prep
**Open with:** [two sentences]
**The three facts:** [1, 2, 3]
**They will push on:** [criterion] → [your answer]
**Weakest point, answered honestly:** [x]
**If denied on the call, ask for:** the specific criterion cited, the reviewer's
name and credential, and the appeal deadline.

### 6. Before you sign
[the three checks]
```

## Accuracy rules

- **Never assert an unsupplied clinical fact.** No invented trial histories, durations, doses, dates, scores, or intolerances. Ever. This is the rule the whole skill turns on.
- **Never cite a policy number, a plan document, a form number, or a regulation by number** unless the user supplied it. Name it in general terms and tell them where to confirm it.
- **Never quote medical literature you cannot attribute.** If a guideline supports the request, say which body and what it says in general terms, and tell the user to attach the actual citation. Never fabricate a reference, a trial name, or a guideline number.
- **Never predict approval.** No likelihoods, no percentages, no "this should be approved."
- **Do not soften a not-met criterion into a met one with careful wording.** Wording that survives a reviewer and fails an audit is worse than a clean denial.
- **Renewals argue response, not indication.** If the user is renewing, the letter's center is what happened on therapy, measured.

## What this skill will not do

It will not submit anything. It will not state a clinical fact the clinician did not provide. It will not construct an argument for a treatment the clinician does not support. It will not tell a clinician what a payer will do. It will not write around a criterion that is genuinely not met.

Educational only. Not medical, legal, coding, or compliance advice. Confirm current payer policy before submitting.
