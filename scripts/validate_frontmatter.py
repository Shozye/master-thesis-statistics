#!/usr/bin/env python3
"""Extract and validate YAML frontmatter from files.

Usage:
  validate.py extract <file>...          # Extract frontmatter as JSON (one object per line)
  validate.py validate <schema> <file>...  # Validate frontmatter against JSON Schema
"""

import json
import sys
from pathlib import Path

import jsonschema
import yaml


def extract_frontmatter(path: Path) -> dict | None:
    """Extract YAML frontmatter from a file. Supports --- and # --- delimiters."""
    text = path.read_text()

    # Markdown-style: --- at start
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4)
        return yaml.safe_load(text[4:end])

    # Comment-style: # --- delimiters (for .py and .sh)
    lines = text.splitlines()
    in_front = False
    front_lines = []
    for line in lines:
        if line == "# ---":
            if in_front:
                break
            in_front = True
            continue
        if in_front and line.startswith("# "):
            front_lines.append(line[2:])
    if front_lines:
        return yaml.safe_load("\n".join(front_lines))

    return None


def cmd_extract(files: list[Path]) -> int:
    """Extract frontmatter as JSON lines (one per file)."""
    errors = 0
    for f in files:
        fm = extract_frontmatter(f)
        if fm is None:
            print(json.dumps({"_file": str(f), "_error": "no frontmatter"}))
            errors += 1
        else:
            fm["_file"] = str(f)
            print(json.dumps(fm))
    return errors


def cmd_validate(schema_path: Path, files: list[Path]) -> int:
    """Validate frontmatter against JSON Schema."""
    schema = json.loads(schema_path.read_text())
    validator = jsonschema.Draft7Validator(schema)
    errors = 0
    for f in files:
        fm = extract_frontmatter(f)
        if fm is None:
            print(f"  MISSING  {f}")
            errors += 1
            continue
        file_errors = list(validator.iter_errors(fm))
        if file_errors:
            msgs = "\n".join(f"    - {e.message}" for e in file_errors)
            print(f"  INVALID  {f}:\n{msgs}")
            errors += 1
    if errors:
        print(f"\n{errors} file(s) failed validation.")
    else:
        print(f"All {len(files)} file(s) valid.")
    return errors


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "extract":
        files = [Path(f) for f in sys.argv[2:]]
        sys.exit(1 if cmd_extract(files) else 0)
    elif cmd == "validate":
        schema_path = Path(sys.argv[2]).resolve()
        files = [Path(f) for f in sys.argv[3:]]
        sys.exit(1 if cmd_validate(schema_path, files) else 0)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
