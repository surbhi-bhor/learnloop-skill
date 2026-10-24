"""Check the skill folder and build the zip for the Claude app.

Checks that block the build:
  - SKILL.md starts with YAML frontmatter (no byte-order mark, no blank line)
  - frontmatter has name and description; description is at most 1024 chars
  - no text file starts with a UTF-8 byte-order mark
  - every references/ or scripts/ path named in SKILL.md exists

Usage (from the project root):
  python tools/package_skill.py            # private zip, includes config.local.json
  python tools/package_skill.py --public   # leaves out config.local.json
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "learnloop"
TEXT_SUFFIXES = {".md", ".py", ".json", ".yaml", ".yml", ".txt"}
SKIP_SUFFIXES = {".stackdump", ".pyc"}
MAX_DESCRIPTION = 1024


def check():
    problems = []
    for path in SKILL_DIR.rglob("*"):
        if path.is_file() and path.suffix in TEXT_SUFFIXES and path.read_bytes().startswith(b"\xef\xbb\xbf"):
            problems.append(f"{path.relative_to(ROOT)} starts with a byte-order mark; save as UTF-8 without BOM")

    text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").replace("\r\n", "\n")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        problems.append("SKILL.md must start with YAML frontmatter (---)")
        return problems
    fields = dict(re.findall(r"^(\w+):\s*(.*)$", match.group(1), re.M))
    for key in ("name", "description"):
        if not fields.get(key):
            problems.append(f"frontmatter is missing {key}")
    if len(fields.get("description", "")) > MAX_DESCRIPTION:
        problems.append(f"description is {len(fields['description'])} chars; maximum is {MAX_DESCRIPTION}")

    for ref in sorted(set(re.findall(r"(?:references|scripts)/[\w.-]+\.(?:md|py)", text))):
        if not (SKILL_DIR / ref).exists():
            problems.append(f"SKILL.md names {ref}, which does not exist")
    return problems


def build(public):
    out = ROOT / "dist" / ("learnloop-public.zip" if public else "learnloop.zip")
    out.parent.mkdir(exist_ok=True)
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(SKILL_DIR.rglob("*")):
            if (not path.is_file() or "__pycache__" in path.parts or path.suffix in SKIP_SUFFIXES
                    or (public and path.name == "config.local.json")):
                continue
            archive.write(path, path.relative_to(ROOT).as_posix())
            count += 1
    return out, count


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--public", action="store_true", help="leave out config.local.json")
    args = parser.parse_args(argv)

    problems = check()
    if problems:
        print("Not packaged:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    out, count = build(args.public)
    print(f"OK: {count} files -> {out.relative_to(ROOT)}")
    if not args.public:
        print("Includes config.local.json (your Notion IDs). Keep this zip private.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
