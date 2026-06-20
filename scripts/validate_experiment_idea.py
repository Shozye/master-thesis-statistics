"""Validate that every experiment directory contains experiment-idea.md with required headers."""

import json
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema" / "experiment_idea_schema.json"
REQUIRED_HEADERS = json.loads(SCHEMA_PATH.read_text())["properties"]["headers"]["const"]


def validate(experiments_root: Path) -> list[str]:
    errors: list[str] = []
    experiment_dirs = sorted(
        d for d in experiments_root.rglob("*") if d.is_dir() and (d / "experiment.py").exists()
    )
    for exp_dir in experiment_dirs:
        idea_file = exp_dir / "experiment-idea.md"
        rel = idea_file.relative_to(experiments_root)
        if not idea_file.exists():
            errors.append(f"{rel}: file missing")
            continue
        content = idea_file.read_text()
        for header in REQUIRED_HEADERS:
            if header not in content:
                errors.append(f"{rel}: missing header '{header}'")
    return errors


def main() -> None:
    root = Path(__file__).resolve().parent.parent / "experiments"
    errors = validate(root)
    if errors:
        print(f"experiment-idea.md validation failed ({len(errors)} error(s)):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        sys.exit(1)
    print("✓ All experiment-idea.md files valid")


if __name__ == "__main__":
    main()
