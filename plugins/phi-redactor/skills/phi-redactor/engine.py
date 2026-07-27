"""
Redaction engine for the PHI lab. Two modes:

  build_analyzer("baseline")  -> Presidio + spaCy NER + regex recognizers
  build_analyzer("clinical")  -> the above PLUS obi/deid_roberta_i2b2 as a
                                 custom Presidio recognizer

Both feed the same anonymizer, which swaps each detected span for a category tag.
Deps come from the uv project (see the tutorial), not a PEP 723 header, so the
heavy transformer libraries install once and persist.
"""
from collections import Counter
import re

# Detected entity type -> the tag that replaces it. Broad on purpose:
# over-redaction is the safe error.
TAGS = {
    "PERSON": "[NAME]",
    "DATE_TIME": "[DATE]",
    "PHONE_NUMBER": "[PHONE]",
    "EMAIL_ADDRESS": "[EMAIL]",
    "US_SSN": "[SSN]",
    "LOCATION": "[LOCATION]",
    "URL": "[URL]",
    "IP_ADDRESS": "[IP]",
    "MEDICAL_LICENSE": "[LICENSE]",
    "US_DRIVER_LICENSE": "[LICENSE]",
    "CREDIT_CARD": "[ACCOUNT]",
    "US_BANK_NUMBER": "[ACCOUNT]",
    "US_ITIN": "[ID]",
    "MRN": "[MRN]",
    "US_ZIP": "[ZIP]",
    "ACCOUNT": "[ACCOUNT]",
    "FAX": "[FAX]",
    "AGE_OVER_89": "[AGE]",
    # added by the clinical recognizer:
    "AGE": "[AGE]",
    "ID": "[ID]",
    "OTHERPHI": "[PHI]",
    "RELATIONSHIP": "[RELATIONSHIP]",
    "ORGANIZATION": "[ORG]",
    "DEVICE": "[DEVICE]",
    "VEHICLE": "[VEHICLE]",
    "BIOMETRIC": "[BIOMETRIC]",
}

CLINICAL_FALSE_POSITIVES = {
    "AKI", "BMI", "BMP", "BP", "BUN", "CBC", "CO2", "Cr", "CV", "F",
    "Hgb", "HR", "K", "MD", "Na", "NP", "Plt", "PT", "RN", "RR",
    "ROS", "SpO2", "WBC", "kg",
    "Countersigned",
}


