# E/M Code Tables by Setting (2023 CPT / Medicare)

Read this file to map a setting + patient type + MDM level (or documented time) to a
specific CPT code. Never state a code or a time threshold from memory. The thresholds
below are exact and were verified against the AMA 2023 E/M descriptors and CMS
guidance; the value of this file is that it is right.

`CPT © American Medical Association.` Educational summary of the AMA 2023 E/M
descriptors and CMS MLN006764 (May 2026). Medicare rules are noted where they differ
from CPT. Confirm against a current CPT codebook, the CY Physician Fee Schedule, and
your MAC's local coverage before billing. Commercial payers may differ.

## How time behaves, by setting (this trips people up)

- **Office/outpatient** codes use a time **range** (e.g., 99214 = 30–39 min). Past the top of the top code's range you add a prolonged code.
- **Hospital, nursing facility, home/residence** codes use a single **floor** ("X minutes must be met or exceeded"). There is no upper bound on the base code; past a further threshold you add a prolonged code.
- **Emergency department** codes have **no time option at all.** Level is by MDM only.
- When you select by time, count total time (see `SKILL.md`, and it must be documented). You may bill by MDM **or** time, whichever the documentation supports at the higher level, except ED which is MDM only.

---

## Office or Other Outpatient (O/O)

Select by MDM **or** total time. New vs established turns on whether the patient had a
professional service from this clinician (or a same-specialty, same-group colleague)
in the prior 3 years.

**New patient** (99201 was deleted in 2021):

| Code | MDM | Total time (range) |
|---|---|---|
| 99202 | Straightforward | 15–29 min |
| 99203 | Low | 30–44 min |
| 99204 | Moderate | 45–59 min |
| 99205 | High | 60–74 min |

**Established patient:**

| Code | MDM | Total time (range) |
|---|---|---|
| 99211 | N/A — may not require the presence of a physician/QHP (typically a nurse visit) | none defined |
| 99212 | Straightforward | 10–19 min |
| 99213 | Low | 20–29 min |
| 99214 | Moderate | 30–39 min |
| 99215 | High | 40–54 min |

**Prolonged O/O:** past the top of 99205 (≥75 min) or 99215 (≥55 min), add **G2212** (Medicare) or **99417** (CPT), per 15 minutes. See prolonged table below.

---

## Hospital Inpatient or Observation

Inpatient and observation are one merged code set (2023). Select by MDM **or** total
time on the calendar date. Only one initial or one subsequent code per calendar date.

**Initial** (per day):

| Code | MDM | Time (floor) |
|---|---|---|
| 99221 | Straightforward or Low | ≥40 min |
| 99222 | Moderate | ≥55 min |
| 99223 | High | ≥75 min |

**Subsequent** (per day):

| Code | MDM | Time (floor) |
|---|---|---|
| 99231 | Straightforward or Low | ≥25 min |
| 99232 | Moderate | ≥35 min |
| 99233 | High | ≥50 min |

**Same-day admit and discharge** (admitted and discharged on the same calendar date, stay of 8+ hours):

| Code | MDM | Time (floor) |
|---|---|---|
| 99234 | Straightforward or Low | ≥45 min |
| 99235 | Moderate | ≥70 min |
| 99236 | High | ≥85 min |

**Discharge day management** (time-based only, does not use MDM):

| Code | Time |
|---|---|
| 99238 | 30 minutes or less |
| 99239 | more than 30 minutes |

**Prolonged inpatient/observation:** add **G0316** (Medicare) or **99418** (CPT). Medicare threshold: 99223 at ≥90 min, 99233 at ≥65 min, 99236 at ≥110 min (see prolonged table).

---

## Emergency Department

**MDM only. No time-based selection. No prolonged codes.**

| Code | MDM |
|---|---|
| 99281 | N/A — may not require the presence of a physician/QHP |
| 99282 | Straightforward |
| 99283 | Low |
| 99284 | Moderate |
| 99285 | High |

In the ED the decision to hospitalize or escalate care is a common driver of High risk
(→ 99285). Note 99281 requires that an E/M service was actually provided; a patient who
leaves before being seen is not 99281.

---

## Nursing Facility

Select by MDM **or** total time. **Code 99318 was deleted for 2023** — if you see it
referenced (including in the heading of CMS MLN006764), use the subsequent nursing
facility codes 99307–99310 instead. Initial NF codes are once per admission.

**Initial** (per day):

| Code | MDM | Time (floor) |
|---|---|---|
| 99304 | Straightforward or Low | ≥25 min |
| 99305 | Moderate | ≥35 min |
| 99306 | High | ≥45 min |

