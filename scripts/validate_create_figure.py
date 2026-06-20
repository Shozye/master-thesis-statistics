#!/usr/bin/env python3
"""Validate create_figure.py files.

Rules:
  1. Must have `out = GeneratedOutputManager(__file__)`.
  2. Must have `from data_for_figure_dataclass import DataModel`.
  3. Must use `load_dataclass(DataModel)`.
  4. Must NOT have `match DRAFT:` (no quality parameters).
  5. Must have get_caption and get_test_caption functions.
  6. Must have `if __name__ == "__main__":` calling `main()`.

Usage:
  validate_create_figure.py <file>...
"""

import ast
import signal
import sys
from pathlib import Path


def check_ast(path: Path) -> list[str]:
    try:
        tree = ast.parse(path.read_text(), filename=str(path))
    except SyntaxError as e:
        return [f"SyntaxError: {e}"]

    errors = []

    # Rule 1: GeneratedOutputManager(__file__)
    gom_found = any(
        isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "out"
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        and node.value.func.id == "GeneratedOutputManager"
        and len(node.value.args) == 1
        and isinstance(node.value.args[0], ast.Name)
        and node.value.args[0].id == "__file__"
        for node in ast.walk(tree)
    )
    if not gom_found:
        errors.append("Must have `out = GeneratedOutputManager(__file__)`.")

    # Rule 2: from data_for_figure_dataclass import DataModel
    has_datamodel_import = any(
        isinstance(node, ast.ImportFrom)
        and node.module == "data_for_figure_dataclass"
        and any(alias.name == "DataModel" for alias in node.names)
        for node in ast.walk(tree)
    )
    if not has_datamodel_import:
        errors.append("Must have `from data_for_figure_dataclass import DataModel`.")

    # Rule 3: load_dataclass(DataModel)
    has_load = any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "load_dataclass"
        and any(isinstance(a, ast.Name) and a.id == "DataModel" for a in node.args)
        for node in ast.walk(tree)
    )
    if not has_load:
        errors.append("Must use `load_dataclass(DataModel)`.")

    # Rule 4: No match DRAFT
    has_match_draft = any(
        isinstance(node, ast.Match)
        and isinstance(node.subject, ast.Name)
        and node.subject.id == "DRAFT"
        for node in ast.walk(tree)
    )
    if has_match_draft:
        errors.append("create_figure.py must NOT contain `match DRAFT:` (no quality parameters).")

    # Rule 5: get_caption / get_test_caption
    top_funcs = {n.name for n in ast.iter_child_nodes(tree) if isinstance(n, ast.FunctionDef)}
    for req in ("get_caption", "get_test_caption"):
        if req not in top_funcs:
            errors.append(f"Missing required function `{req}()`.")

    # Rule 6: if __name__ == "__main__" with main()
    name_main_block = None
    for n in ast.iter_child_nodes(tree):
        if (
            isinstance(n, ast.If)
            and isinstance(n.test, ast.Compare)
            and isinstance(n.test.left, ast.Name)
            and n.test.left.id == "__name__"
        ):
            name_main_block = n
            break
    if not name_main_block:
        errors.append('Missing `if __name__ == "__main__":` block.')
    else:
        has_main_call = any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "main"
            for node in ast.walk(name_main_block)
        )
        if not has_main_call:
            errors.append('`if __name__ == "__main__":` must call `main()`.')

    # Rule 7: Must have FIGURE_KEY = "<experiment-dir-name>" at module level
    figure_key_node = None
    for node in ast.iter_child_nodes(tree):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "FIGURE_KEY"
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            figure_key_node = node
            break
    if not figure_key_node:
        errors.append('Must have `FIGURE_KEY = "..."` (string constant at module level).')
    else:
        expected = path.parent.name
        actual = figure_key_node.value.value
        if actual != expected:
            errors.append(
                f'FIGURE_KEY must equal experiment dir name: expected "{expected}", got "{actual}".'
            )

    # Rule 8: Must use at least one output method, and at most one save_text or save_tex_figure
    _REQUIRED_OUTPUT = {"savefig", "save_tex", "save_tex_figure", "save_text"}
    output_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in _REQUIRED_OUTPUT
    ]
    if not output_calls:
        errors.append(
            "Must use at least one of: savefig, save_tex, save_tex_figure, save_text."
        )
    tex_output_calls = [
        n for n in output_calls if n.func.attr in ("save_tex_figure", "save_text")
    ]
    if len(tex_output_calls) > 1:
        errors.append(
            f"At most one `save_tex_figure` or `save_text` call allowed (found {len(tex_output_calls)})."
        )

    return errors


def main() -> None:
    files = [Path(f) for f in sys.argv[1:]]
    if not files:
        print(__doc__)
        sys.exit(1)

    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    signal.alarm(0)

    total_errors = 0
    for f in files:
        errs = check_ast(f)
        if errs:
            for e in errs:
                print(f"  INVALID  {f}: {e}")
            total_errors += len(errs)

    if total_errors:
        print(f"\n{total_errors} violation(s) found.")
        sys.exit(1)
    else:
        print(f"All {len(files)} file(s) valid.")


if __name__ == "__main__":
    main()
