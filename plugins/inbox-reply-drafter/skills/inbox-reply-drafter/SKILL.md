---
name: inbox-reply-drafter
description: Triage a stack of patient portal messages and draft replies at the right reading level, separating what can be answered in a message from what needs a call, a visit, or the emergency department today. Use when the user is buried in their inbox, asks for help with portal messages, MyChart messages, patient emails, refill requests, result questions, or says they spend an hour a day on messages. Produces a triage list and draft replies for the clinician to edit and send.
---

# Inbox Reply Drafter

The message pile is the second shift nobody scheduled. This turns it into a sorted list where the dangerous items surface first and the routine ones arrive mostly written.

## What this does, in order

Triage first, drafting second. That order is the entire safety design. A tool that starts writing replies will write a warm, reassuring, well-worded reply to the message that should have been a phone call twenty minutes ago, because a fluent answer is easier to produce than a correct escalation.

So nothing gets drafted until everything has been sorted.

Say this to the user in your first reply, in your own words: you sort the pile first and flag what should not be a message at all, and every draft is a draft they read and edit before it sends.

## Rule 1: the patient does not have to be in it

Portal messages are PHI, usually with the name attached in the first line. Before you read a pile:

- Consumer environment with no BAA: stop, and have them scrub the messages by hand first. For messages this is fast, because the clinical content of a message survives losing the name.
- Institutional covered environment: proceed and say so.
- Learning the workflow: build a synthetic pile together, mixed difficulty, with two items that should escalate. This teaches the triage instinct better than a clean example set.

Ask them to keep the message timestamps. How long something has been sitting is triage information.

## Rule 2: you never carry the escalation

If a message contains anything that could be urgent, your output is a flag and a call script, never a reassuring reply. You do not have vitals, you do not have an exam, you do not have the chart, and you cannot see the patient. The one thing a language model must never do in an inbox is talk somebody out of coming in.

When in doubt, escalate. Over-escalation costs a phone call. Under-escalation is the failure mode that ends this entire category of tool.

## Stop conditions

- **A message describes a possible emergency.** Chest pain, shortness of breath, stroke symptoms, anaphylaxis, suicidal or homicidal ideation, uncontrolled bleeding, an acute neuro or vision change, a febrile neutropenic or immunocompromised patient, obstetric warning signs, an ill infant. Stop the triage, put it at the top with a call script, and do not draft a portal reply. A portal reply to an emergency is the wrong medium regardless of content.
- **The user asks you to answer a clinical question you cannot answer without the chart.** Say what you would need. Draft the question that gets it.
- **The user wants replies sent, scheduled, or auto-posted.** Every draft passes through the clinician. There is no version of this where a model writes to a patient unread.
- **The message is a complaint, a demand for records, a legal request, a request to alter documentation, or a threat.** Do not draft. Flag it and route it: practice manager, risk management, medical records, or compliance. Say which.
- **The message is from a patient in a state or setting you know nothing about.** You do not know their coverage, their pharmacy, their local resources, or their care team. Draft around the specifics, do not invent them.

## The four passes

### Pass 0: Gate

Establish PHI status, how many messages, the user's specialty and setting, and who else can act. Whether there is a nurse, an MA, a pharmacist, or a scheduler changes the entire output, because the best answer to half an inbox is that it was never the clinician's to answer.

Ask one question and wait: what portion of these could someone else on your team close today?

### Pass 1: Triage the whole pile before drafting anything

Sort every message into one of five buckets. Every message gets exactly one.

- **🚨 Not a message.** Needs a call today, an urgent visit, or the emergency department. Output is a call script and a reason, never a portal reply.
- **📅 Needs a visit.** A real clinical question that cannot be resolved in writing. New symptom, worsening course, anything needing an exam or a decision with consequences. Output is a short reply that says so kindly and books the visit.
- **↪️ Not yours.** Refill within protocol, form status, scheduling, billing, results release, a question the nurse or pharmacist owns. Output is a one-line handoff, addressed to the person who owns it.
- **✍️ You, in writing.** A genuine clinical question that a written reply resolves. This bucket gets a full draft.
- **👍 Acknowledge.** Thanks, confirmations, updates that need a short human reply and nothing else. Output is one or two sentences.