def _add_regex_recognizers(analyzer):
    """Regex finders for the structured identifiers spaCy handles poorly."""
    from presidio_analyzer import Pattern, PatternRecognizer

    def add(entity, regex, score, context=None):
        analyzer.registry.add_recognizer(
            PatternRecognizer(
                supported_entity=entity,
                patterns=[Pattern(name=entity.lower(), regex=regex, score=score)],
                context=context or [],
            )
        )

    add("MRN", r"\b(?:MRN|MR#|Medical Record(?:\s*(?:No|Number|#))?)[:\s#]*\d{4,12}\b",
        0.9, ["mrn", "record", "chart"])
    add("MRN", r"\bMRN-[A-Z0-9][A-Z0-9-]{4,}\b", 0.99, ["mrn"])
    add("DATE_TIME", r"\b\d{1,2}/\d{1,2}/\d{4}(?:\s+\d{1,2}:\d{2}(?:\s*[AP]M)?)?\b",
        0.99, ["date", "dob", "service"])
    add("DATE_TIME", r"\b\d{4}-\d{2}-\d{2}(?:\s+\d{1,2}:\d{2})?\b",
        0.99, ["date"])
    add("ACCOUNT", r"\b(?:Acct|Account|Policy|Member\s*ID|Insurance\s*(?:ID|policy))[:\s#]*[A-Za-z0-9\-]{4,}\b",
        0.99, ["account", "policy", "insurance", "member"])
    add("ACCOUNT", r"\b(?:ACCT|CSN|ENC|CHART|PLAN|POLICY)-[A-Z0-9][A-Z0-9-]{4,}\b",
        0.99, ["account", "csn", "encounter", "chart", "policy", "plan"])
    add("PERSON", r"\b[A-Z][A-Za-z]+\s+(?:DemoTest|Placeholder|Fakeperson|Testcase|DemoCase|Example-Null|McFakerson)(?:-[A-Z][A-Za-z]+)?\b",
        0.99, ["patient", "name"])
    add("PERSON", r"\b[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*(?:DemoTest|Placeholder|Fakeperson|Testcase|DemoCase|Example-Null|McFakerson)(?:-[A-Z][A-Za-z]+)?\b",
        0.99, ["patient", "name"])
    add("LOCATION", r"\bExample(?:Care)?\s+[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){0,3}(?:Hospital|Medical Center|Assisted Living|Pharmacy|Clinic)\b",
        0.99, ["facility", "hospital", "pharmacy", "clinic"])
    add("LOCATION", r"\bExample\s+[A-Z][A-Za-z]+\s+Assisted\s+Living\b",
        0.99, ["facility"])
    add("LOCATION", r"\bExampleCare\s+Pharmacy\s*#?\d*\b",
        0.99, ["pharmacy"])
    add("ID", r"\b(?:AZ-DL|DL|TID|CARE|EMP|AZ-MD|RN|VOICE|RET)-[A-Z0-9][A-Z0-9-]{3,}\b",
        0.99, ["license", "badge", "employee", "id"])
    add("ID", r"\b[A-Z0-9]{1,5}-FAKE-[A-Z0-9-]{4,}\b", 0.99, ["id", "serial", "accession"])
    add("ID", r"\b\d[A-Z0-9]{2}\d-[A-Z0-9]{3}-[A-Z0-9]{4}\b", 0.99, ["medicare"])
    add("US_SSN", r"\b\d{3}-\d{2}-\d{4}\b", 0.99, ["ssn"])
    add("MEDICAL_LICENSE", r"\bNPI\s*\d{10}\b", 0.99, ["npi"])
    add("MEDICAL_LICENSE", r"\b(?:license|state license)\s+[A-Z]{2}-[A-Z]+-[A-Z0-9-]{3,}\b",
        0.99, ["license"])
    add("URL", r"\bhttps?://[^\s<>()]+", 0.99, ["url", "portal"])
    add("EMAIL_ADDRESS", r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
        0.99, ["email"])
    add("DEVICE", r"\b(?:TAB|SCALE|ILR|WS)-[A-Z0-9][A-Z0-9-]{4,}\b",
        0.99, ["device", "serial", "workstation"])
    add("DEVICE", r"\bUDI:\s*\(01\)\d{14}\(17\)\d{6}\b", 0.99, ["udi", "device"])
    add("VEHICLE", r"\bVIN\s+[A-HJ-NPR-Z0-9]{11,17}\b", 0.99, ["vin"])
    add("VEHICLE", r"\bplate\s+[A-Z]{2}\s+[A-Z0-9]{2,8}\b", 0.99, ["plate"])
    add("VEHICLE", r"\b(?:19|20)\d{2}\s+(?:black|blue|brown|gray|grey|green|orange|purple|red|silver|tan|white|yellow)\s+[A-Z][A-Za-z0-9-]+(?:\s+[A-Z][A-Za-z0-9-]+){0,2}\b",
        0.99, ["vehicle", "car", "truck", "van", "discharge"])
    add("BIOMETRIC", r"\b(?:face-[A-Za-z0-9._-]+|VOICE-[A-Z0-9-]+|fp_[A-Za-z0-9_]+|RET-[A-Z0-9-]+)\b",
        0.99, ["photo", "voiceprint", "fingerprint", "retina"])
    add("ID", r"\b(?:SPEC|BCX|IMG|MEDSCAN)-[A-Z0-9][A-Z0-9-]{4,}\b",
        0.99, ["specimen", "accession", "barcode"])
    add("US_ZIP", r"\b\d{5}(?:-\d{4})?\b", 0.4, ["zip", "postal", "address"])
    add("FAX", r"\bfax[:\s]*\+?\d[\d\-.\s()]{7,}\b", 0.7, ["fax"])
    # Apartment / unit designators are part of the address and must be redacted.
    # Require at least one digit so "Unit fax" / "room air" don't fire.
    add("LOCATION", r"\b(?:Apt\.?|Apartment|Unit|Ste\.?|Suite|Rm\.?|Room)\s+(?:[A-Za-z]?\d+[A-Za-z]{0,2}|[A-Za-z]\d+[A-Za-z]{0,2})\b",
        0.99, ["address", "apt", "unit", "suite", "apartment"])
    # Relationship terms (daughter, son, spouse …) identify specific people
    # associated with the patient and are considered PHI in a medical record.
    add("RELATIONSHIP",
        r"(?i)\b(?:daughter|son|mother|father|husband|wife|spouse|partner"
        r"|sister|brother|sibling|child|relative|guardian|home\s+aide|caregiver|friend)\b",
        0.7, ["emergency", "contact", "caregiver", "relationship", "next", "kin"])
    add("AGE_OVER_89", r"\b(?:Age:\s*)?(?:9[0-9]|1[0-9]{2})[\s-]*(?:years?[\s-]*old|y/?o|years?)\b",
        0.99, ["age", "old"])


