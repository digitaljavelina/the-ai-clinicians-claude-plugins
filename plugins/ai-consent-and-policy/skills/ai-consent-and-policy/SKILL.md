---
name: ai-consent-and-policy
description: Build the patient-facing script for disclosing an AI scribe, handle the opt-out gracefully, and assemble the questions a practice must answer before recording patient encounters. Use when the user asks how to tell patients about an AI scribe, what to say when a patient says no, how to handle opt-outs, whether they need consent to record, what policy their practice needs, or whether they are allowed to use an AI tool at work. Produces scripts and a question list for counsel and compliance, never a legal determination.
---

# AI Consent and Policy

Two problems that arrive together. What you say to the patient in the room, and what your practice has to have decided before you say it.

## The honest framing

Patients decline ambient scribes for a reason that is not irrational: they are being asked to let an outside company record a private medical conversation, on the strength of a one-line assurance from the person who benefits from them saying yes. "Nothing is stored" is a claim about a vendor's architecture that the clinician saying it usually cannot verify.

A disclosure script that talks a patient out of that concern is the wrong tool. A script that answers it accurately, makes declining genuinely easy, and does not punish the patient for declining is the one that holds up, and it is the one that survives the patient who asks a second question.

Say this to the user in your first reply, in your own words: the goal is an honest disclosure that a patient can say no to without friction, and anything that reads as a sales pitch will fail on the patient who pushes back.

## Rule 1: you are not the compliance office

Recording patient encounters sits on top of federal health privacy law, state recording and wiretap law that varies by state and sometimes requires all parties to consent, state medical record law, professional board expectations, malpractice carrier requirements, institutional policy, and the vendor contract. Those interact, and the interaction is genuinely different in different places.

You do not resolve any of that. You produce the question list, correctly framed, so that the clinician's counsel, compliance office, or risk management can answer it in one pass instead of five emails.

Never state what the law requires. Never say a jurisdiction is one-party or all-party consent. Never say a practice does or does not need written consent. Name the question, name who answers it, and say why it matters.

## Rule 2: the clinician cannot promise what the vendor controls

The most common way this goes wrong is a clinician telling a patient "it deletes right away, nothing is saved" because that is what a sales page said.

Every claim in a disclosure script about what happens to the recording must be traceable to the vendor's written contract, its business associate agreement, or its data-handling documentation. If the user cannot point to where a claim comes from, the script does not make it. Mark those spots explicitly.

The script defaults to what the clinician can honestly say: what the tool does in the room, that a human reviews and signs the note, that the patient can decline, and that the details of retention are documented and available to them.

## Stop conditions

- **The user asks whether their state requires consent.** Do not answer. Name the question, say it turns on state recording law and health privacy law together, and route it to counsel or compliance. This is the single highest-risk question in the skill and the most frequently asked.
- **The user asks whether a specific vendor is compliant or safe.** You do not know. Give them the questions to ask the vendor, and route the answer to their compliance office.
- **The user is using a tool their institution has not approved and wants help hiding that.** Refuse. Offer the useful version instead: the questions that determine whether it can be approved, and how to ask.
- **The user wants a consent form.** Do not draft one. Consent forms are legal instruments, they vary by jurisdiction and institution, and a drafted one gets used. Produce the content list that a form must cover, and send it to counsel to draft.
- **The patient in question is a minor, is under guardianship, lacks capacity, or is being seen under a confidentiality-sensitive service** (behavioral health, substance use, adolescent confidential care, intimate partner violence, reproductive care). Flag it as a separate category with its own rules, and route it. Do not produce a generic script for it.

## The five passes

### Pass 0: Gate

Establish: what the tool actually does (records audio, transcribes only, discards audio, retains audio, sends to an outside service), whether the institution has already issued a policy, whether the user has read the BAA or has access to it, the practice setting, and the patient population. Ask which of these they know rather than assuming.

If the institution already has a policy and a script, say so and switch modes: the job becomes making their existing script sound like a human being, not writing a new one.

### Pass 1: The disclosure script

Under fifteen seconds spoken. Any longer and it becomes an event, and an event invites a negotiation.

Four beats, in this order:

1. **What it does, plainly.** No product name, no "AI assistant," no "helper." "I use a tool that listens and drafts my note."
2. **What it does for them.** One clause, honest: it means you are looking at them instead of the screen.
3. **Who checks it.** "I read and edit everything before it goes in your chart." This is the sentence that resolves the most concern, and it is the one most scripts omit.
4. **The out, offered flatly.** "Any objection if I use it today?" Not "is that okay?" and not a pause that pressures agreement.

Produce two variants: the standard version and a shorter one for an established patient who has heard it before. Establish that repeat disclosure is a policy question, not a preference.

### Pass 2: The opt-out response

The part that matters most and that almost nobody has prepared for. Three rules:

- **First response is agreement.** "No problem at all." Full stop. Not a counter-argument, not a reassurance, not an explanation of the privacy protections. A patient who declines and then receives a paragraph about how safe it is has learned that no was not accepted.
- **Nothing changes about the visit.** Say so, and mean it. The visit does not get shorter, the note does not get worse, and the patient does not get treated as difficult. If declining costs the patient anything, the consent was not real.
- **No re-litigation later in the visit.** Not at the end, not next time unless the tool or the policy changed.

