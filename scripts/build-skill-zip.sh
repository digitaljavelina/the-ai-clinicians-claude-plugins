#!/usr/bin/env bash
# Package a skill for upload to Claude Desktop (Settings -> Capabilities -> Skills).
#
#   ./scripts/build-skill-zip.sh pubmed-search    # one skill
#   ./scripts/build-skill-zip.sh --all            # every skill in plugins/
#
# Zips land in dist/ (gitignored). Validates against Claude Desktop's upload
# rules first, so a bad description fails here instead of in the browser.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$REPO/dist"

die() { printf '\033[31merror:\033[0m %s\n' "$1" >&2; exit 1; }

# Reads SKILL.md and enforces the frontmatter rules Desktop enforces on upload.
validate() {
  python3 - "$1" <<'PY'
import re, sys, pathlib

DESC_MAX, NAME_MAX = 1024, 64

p = pathlib.Path(sys.argv[1])
text = p.read_text(encoding="utf-8")
m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
if not m:
    sys.exit(f"{p}: no YAML frontmatter (the file must open with a --- fence)")

try:
    import yaml
    fm = yaml.safe_load(m.group(1)) or {}
except ImportError:
    # Good enough for the flat single-line keys these skills use.
    fm = {}
    for line in m.group(1).split("\n"):
        k, sep, v = line.partition(":")
        if sep and not k.startswith((" ", "\t", "#")):
            fm[k.strip()] = v.strip().strip("'\"")

name, desc = fm.get("name"), fm.get("description")
if not name:
    sys.exit(f"{p}: frontmatter is missing 'name'")
if not desc:
    sys.exit(f"{p}: frontmatter is missing 'description'")
if len(name) > NAME_MAX:
    sys.exit(f"{p}: name is {len(name)} chars, max {NAME_MAX}")
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
    sys.exit(f"{p}: name '{name}' must be lowercase letters, digits, and single hyphens")
if name != p.parent.name:
    sys.exit(f"{p}: name '{name}' does not match its folder '{p.parent.name}'")
if len(desc) > DESC_MAX:
    sys.exit(f"{p}: description is {len(desc)} chars, max {DESC_MAX} — trim {len(desc) - DESC_MAX}")

print(f"  name         {name}")
print(f"  description  {len(desc)}/{DESC_MAX} chars")
PY
}

build() {
  local name="$1"
  local src="$REPO/plugins/$name/skills/$name"
  [[ -d "$src" ]] || die "no skill at plugins/$name/skills/$name"
  [[ -f "$src/SKILL.md" ]] || die "plugins/$name/skills/$name has no SKILL.md"

  printf '\033[1m%s\033[0m\n' "$name"
  validate "$src/SKILL.md"

  local out="$DIST/$name.zip"
  mkdir -p "$DIST"
  rm -f "$out"

  # Stage a copy so the archive root is the skill folder itself, which is the
  # layout Desktop expects, and so pruning junk never touches the working tree.
  local stage
  stage="$(mktemp -d)"
  cp -R "$src" "$stage/$name"
  find "$stage/$name" \
    \( -name '.DS_Store' -o -name '*.pyc' -o -name '__pycache__' \
       -o -name '.venv' -o -name '.pytest_cache' -o -name '.ruff_cache' \) \
    -exec rm -rf {} + 2>/dev/null || true

  ( cd "$stage" && zip -rq "$out" "$name" -x '.*' )
  rm -rf "$stage"

  printf '  \033[32mwrote\033[0m       %s (%s)\n\n' "${out#"$REPO"/}" "$(du -h "$out" | cut -f1)"
}

case "${1:-}" in
  --all)
    for d in "$REPO"/plugins/*/; do build "$(basename "$d")"; done
    ;;
  "" | -h | --help)
    sed -n '2,8p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    printf '\nAvailable skills:\n'
    for d in "$REPO"/plugins/*/; do printf '  %s\n' "$(basename "$d")"; done
    ;;
  *)
    build "$1"
    ;;
esac