**Subsequent** (per day):

| Code | MDM | Time (floor) |
|---|---|---|
| 99307 | Straightforward | ≥10 min |
| 99308 | Low | ≥15 min |
| 99309 | Moderate | ≥30 min |
| 99310 | High | ≥45 min |

**Discharge:**

| Code | Time |
|---|---|
| 99315 | 30 minutes or less |
| 99316 | more than 30 minutes |

**Prolonged NF:** add **G0317** (Medicare) or **99418** (CPT). Medicare threshold: 99306 at ≥95 min, 99310 at ≥85 min. Not allowed with discharge-day codes.

---

## Home or Residence

One merged family (2023) covering home (POS 12), assisted living (13), group home
(14), custodial care (33), and residential substance-abuse treatment (55). Select by
MDM **or** total time. **Code 99343 was deleted** from the new-patient set.

**New patient:**

| Code | MDM | Time (floor) |
|---|---|---|
| 99341 | Straightforward | ≥15 min |
| 99342 | Low | ≥30 min |
| 99344 | Moderate | ≥60 min |
| 99345 | High | ≥75 min |

**Established patient:**

| Code | MDM | Time (floor) |
|---|---|---|
| 99347 | Straightforward | ≥20 min |
| 99348 | Low | ≥30 min |
| 99349 | Moderate | ≥40 min |
| 99350 | High | ≥60 min |

**Prolonged home/residence:** add **G0318** (Medicare) or **99417** (CPT). Medicare threshold: 99345 at ≥140 min, 99350 at ≥110 min. G2211 may be added to home/residence base codes starting 1/1/2026.

---

## Prolonged service thresholds (Medicare)

Prolonged codes apply **only when the level was selected by time** and total time
exceeds the threshold below. Do not add a prolonged code to a level chosen by MDM.

| Primary service | Add-on (Medicare) | Report prolonged at |
|---|---|---|
| 99205 (O/O new, top) | G2212 | 89 min (then again at 104) |
| 99215 (O/O established, top) | G2212 | 69 min (then again at 84) |
| 99223 (initial inpatient/obs) | G0316 | ≥90 min |
| 99233 (subsequent inpatient/obs) | G0316 | ≥65 min |
| 99236 (same-day admit/discharge) | G0316 | ≥110 min |
| 99306 (initial NF) | G0317 | ≥95 min |
| 99310 (subsequent NF) | G0317 | ≥85 min |
| 99345 (home/residence new) | G0318 | ≥140 min |
| 99350 (home/residence established) | G0318 | ≥110 min |

CPT (non-Medicare) uses 99417 for office and home/residence and 99418 for the other
settings. ED visits and discharge-day codes have no prolonged add-on.

---

## Add-on codes and modifiers to flag

- **G2211 (Medicare O/O complexity add-on):** for visits that are the continuing focal point of a patient's care or ongoing care of a single serious/complex condition. Reportable with 99202–99205 and 99211–99215 (and, from 1/1/2026, home/residence base codes). Not payable with modifier 25 on the E/M except with an AWV, vaccine administration, or a Part B preventive service.
- **Modifier 25:** a significant, separately identifiable E/M provided on the same day as a procedure or other service. Flag when a note documents both an E/M and a procedure.
- **Modifier FS:** split or shared visit (physician + NPP in a facility setting). The clinician who did the substantive portion (more than half the total time, or the substantive part of MDM) bills. Office and NF visits cannot be split/shared.
- **Modifier FT:** unrelated E/M during a global surgical period / same day as critical care.

---

## Not leveled by this grid — recognize and route

- **Critical care (99291 / 99292):** time-based, not MDM-leveled. 99291 = 30–74 minutes of critical care on a date; add 99292 for each additional 30 minutes (bill 99291+99292 once cumulative time reaches 104 minutes). If the documentation describes critical illness with organ-system failure and high-complexity decision-making consuming dedicated time, say so and code critical care by time rather than forcing an office/hospital level.
- **Consultations (99242–99245 outpatient, 99252–99255 inpatient):** these CPT codes exist and are MDM/time leveled, but **Medicare does not recognize them for Part B payment.** For a Medicare patient, report the appropriate visit code for the setting instead (e.g., an office or subsequent hospital code). For a commercial payer that accepts consults, level them like the corresponding visit family. Always flag the payer question.
- **Annual wellness visit, preventive medicine, transitional care, chronic care management:** different code families, out of scope for this skill. Name the family and stop.