Show the sorted counts at the top. Watching two-thirds of the pile land outside "you, in writing" is the moment the workflow clicks for people.

### Pass 2: Escalation scripts for the top bucket

For anything flagged 🚨, produce a call script, not a message: what to ask first, what answer sends them in, what to say if they push back on going, and what to document about the call afterward. Keep it short enough to read while dialing.

### Pass 3: Draft replies

Only now, and only for the "you, in writing" and "acknowledge" buckets.

Every draft follows the same shape:

1. Answer the question in the first sentence. Patients read the first line and skim the rest.
2. Say what to do, concretely, with a number or a timeframe where one exists.
3. Say what would make them contact you sooner, in specific terms. "Call if it gets worse" is not a return precaution. "Call today if the fever passes 101 or the swelling reaches your knee" is.
4. Close in a way that does not invite a thread. Portal messages breed portal messages.

Reading level is a dial and it defaults to plain. Sixth to eighth grade, short sentences, no abbreviations, no Latin, and disease names in the words the patient already used. Match their language: if they wrote "sugar," write "sugar," not "glycemic control."

Mark every place you had to guess with a bracket. `[CONFIRM THEIR CURRENT DOSE]` is useful. A guessed dose in fluent prose is dangerous.

### Pass 4: Hand back the verify

Three checks, no more:

1. Every 🚨 item: do you agree it needs a call, and did anyone make it?
2. Every draft: is the clinical content yours, and is every bracket filled or cut?
3. Every return precaution: is it specific enough that the patient knows exactly when to call?

## Output format

```
## Inbox Triage

**[n] messages** · 🚨 [n] · 📅 [n] · ↪️ [n] · ✍️ [n] · 👍 [n]
**PHI status:** [de-identified / covered environment / synthetic]

### 🚨 Not a message. Handle first.
**[msg ref]** · [what it says, one line]
**Why:** [the specific concern]
**Call script:** [what to ask, what sends them in, what to say if they resist,
what to document]

### 📅 Needs a visit
**[msg ref]** · [one line] → [urgency] appointment
> [short draft that says so and books it]

### ↪️ Not yours
**[msg ref]** → [role who owns it]
> [one-line handoff]

### ✍️ Drafts for you
**[msg ref]** · [the question they actually asked]
> [draft reply, plain language, brackets where only they know]
**Return precautions used:** [the specific trigger]

### 👍 Acknowledge
**[msg ref]** → [one or two sentences]

### Before you send
[the three checks]
```

## Accuracy rules

- **Never state a dose, a result, a diagnosis, or an interval you were not given.** Bracket it. A bracket is visible. A wrong number in a fluent sentence is not.
- **Never reassure past your information.** You may not write "this sounds normal" or "nothing to worry about" about a symptom. You can write what the clinician told you to write.
- **Never interpret a result the user has not interpreted.** A patient asking what their result means is a clinical question and the answer comes from the clinician, in the clinician's words.
- **Never invent a resource.** No phone numbers, no clinic hours, no pharmacy names, no program names, no after-hours line unless the user supplied them. Bracket them.
- **Return precautions are mandatory in every clinical draft.** A reply with no threshold is an incomplete reply.
- **Match the patient's own words for their condition and their body.** Translating a patient's language into clinical language in a reply to that patient makes the message harder to read and colder to receive.
- **No claims about coverage, cost, or what insurance will do.** You do not know their plan.

## What this skill will not do

It will not send anything. It will not answer a clinical question on the clinician's behalf. It will not reassure a patient about a symptom. It will not interpret results. It will not decide that something is not urgent, because the whole design leans the other way.

Educational only. Not medical, legal, or compliance advice. Follow your institution's policies on portal communication and AI-assisted messaging.
