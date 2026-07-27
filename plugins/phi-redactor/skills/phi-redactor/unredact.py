"""
unredact.py - Put the original values back after reversible redaction.

Use this at the end of the round trip:
  1. uv run redact.py note.txt --reversible   -> note.redacted.txt + note.redacted.map.json
  2. send ONLY note.redacted.txt to your AI / algorithm, keep the .map.json local
  3. save what the AI returns, then:
        uv run unredact.py ai_output.txt --map outputs/note.redacted.map.json

It replaces every placeholder like [[NAME_1]] with its original value from the key
file, and runs a round-trip check so a broken restoration is loud, not silent:
  * placeholders that are in the key but MISSING from the AI's output (it dropped
    or reworded them, so they cannot be restored), and
  * placeholder-shaped tokens in the output that are NOT in the key (the AI
    invented or altered one).

This tool needs no models and no network; it is plain text substitution. The key
file and the restored output both contain PHI, so they stay on your machine.
"""
import argparse
import json
import re
import sys
from pathlib import Path

# Read and write UTF-8 no matter the console default (Windows uses a legacy code
# page by default, which would mangle non-ASCII text).
for _stream in (sys.stdin, sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

TOKEN = re.compile(r"\[\[[A-Za-z0-9_]+\]\]")


def load_mapping(map_path: Path) -> dict:
    data = json.loads(map_path.read_text(encoding="utf-8"))
    mapping = data.get("mapping", data) if isinstance(data, dict) else None
    if not isinstance(mapping, dict) or not mapping:
        raise SystemExit(f"{map_path} has no usable 'mapping'. Was it made by redact.py --reversible?")
    return mapping


def restore(text: str, mapping: dict) -> str:
    # Longest placeholders first so [[NAME_1]] can never be replaced inside a
    # longer token before the longer one is handled.
    for placeholder in sorted(mapping, key=len, reverse=True):
        text = text.replace(placeholder, mapping[placeholder])
    return text


def round_trip_check(text: str, mapping: dict) -> tuple[list[str], list[str]]:
    present = set(TOKEN.findall(text))
    expected = set(mapping)
    missing = sorted(expected - present)   # in key, gone from AI output
    unknown = sorted(present - expected)   # in AI output, not in key
    return missing, unknown


def main() -> int:
    ap = argparse.ArgumentParser(description="Restore reversibly-redacted text using its key file.")
    ap.add_argument("input", help="the AI's output text file, or '-' for stdin")
    ap.add_argument("--map", required=True, help="the .map.json key written by redact.py --reversible")
    ap.add_argument("-o", "--output", help="restored output file (default: <input>.restored.txt)")
    args = ap.parse_args()

    mapping = load_mapping(Path(args.map))

    if args.input == "-":
        text = sys.stdin.read()
    else:
        text = Path(args.input).read_text(encoding="utf-8", errors="replace")

    missing, unknown = round_trip_check(text, mapping)
    restored = restore(text, mapping)

    if args.input == "-":
        sys.stdout.write(restored)
    else:
        dest = Path(args.output) if args.output else Path(args.input).with_suffix(".restored.txt")
        dest.write_text(restored, encoding="utf-8")
        print(f"Restored -> {dest}")

    restored_count = len(mapping) - len(missing)
    print(f"{restored_count}/{len(mapping)} placeholders restored.", file=sys.stderr)
    if missing:
        print(f"WARNING: {len(missing)} placeholder(s) in the key never came back from the AI, "
              f"so their original values are NOT in the output: {', '.join(missing)}", file=sys.stderr)
    if unknown:
        print(f"WARNING: {len(unknown)} token(s) in the AI output are not in the key "
              f"(invented or altered): {', '.join(unknown)}", file=sys.stderr)
    return 1 if (missing or unknown) else 0


if __name__ == "__main__":
    raise SystemExit(main())
