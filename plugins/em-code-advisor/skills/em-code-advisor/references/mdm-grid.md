# MDM Grid (2021/2023 CPT E/M)

The engine for every level decision that is not made on time alone. Read this file
whenever you score medical decision making. Do not reproduce a level or a category
from memory; the categories are easy to misremember and a wrong category silently
changes the code.

The level of MDM is chosen by **meeting or exceeding 2 of the 3 elements**:

1. Number and Complexity of Problems Addressed (COPA)
2. Amount and/or Complexity of Data Reviewed and Analyzed
3. Risk of Complications and/or Morbidity or Mortality of Patient Management

Four levels exist: **straightforward, low, moderate, high.** History and physical exam
are *not* elements of level selection. They must be medically appropriate, but their
length never raises or lowers the level.

`CPT © American Medical Association.` These tables summarize the AMA 2023 E/M
guidelines for educational use. Confirm against a current CPT codebook and your
payer's rules before billing.

---

## Element 1 — Number and Complexity of Problems Addressed (COPA)

The problem status is measured **on the date of the encounter**, by the problem the
clinician actually addressed (evaluated or managed), not every problem on the list.

| MDM level | COPA | What qualifies |
|---|---|---|
| Straightforward | **Minimal** | 1 self-limited or minor problem |
| Low | **Low** | 2+ self-limited or minor problems; **or** 1 stable chronic illness; **or** 1 acute, uncomplicated illness or injury; **or** 1 stable acute illness; **or** 1 acute, uncomplicated illness or injury requiring hospital inpatient or observation level of care |
| Moderate | **Moderate** | 1+ chronic illness with exacerbation, progression, or side effects of treatment; **or** 2+ stable chronic illnesses; **or** 1 undiagnosed new problem with uncertain prognosis; **or** 1 acute illness with systemic symptoms; **or** 1 acute complicated injury |
| High | **High** | 1+ chronic illness with severe exacerbation, progression, or side effects of treatment; **or** 1 acute or chronic illness or injury that poses a threat to life or bodily function |

### Problem definitions (apply these, they are where coders go wrong)

- **Self-limited or minor problem:** runs a definite and prescribed course, transient, not likely to permanently alter health status.
- **Stable chronic illness:** expected to last at least a year or until death. "Stable" means the patient is **at their treatment goal**, not merely unchanged. A patient whose A1c is 9% is not "stable" even if it is the same 9% as last visit, because they are not at goal.
- **Acute, uncomplicated illness or injury:** recent or new, low risk of morbidity, full recovery expected (e.g., cystitis, simple sprain).
- **Chronic illness with exacerbation/progression/side effects:** worse, poorly controlled, or progressing, requiring additional care.
- **Undiagnosed new problem with uncertain prognosis:** a new problem whose workup could reveal something serious (e.g., a new breast lump).
- **Acute illness with systemic symptoms:** an illness causing systemic symptoms with a risk of morbidity (e.g., pyelonephritis, pneumonia). A systemic *general* symptom of a minor illness (fever with a cold) does not count.
- **Acute complicated injury:** requires evaluation of body systems beyond the injured organ, is extensive, or the treatment options carry risk.
- **Threat to life or bodily function:** an acute or chronic problem that, untreated, poses a near-term threat (e.g., acute MI, PE, respiratory failure, a severe exacerbation with possible escalation).

---

## Element 2 — Amount and/or Complexity of Data

Each unique test, order, or document counts once. A panel ordered as one test counts
once. Ordering a test and then reviewing that same test's result is one point, not two.
"Unique source" means a distinct physician, QHP, facility, or provider group.

| MDM level | Data | Requirement |
|---|---|---|
| Straightforward | **Minimal or none** | No data, or a trivial amount |
| Low | **Limited** | Meet **at least 1 of 2** categories below |
| Moderate | **Moderate** | Meet **at least 1 of 3** categories below |
| High | **Extensive** | Meet **at least 2 of 3** categories below |

**Category 1 — Tests, documents, or independent historian.** Any combination of the following:
- Review of prior external note(s) from each unique source
- Review of the result(s) of each unique test
- Ordering of each unique test
- Assessment requiring an independent historian

Count needed: **Limited (Low)** = any combination of **2**. **Moderate/Extensive** = any combination of **3**.
(For Low, Category 1 is "tests and documents" only; the independent historian sits in its own Category 2 at the Low level.)

**Category 2 — Independent interpretation of tests.** Independent interpretation of a test performed by another physician/QHP, not separately reported (i.e., you are not billing the interpretation yourself).

**Category 3 — Discussion of management or test interpretation.** Direct discussion (not through the chart) with an external physician/QHP/appropriate source, not separately reported.

At the **Low** level only, the two categories are: Category 1 (any 2 tests/documents) **or** Category 2 (assessment requiring an independent historian). Independent interpretation and external discussion do not apply until Moderate.

---

## Element 3 — Risk of Complications and/or Morbidity or Mortality

Risk is judged from the problem(s) addressed and the management selected, at the time
of the encounter, when appropriately treated. It is a clinical-judgment element, so
use the examples as anchors, not an exhaustive list.

| MDM level | Risk | Anchoring examples |
|---|---|---|
| Straightforward | **Minimal** | Minimal risk of morbidity from additional diagnostic testing or treatment |
| Low | **Low** | Low risk of morbidity; over-the-counter management, rest, minor care |
| Moderate | **Moderate** | **Prescription drug management**; decision regarding minor surgery with identified patient/procedure risk factors; decision regarding elective major surgery without identified risk factors; **diagnosis or treatment significantly limited by social determinants of health** |
| High | **High** | **Drug therapy requiring intensive monitoring for toxicity**; decision regarding elective major surgery with identified risk factors; decision regarding emergency major surgery; **decision regarding hospitalization or escalation of hospital-level care**; decision not to resuscitate or to de-escalate care because of poor prognosis; parenteral controlled substances |

### High-yield risk facts

- **Prescription drug management is Moderate risk.** Starting, stopping, adjusting, or continuing a prescription medication (with documented management) lands the risk element at Moderate. This single fact carries a large share of real 99214 / moderate visits. It requires actual management, not just a med list on the chart.
- **The decision to hospitalize or escalate care is High risk.** In the ED and inpatient settings this is often what separates moderate from high. The decision itself counts, even if the outcome is admission by someone else.
- **"Drug therapy requiring intensive monitoring for toxicity"** means monitoring for a serious adverse effect of the *drug* (e.g., a therapeutic drug level or a lab drawn to watch for toxicity), not routine efficacy monitoring.
- Social determinants of health that significantly limit diagnosis or treatment raise the risk element to Moderate.

---

## Putting it together

1. Score each of the three elements independently against its table above.
2. The MDM level is the one where **at least 2 of the 3 elements** meet or exceed that level.
3. Worked example: 2 stable chronic illnesses (COPA = Moderate) + ordering a CBC and a BMP and reviewing an outside note, 3 items (Data = Moderate) + prescription drug management (Risk = Moderate) = **Moderate MDM**, all three elements aligned.
4. Worked example: 1 stable chronic illness (COPA = Low) + no data reviewed (Data = Minimal) + prescription drug management (Risk = Moderate) = **Low MDM**, because only 1 element reached Moderate and 2 of 3 sit at Low.

The 2-of-3 rule is why the risk element alone (e.g., a single refilled prescription)
does not by itself make a visit moderate. It needs a second element to agree.