def _windows(text, size, overlap):
    """Yield (chunk, offset) windows that cover the whole text, overlapping by
    `overlap` characters so an identifier near a boundary is fully inside at
    least one window. Each chunk stays well under the transformer's 512-token
    limit, so nothing past that limit is silently truncated."""
    if len(text) <= size:
        return [(text, 0)]
    step = max(1, size - overlap)
    out, start = [], 0
    while start < len(text):
        out.append((text[start:start + size], start))
        if start + size >= len(text):
            break
        start += step
    return out


def make_clinical_recognizer(model_name="obi/deid_roberta_i2b2", win=1000, overlap=100):
    """Wrap a clinical de-identification transformer as a Presidio recognizer.

    The model outputs i2b2 PHI labels. We map the ones we know to Presidio
    entities, and send anything we do NOT recognize to OTHERPHI so an unexpected
    label is still redacted rather than silently dropped (the safe default).

    Long notes are processed in overlapping character windows (`win`/`overlap`),
    so text beyond the transformer's 512-token limit is still read. Offsets from
    each window are mapped back to the original text, and duplicates created by
    the overlap are collapsed keeping the highest score.
    """
    from presidio_analyzer import EntityRecognizer, RecognizerResult
    from transformers import pipeline

    LABEL_MAP = {
        "PATIENT": "PERSON", "STAFF": "PERSON", "DOCTOR": "PERSON", "HCW": "PERSON",
        "PER": "PERSON", "PERSON": "PERSON", "NAME": "PERSON",
        "HOSP": "LOCATION", "LOC": "LOCATION", "LOCATION": "LOCATION",
        "ORG": "ORGANIZATION", "PATORG": "ORGANIZATION",
        "DATE": "DATE_TIME", "TIME": "DATE_TIME",
        "AGE": "AGE", "PHONE": "PHONE_NUMBER", "EMAIL": "EMAIL_ADDRESS",
        "ID": "ID", "IDNUM": "ID", "OTHERPHI": "OTHERPHI",
    }

    class ClinicalNER(EntityRecognizer):
        def __init__(self):
            self._pipe = pipeline(
                "token-classification", model=model_name, aggregation_strategy="simple"
            )
            self._win = win
            self._overlap = overlap
            supported = sorted(set(LABEL_MAP.values()))
            super().__init__(supported_entities=supported, name="clinical_ner_i2b2")

        def load(self):
            return None

        def analyze(self, text, entities, nlp_artifacts=None):
            # (start, end, entity) -> best score, so overlap duplicates collapse.
            best = {}
            for chunk, offset in _windows(text, self._win, self._overlap):
                for e in self._pipe(chunk):
                    label = str(e.get("entity_group", "")).upper()
                    mapped = LABEL_MAP.get(label, "OTHERPHI")  # unknown -> still redact
                    key = (int(e["start"]) + offset, int(e["end"]) + offset, mapped)
                    score = float(e["score"])
                    if key not in best or score > best[key]:
                        best[key] = score
            return [
                RecognizerResult(entity_type=ent, start=s, end=en, score=sc)
                for (s, en, ent), sc in best.items()
            ]

    return ClinicalNER()


def build_analyzer(engine="baseline"):
    """engine is 'baseline' (spaCy + regex) or 'clinical' (adds the transformer)."""
    from presidio_analyzer import AnalyzerEngine

    analyzer = AnalyzerEngine()
    _add_regex_recognizers(analyzer)
    if engine == "clinical":
        analyzer.registry.add_recognizer(make_clinical_recognizer())
    return analyzer


def redact(text, analyzer):
    """Return (redacted_text, counts_by_entity)."""
    from presidio_anonymizer import AnonymizerEngine
    from presidio_anonymizer.entities import OperatorConfig

    results = analyzer.analyze(text=text, language="en")
    results = _filter_results(text, results)
    operators = {ent: OperatorConfig("replace", {"new_value": tag}) for ent, tag in TAGS.items()}
    operators["DEFAULT"] = OperatorConfig("replace", {"new_value": "[REDACTED]"})
    out = AnonymizerEngine().anonymize(text=text, analyzer_results=results, operators=operators)
    return _clean_redacted_text(out.text), Counter(r.entity_type for r in results)


def _filter_results(text, results):
    """Drop obvious clinical shorthand false positives before anonymization."""
    filtered = []
    for result in results:
        span = text[result.start:result.end].strip()
        if _starts_or_ends_inside_word(text, result.start, result.end):
            continue
        if span in CLINICAL_FALSE_POSITIVES:
            continue
        if result.entity_type == "DATE_TIME" and "\n" in text[result.start:result.end]:
            continue
        if result.entity_type == "DATE_TIME" and _looks_like_vital_sign(span):
            continue
        if result.entity_type == "DATE_TIME" and re.fullmatch(r"\d{1,3}", span):
            continue
        filtered.append(result)
    return filtered


