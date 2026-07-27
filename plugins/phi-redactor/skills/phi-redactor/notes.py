"""
Generate synthetic clinical notes with FAKE PHI and a ground-truth list of what
should be redacted. Faker produces the fake identifiers, and we record every one
we plant, so the test harness can measure whether the redactor caught it.

Nothing here is a real patient. Everything is invented by Faker.

Run standalone to eyeball one note and its ground truth:
    uv run notes.py
"""
import random


def make_note(fake):
    """Return (note_text, planted) where planted is a list of (category, value)."""
    first = fake.first_name()
    last = fake.last_name()
    name = f"{first} {last}"
    daughter = f"{fake.first_name_female()} {last}"
    provider_last = fake.last_name()
    provider = f"Dr. {provider_last}"

    dob = fake.date_of_birth(minimum_age=30, maximum_age=95).strftime("%m/%d/%Y")
    visit = fake.date_this_year().strftime("%m/%d/%Y")
    followup = fake.date_this_year().strftime("%m/%d/%Y")

    mrn = fake.numerify("########")
    ssn = fake.ssn()
    phone = fake.phone_number()
    email = f"{first.lower()}.{last.lower()}@example.com"
    street = fake.street_address()
    city = fake.city()
    state = fake.state_abbr()
    zipc = fake.postcode()
    policy = fake.bothify("???-#######").upper()
    hospital = f"{fake.last_name()} {random.choice(['Medical Center', 'Family Clinic', 'Regional Hospital'])}"

    # Ground truth: what a correct redactor must remove. Categories are our own
    # labels for scoring, not Presidio entity names.
    planted = [
        ("NAME_full", name),
        ("NAME_narrative", last),
        ("NAME_provider", provider_last),
        ("NAME_family", daughter),
        ("DATE_dob", dob),
        ("DATE_visit", visit),
        ("DATE_followup", followup),
        ("MRN", mrn),
        ("SSN", ssn),
        ("PHONE", phone),
        ("EMAIL", email),
        ("ADDRESS_street", street),
        ("ZIP", zipc),
        ("ACCOUNT_policy", policy),
        ("LOCATION_hospital", hospital),
    ]

    text = f"""PROGRESS NOTE (SYNTHETIC TEST DOCUMENT, NO REAL PATIENT)

Patient: {name}    DOB: {dob}    MRN: {mrn}    SSN: {ssn}
Address: {street}, {city}, {state} {zipc}
Contact: {phone}    {email}    Insurance policy: {policy}
Facility: {hospital}    Visit date: {visit}

HPI: {last} is a patient seen today by {provider}, accompanied by daughter {daughter}.
The patient reports three days of productive cough. {provider} reviewed the chart,
noted the history, and adjusted therapy. Follow-up with {provider} is scheduled for {followup}.
"""
    return text, planted


def generate(n=10, seed=7):
    """Deterministic dataset of n (text, planted) pairs. Fixed seed = reproducible runs."""
    from faker import Faker

    fake = Faker("en_US")
    Faker.seed(seed)
    random.seed(seed)
    return [make_note(fake) for _ in range(n)]


if __name__ == "__main__":
    text, planted = generate(1)[0]
    print(text)
    print("PLANTED PHI (ground truth this run must remove):")
    for cat, val in planted:
        print(f"  {cat:18} {val}")