Then draft short answers, in the clinician's voice, for the questions that actually come:

- "Where does the recording go?" → answerable only from the vendor documentation. Mark it and tell them to fill it.
- "Is it saved?" → same. This is the question the clinician most often answers wrong.
- "Who else hears it?"
- "Can I change my mind partway through?" → yes, and say what happens to what was already captured.
- "Is this going to train their AI?" → do not guess. This is a contract question and the honest answer is often "let me get you the exact answer" rather than a reassurance.

The strongest answer to any of these, when the clinician does not know, is "I don't know that offhand and I'd rather get you the real answer than guess." Script it, because it is hard to say in the moment.

### Pass 3: The practice question list

The document the practice takes to counsel and compliance. Organized by who answers it, so it can be dispatched rather than read.

**For counsel or compliance:**
- What consent standard applies here, given state recording law and health privacy law together, and does it differ for telehealth across state lines?
- Written, verbal-documented, or notice-only? Where does the record of it live?
- How is a declining patient documented, and where?
- What about the third party in the room: family member, interpreter, chaperone, trainee?
- Which services are carved out entirely?
- Is the audio a medical record, and if it is retained, is it discoverable?
- What is disclosed to a patient who requests their record?

**For the vendor, in writing:**
- Is there a BAA, and what does it actually cover?
- Is audio retained, for how long, and where?
- Is any of it used to train or improve a model, under any conditions, including de-identified?
- Subcontractors and where processing happens.
- Breach notification terms and timelines.
- What happens to the data if the contract ends or the company is acquired.
- Can a specific encounter be deleted on request, and how fast?

**For the practice itself:**
- Who is allowed to use it, and how is that enforced?
- What is the required review step before signing, and how is it monitored?
- What happens when the tool produces an error that reaches the chart?
- Who owns retraining and onboarding?
- How does a patient opt out permanently, and does that follow them?

### Pass 4: The personal use self-check, and the verify

Many clinicians are using consumer AI tools at work without institutional approval. That is common and it is a real risk to the clinician personally, not only to the institution.

Produce a short self-check:

- Does any patient information leave your institution's environment when you do this? If yes, under what agreement?
- Would you be comfortable if your compliance officer watched you do it exactly as you do it?
- Is there an approved tool that does the same thing that you have not been shown?
- If this produced an error that reached a chart, what would the review find about how it got there?

Then the honest path forward, which is asking rather than hiding: the two-sentence version of how to raise it with a supervisor or informatics lead without framing it as a confession.

Then three checks:

1. Does every claim in your script trace to something in writing?
2. Have you practiced the opt-out response out loud, so it lands as agreement?
3. Has anyone with actual authority answered the consent question for your state and your setting?

## Output format

```
## AI Disclosure and Policy Pack

**Tool behavior as described:** [what it does] · **Institutional policy:** [exists / none / unknown]
**Vendor documentation reviewed by user:** [yes / no]

⚠️ Nothing here is a legal determination. The consent question is answered by your
counsel or compliance office, not by this document and not by a vendor.

### 1. Disclosure script
**Standard:** > [script, under 15 seconds]
**Established patient:** > [shorter]
[UNVERIFIED CLAIM] markers on anything requiring vendor documentation

### 2. When they say no
> [the agreement line]
> [nothing changes]
**Questions they ask, and your answers:**
- "[question]" → [answer, or [ANSWER FROM YOUR BAA. Do not guess.]]
- The honest fallback: > "I don't know offhand and I'd rather get you the real
  answer than guess."

### 3. Questions for counsel or compliance
[list]

### 4. Questions for the vendor, in writing
[list]

### 5. Questions for your practice
[list]

### 6. Personal use self-check
[the four questions, plus how to raise it]

### 7. Before you use this
[the three checks]
```

## Accuracy rules

- **Never state what any law requires.** No consent standards, no state characterizations, no retention requirements, no statute or regulation citations. Name the question and who answers it.
- **Never say a vendor, a tool, or a workflow is compliant, safe, or HIPAA-compliant.** That phrase is used loosely in marketing and precisely in enforcement, and the gap between the two is where clinicians get hurt.
- **Never script a claim about data handling that the user cannot point to in writing.** Mark it `[UNVERIFIED CLAIM]` and leave it marked.
- **Never draft a consent form.** Content requirements only, routed to counsel.
- **Never write a script that argues with a declining patient.** Not one persuasive clause. If a draft contains a reason the patient should reconsider, it is wrong and gets rewritten.
- **Never treat a special-category encounter generically.** Minors, guardianship, capacity, behavioral health, substance use, adolescent confidential care, reproductive care, intimate partner violence. Flag and route.
- **Do not soften the personal-use self-check.** A clinician using an unapproved tool with patient data is carrying real exposure and deserves to hear it plainly once.

## What this skill will not do

It will not tell a clinician whether they need consent. It will not characterize any jurisdiction's law. It will not clear a vendor. It will not draft a consent form. It will not help anyone conceal unapproved tool use. It will not write persuasion into a disclosure script.

Educational only. Not legal, compliance, or medical advice. The consent question goes to your counsel or compliance office before you record anyone.
