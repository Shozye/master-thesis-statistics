#!/usr/bin/env python3
"""Validate directory structure against a YAML schema.

Usage:
  validate_directory_schema.py <schema.yaml>
"""

import re
import sys
from pathlib import Path

import yaml


IGNORED_DIRS = {"__pycache__"}


def validate(schema_path: Path) -> list[str]:
    schema = yaml.safe_load(schema_path.read_text())
    root = schema_path.parent / schema["root"]
    errors: list[str] = []

    if not root.is_dir():
        return [f"Root directory '{root}' does not exist"]

    allowed_root_files = set(schema.get("allowed_root_files", []))
    children_rules = schema.get("children", [])

    for entry in sorted(root.iterdir()):
        if entry.is_file():
            if entry.name not in allowed_root_files:
                errors.append(f"Unexpected file in root: {entry.relative_to(root.parent)}")
            continue
        if entry.is_dir():
            errors.extend(_match_dir(entry, children_rules, root.parent))

    return errors


def _match_dir(directory: Path, rules: list[dict], base: Path) -> list[str]:
    """Match a directory against a list of possible rules."""
    for rule in rules:
        if re.match(rule["name_pattern"], directory.name):
            return _validate_node(directory, rule, base)
    return [
        f"Directory '{directory.name}' does not match any pattern: {directory.relative_to(base)}"
    ]


def _validate_node(directory: Path, rule: dict, base: Path) -> list[str]:
    """Validate a directory node against its matched rule."""
    errors: list[str] = []
    children_rules = rule.get("children", [])
    allow_empty = rule.get("allow_empty", False)
    required_files = set(rule.get("required_files", []))
    optional_files = set(rule.get("optional_files", []))
    allow_extra = rule.get("allow_extra_files", False)

    entries = sorted(directory.iterdir())

    if not entries and allow_empty:
        return []
    if not entries and not allow_empty:
        return [f"Empty directory not allowed: {directory.relative_to(base)}"]

    # Leaf node (has required_files) — validate file contents
    if required_files:
        existing_files = {e.name for e in entries if e.is_file()}
        for req in sorted(required_files):
            if req not in existing_files:
                errors.append(f"Missing required file: {directory.relative_to(base)}/{req}")
        if not allow_extra:
            allowed_files = required_files | optional_files
            for f in sorted(existing_files - allowed_files):
                errors.append(f"Unexpected file: {directory.relative_to(base)}/{f}")
        for entry in entries:
            if entry.is_dir() and entry.name not in IGNORED_DIRS:
                errors.append(f"Unexpected subdirectory: {entry.relative_to(base)}")
        return errors

    # Branch node — recurse into children
    for entry in entries:
        if entry.is_file():
            errors.append(f"Unexpected file: {entry.relative_to(base)}")
            continue
        if entry.is_dir() and entry.name not in IGNORED_DIRS:
            errors.extend(_match_dir(entry, children_rules, base))

    return errors


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__.strip())
        sys.exit(1)

    schema_path = Path(sys.argv[1])
    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}")
        sys.exit(1)

    errors = validate(schema_path)
    if errors:
        for e in errors:
            print(f"  INVALID  {e}")
        print(f"\n{len(errors)} violation(s) found.")
        sys.exit(1)
    else:
        print("Directory structure valid.")


if __name__ == "__main__":
    main()
