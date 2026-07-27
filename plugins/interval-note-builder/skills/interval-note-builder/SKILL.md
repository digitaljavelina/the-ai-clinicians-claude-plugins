---
name: interval-note-builder
description: Build the carry-forward scaffold for a progress, rounding, continuity, or follow-up note so active problems do not vanish when nobody mentions them out loud today. Use when the user says their AI scribe is fine for admissions but terrible for daily or follow-up notes, that problems keep dropping off, that they keep rewriting prompts for continuity notes, or asks for help with a rounding note, interval note, progress note, or day-two-onward documentation. Produces a problem scaffold and a status question list, never a finished note.
---

# Interval Note Builder

Ambient tools are good at first encounters and bad at every encounter after that. This is the fix.

## The problem this solves, precisely

A first encounter is a complete story told out loud. Everything the note needs gets said in the room, so a tool that listens to the room can write it.

An interval note is different. It is mostly carried state. The antibiotic that started Thursday, the drain that is still in, the anticoagulation that is still held, the culture that is still pending, the taper that is on day three. None of that gets said today, because everyone caring for the patient already knows it. A tool that only hears today's conversation writes a note that silently drops it, and the chart then reads as though those problems resolved.

The failure is not a bad sentence. It is an absence, which is much harder to catch on a read-through.

So the fix is not a better prompt for the scribe. It is a scaffold you build before the encounter and hand to the scribe as context, plus a status sweep you run after.

Say this to the user in your first reply, in your own words: you are building the skeleton, they are putting today's findings on it, and nothing here is a finished note.

## Rule 1: the patient does not have to be in it

An interval note and a prior note are both PHI. Before you read either:

- Consumer environment with no BAA: stop, and have them scrub the note by hand first.
- Institutional covered environment: proceed and say so.
- Learning the workflow: build a synthetic case together. This one teaches well synthetically, because the carry-forward failure is easy to demonstrate on purpose.

Keep relative durations when redacting. "Day 4 of ceftriaxone," "post-op day 2," "third cycle" are the entire substance of an interval note and they identify nobody. Calendar dates can go.

## Rule 2: you build the scaffold, they fill the findings

You produce structure and questions. They produce clinical content. You never write a finding, a value, an exam element, or an assessment they did not give you.

This is not caution for its own sake. A scaffold that arrives pre-filled with plausible content gets signed with the plausible content still in it. Empty slots get filled by the person who knows.

## Stop conditions

- **No prior note, no problem list, and no summary from the user.** The whole method depends on knowing what is already running. Ask for one of the three. If they genuinely have nothing, tell them this becomes a first-encounter note and the carry-forward pass does not apply.
- **The user wants a complete note generated from a one-line update.** Name what is missing rather than filling it in. A note built from four words is a note built from your assumptions.
- **The patient is unstable or the ask is what to do next.** This is a documentation tool. Clinical management questions go to the clinician, the team, and the relevant reference. Say so and stop.

## The five passes

### Pass 0: Gate

Establish PHI status, setting (inpatient rounding, post-op, outpatient follow-up, infusion, consult follow-up, telehealth), and what source you have: prior note, problem list, discharge instructions, or the user's own recollection. Name which, because it determines how confident the scaffold can be.

### Pass 1: Extract the carried state

From the prior note or problem list, pull every item that has a state that persists past today. Do not summarize the prior note. Extract the running threads.

Look specifically for:

- **Active medications with a clock on them.** Antibiotics with a day number and a planned stop, steroid tapers, anticoagulation, chemotherapy cycles, insulin adjustments, anything titrated.
- **Held or stopped medications, and what would restart them.** The most commonly dropped item in the entire chart. A hold with no restart condition becomes a permanent discontinuation by accident.
- **Devices and lines.** Drains, catheters, central access, wound vacs, tubes, external fixation, packing. Each with a day count and a removal plan if one exists.
- **Pending results.** Cultures, pathology, imaging read, consult recommendation, genetics, level draws.
- **Consultants engaged and what was asked of them.**
- **Diet, activity, weight-bearing, and precaution status.**
- **Open decisions with a trigger.** "If afebrile 48 hours, narrow." "If the drain is under 30, pull it." These are the items where a dropped thread does actual harm.
- **Disposition barriers.** What has to be true before this patient leaves.

Output this as the scaffold, one line per thread, each carrying its day count or interval.

### Pass 2: The status sweep

For every thread in Pass 1, generate the one question that resolves it today. Not a paragraph. One question, answerable in a few words while walking.

The sweep is the deliverable people actually use. It is what a clinician reads before they walk in, so that the things nobody will say out loud get said.

Group by how fast they change. Threads that move daily go first.

### Pass 3: The unspoken-problem check

Take today's encounter content, whether that is a scribe draft, a dictation, or the user's own account, and compare it against the scaffold.

Report every thread from Pass 1 that today's content does not touch. For each, ask the resolution question: resolved, ongoing unchanged, ongoing changed, or simply not discussed. Those four states are not the same and the note should say which.

An item that is ongoing and unchanged still belongs in the note. That is the whole point. Silence is not documentation.

### Pass 4: Assemble the shell and hand back the verify

Produce the note shell: the problem-oriented skeleton with each thread in place, day counts current, and clearly marked empty slots where today's findings go. Empty slots stay empty.

Then three checks:

1. Is every day count and interval in the scaffold right, given what you know today?
2. Every thread you marked "not discussed": is it ongoing, or did it resolve and nobody wrote it down?
3. Every empty slot: is it filled with what you found, in your words?

## Output format

```
## Interval Note Scaffold

**Setting:** [type] · **Source:** [prior note / problem list / user summary]
**PHI status:** [de-identified / covered environment / synthetic]

### 1. Carried state
| Thread | Status as of last note | Clock | Trigger or plan |
|---|---|---|---|
| [problem or item] | [state] | [day n / cycle n / interval] | [what changes it] |

### 2. Today's status sweep
Ask before you write. One line each.
**Moves daily:**
- [ ] [question]
**Moves slower:**
- [ ] [question]

### 3. Threads today's encounter did not touch
🔴 [thread] → resolved, ongoing unchanged, ongoing changed, or not discussed?

### 4. Note shell
[problem-oriented skeleton, day counts current, findings slots marked
[TODAY: ______] and left empty]

### 5. Before you sign
[the three checks]
```

## Accuracy rules

- **Never carry a value forward as current.** A lab from the prior note is a prior lab and gets labeled with when it was drawn. Carrying a number forward without its date is how a stale value becomes today's justification.
- **Never fill a findings slot.** Not with likely findings, not with the prior note's findings, not with "stable" as a default. Empty means empty.
- **Never invent a day count.** If the prior note does not establish when something started, say the count is unknown and ask.
- **Extract, do not paraphrase.** A carried thread should be recognizable to whoever wrote the prior note. Rewording a plan quietly changes it.
- **Flag guidance that may have moved.** If a carried plan depends on something that changes, say so and tell them to check it against a current source rather than trusting the carry-forward.
- **Say when the prior note is thin.** If the source does not establish the running threads, the scaffold is a guess and the user needs to hear that before they rely on it.

## What this skill will not do

It will not write a note. It will not supply findings, values, or assessments. It will not make management recommendations. It will not decide that a problem resolved. It hands the clinician a structure and a list of questions, and the clinician answers them.

Educational only. Not medical, legal, coding, or compliance advice.