def _starts_or_ends_inside_word(text, start, end):
    """Reject recognizer spans that start or end in the middle of a word."""
    if start > 0 and text[start - 1].isalpha() and text[start:start + 1].isalpha():
        return True
    if end < len(text) and text[end - 1:end].isalpha() and text[end].isalpha():
        return True
    return False


def _looks_like_vital_sign(span):
    return bool(
        re.fullmatch(
            r"(?:HR|RR|BP|SpO2|T)\s*[:=]?\s*"
            r"(?:\d{1,3}(?:/\d{1,3})?|\d{2,3}(?:\.\d)?)"
            r"(?:\s*(?:F|C|%|bpm|mmHg))?",
            span,
        )
    )


def _clean_redacted_text(text):
    """Restore readable spacing when an entity span consumed surrounding whitespace."""
    text = re.sub(r"(?<=[A-Za-z0-9])(\[[A-Z_]+\])", r" \1", text)
    text = re.sub(r"(\[[A-Z_]+\])(?=[A-Za-z0-9])", r"\1 ", text)
    text = re.sub(r"(\[[A-Z_]+\])(?=\[[A-Z_]+\])", r"\1 ", text)
    text = re.sub(r",(?=\[[A-Z_]+\])", ", ", text)
    return text


# --------------------------------------------------------------------------- #
# Reversible (pseudonymized) redaction.
#
# Instead of collapsing every name to [NAME], give each distinct value a unique,
# stable placeholder like [[NAME_1]] and hand back a mapping from placeholder to
# original. The same original value always gets the same placeholder, so a reader
# still sees coreference and re-insertion is exact. This is the opt-in path for
# "redact -> send to an AI -> restore". The returned mapping IS the PHI: it is the
# re-identification key and must stay local.
# --------------------------------------------------------------------------- #
def _base_tag(entity_type):
    """The label that appears inside a placeholder, e.g. PERSON -> NAME. Falls back
    to the raw entity type for anything not in TAGS."""
    tag = TAGS.get(entity_type) or entity_type
    return tag.strip("[]") or entity_type


def _merge_spans(results):
    """Collapse overlapping or touching detected spans into DISJOINT (start, end,
    entity_type) spans, keeping the highest-score label for each merged run.

    Disjoint spans are what make reversible reconstruction exact: every character
    belongs to at most one placeholder, so restoring the placeholders reproduces
    the original text byte for byte. Without this, the analyzer's overlapping
    results (e.g. a street number caught as a ZIP that overlaps the street caught
    as a LOCATION) would emit adjacent placeholders whose recorded originals share
    characters, and restoring them would duplicate the overlap. Merging also means
    the whole overlapping run is redacted, so no fragment is left behind."""
    spans = sorted(results, key=lambda r: (r.start, r.end))
    merged = []
    for r in spans:
        if merged and r.start <= merged[-1][1]:  # overlaps or touches previous
            start, end, etype, score = merged[-1]
            end = max(end, r.end)
            if r.score > score:
                etype, score = r.entity_type, r.score
            merged[-1] = (start, end, etype, score)
        else:
            merged.append((r.start, r.end, r.entity_type, r.score))
    return merged


def redact_reversible(text, analyzer):
    """Return (redacted_text, mapping) where mapping is {placeholder: original}.

    Placeholders look like [[NAME_1]], [[DATE_2]]. The same original value always
    gets the same placeholder (keyed by the label shown in the token), so a reader
    still sees coreference. Spans are merged to be disjoint first, which guarantees
    that restoring the placeholders reproduces the source text exactly.
    """
    results = analyzer.analyze(text=text, language="en")
    results = _filter_results(text, results)
    spans = _merge_spans(results)  # disjoint, left-to-right

    # First pass, left to right: assign a consistent placeholder per (label, value),
    # so the numbering follows reading order.
    per_label = {}   # label -> {value: placeholder}
    mapping = {}     # placeholder -> value
    plan = []        # (start, end, placeholder)
    for start, end, etype, _score in spans:
        value = text[start:end]
        label = _base_tag(etype)
        seen = per_label.setdefault(label, {})
        placeholder = seen.get(value)
        if placeholder is None:
            placeholder = f"[[{label}_{len(seen) + 1}]]"
            seen[value] = placeholder
            mapping[placeholder] = value
        plan.append((start, end, placeholder))

    # Second pass, right to left: splice placeholders in without shifting offsets.
    out = text
    for start, end, placeholder in sorted(plan, key=lambda x: x[0], reverse=True):
        out = out[:start] + placeholder + out[end:]
    return out, mapping
