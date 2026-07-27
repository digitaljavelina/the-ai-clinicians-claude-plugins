"""
bootstrap.py - Install everything the redactor needs, exactly once.

Run this the first time (and only the first time):

    uv run scripts/bootstrap.py

It does the heavy, one-time work:
  1. uv has already installed the Python deps (uv run syncs before this script).
  2. Downloads the large spaCy model (en_core_web_lg) if it is missing.
  3. Downloads and caches the clinical NER model (obi/deid_roberta_i2b2).
  4. Runs one tiny redaction to prove the whole pipeline loads.
  5. Writes a .installed marker so future runs skip all of the above.

Everything lands in caches that persist across runs and even across a rebuilt
virtual environment:
  * Python wheels  -> uv's cache (~/.cache/uv)
  * spaCy model    -> installed into this project's .venv
  * clinical model -> Hugging Face hub cache (~/.cache/huggingface/hub)

So the downloads happen once. Delete .venv and re-sync and nothing re-downloads
from the network; it all comes from cache. Re-run with --force to repeat the
checks anyway.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # so `import engine` works from scripts/

MARKER = ROOT / ".installed"
SPACY_MODEL = "en_core_web_lg"
CLINICAL_MODEL = "obi/deid_roberta_i2b2"


def ensure_spacy_model() -> None:
    import spacy.util

    if spacy.util.is_package(SPACY_MODEL):
        print(f"[2/4] spaCy model {SPACY_MODEL} already present.")
        return
    print(f"[2/4] Downloading spaCy model {SPACY_MODEL} (this is large, one time)...")
    subprocess.run([sys.executable, "-m", "spacy", "download", SPACY_MODEL], check=True)


def ensure_clinical_model() -> None:
    print(f"[3/4] Loading clinical model {CLINICAL_MODEL} "
          f"(first time downloads a few hundred MB, then it is cached)...")
    import engine as E

    analyzer = E.build_analyzer("clinical")  # constructs the transformer pipeline
    return analyzer


def smoke_test(analyzer) -> None:
    import engine as E

    sample = "Patient John Smith, MRN 12345678, seen by Dr. Alvarez on 03/04/2025."
    redacted, counts = E.redact(sample, analyzer)
    print("[4/4] Smoke test - clinical engine redacted a sample line:")
    print(f"      in : {sample}")
    print(f"      out: {redacted}")
    if "John Smith" in redacted or "Alvarez" in redacted:
        raise RuntimeError("Smoke test failed: a name survived redaction.")


def main() -> int:
    force = "--force" in sys.argv[1:]
    if MARKER.exists() and not force:
        print("Already installed (.installed present). Use --force to reinstall.")
        return 0

    print("[1/4] Python dependencies installed by uv.")
    ensure_spacy_model()
    analyzer = ensure_clinical_model()
    smoke_test(analyzer)

    MARKER.write_text(
        "phi-redactor bootstrap complete.\n"
        f"spaCy model: {SPACY_MODEL}\n"
        f"clinical model: {CLINICAL_MODEL}\n",
        encoding="utf-8",
    )
    print("\nInstall complete. The downloads above will not run again.")
    print("Redact a document with:  uv run redact.py <yourfile>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
