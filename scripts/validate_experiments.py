#!/usr/bin/env python3
"""Validate experiment.py files against experiment_py_contract.md.

Rules:
  1. GeneratedOutputManager: exactly one `out = GeneratedOutputManager(__file__)`
  2. match DRAFT: exactly one block with all 3 DraftLevel cases,
     each case body only `VAR = number` or `VAR = [numbers]`, same vars in all cases.
  3. tqdm: if used — `import tqdm` only, one `tqdm.tqdm(...)` call with desc=, colour=, unit=.
  4. `if __name__ == "__main__":` block required.
  5. Frontmatter validated separately by validate_frontmatter.py.

Usage:
  validate_experiments.py <file>...
"""

import ast
import signal
import sys
from pathlib import Path


def _is_numeric_literal(node: ast.expr) -> bool:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return True
    if (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.USub)
        and isinstance(node.operand, ast.Constant)
        and isinstance(node.operand.value, (int, float))
    ):
        return True
    return False


def _is_gom_call(node: ast.expr) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "GeneratedOutputManager"
        and len(node.args) == 1
        and isinstance(node.args[0], ast.Name)
        and node.args[0].id == "__file__"
        and not node.keywords
    )


def _is_tqdm_tqdm_call(node: ast.expr) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "tqdm"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "tqdm"
    )


def check_ast(path: Path) -> list[str]:
    """AST-based checks."""
    try:
        source = path.read_text()
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as e:
        return [f"SyntaxError: {e}"]

    errors = []

    # --- Rule 1: GeneratedOutputManager ---
    gom_exact = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "out"
            and _is_gom_call(node.value)
        ):
            gom_exact.append(node)
    if len(gom_exact) != 1:
        errors.append(
            f"Must have exactly one `out = GeneratedOutputManager(__file__)` (found {len(gom_exact)})."
        )

    # --- Rule 2: match DRAFT ---
    _REQUIRED_CASES = {
        "DRAFT_FINAL_VERSION",
        "DRAFT_FOR_HUMAN_TO_VIEW_LATEX",
        "DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES",
    }
    match_stmts = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Match) and isinstance(n.subject, ast.Name) and n.subject.id == "DRAFT"
    ]
    if len(match_stmts) != 1:
        errors.append(f"Must have exactly one `match DRAFT:` (found {len(match_stmts)}).")
    else:
        match_node = match_stmts[0]
        found_cases: dict[str, set[str]] = {}
        for case in match_node.cases:
            pat = case.pattern
            if (
                isinstance(pat, ast.MatchValue)
                and isinstance(pat.value, ast.Attribute)
                and isinstance(pat.value.value, ast.Name)
                and pat.value.value.id == "DraftLevel"
            ):
                case_name = pat.value.attr
            else:
                errors.append("match DRAFT case pattern must be `DraftLevel.<MEMBER>`.")
                continue
            if case_name not in _REQUIRED_CASES:
                errors.append(f"Unexpected case `DraftLevel.{case_name}` in match DRAFT.")
                continue
            var_names: set[str] = set()
            for stmt in case.body:
                if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1:
                    tgt = stmt.targets[0]
                    if isinstance(tgt, ast.Name):
                        val = stmt.value
                        if _is_numeric_literal(val):
                            var_names.add(tgt.id)
                            continue
                        if isinstance(val, ast.List) and all(
                            _is_numeric_literal(e) for e in val.elts
                        ):
                            var_names.add(tgt.id)
                            continue
                errors.append(
                    f"case DraftLevel.{case_name}: only `VAR = number` or "
                    f"`VAR = [numbers]` allowed (line {stmt.lineno})."
                )
            found_cases[case_name] = var_names

        missing = _REQUIRED_CASES - set(found_cases)
        if missing:
            errors.append(f"match DRAFT missing cases: {sorted(missing)}.")

        # Rule 2b: cases must appear in canonical order
        _REQUIRED_ORDER = [
            "DRAFT_FINAL_VERSION",
            "DRAFT_FOR_HUMAN_TO_VIEW_LATEX",
            "DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES",
        ]
        case_order = [c for c in found_cases if c in _REQUIRED_ORDER]
        if case_order != _REQUIRED_ORDER[: len(case_order)]:
            errors.append(
                "match DRAFT cases must be ordered: "
                "DRAFT_FINAL_VERSION, DRAFT_FOR_HUMAN_TO_VIEW_LATEX, "
                "DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES."
            )

        if len(found_cases) >= 2:
            ref_name, ref_vars = next(iter(found_cases.items()))
            for cn, cv in found_cases.items():
                if cv != ref_vars:
                    errors.append(
                        f"case DraftLevel.{cn} sets {sorted(cv)} but "
                        f"DraftLevel.{ref_name} sets {sorted(ref_vars)}. Must be same."
                    )

    # --- Rule 3: tqdm ---
    tqdm_imports = []
    from_tqdm_imports = []
    tqdm_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "tqdm":
                    tqdm_imports.append(node)
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("tqdm"):
            from_tqdm_imports.append(node)
        if isinstance(node, ast.Call) and _is_tqdm_tqdm_call(node):
            tqdm_calls.append(node)

    if from_tqdm_imports:
        errors.append("`from tqdm import ...` not allowed. Use `import tqdm`.")
    if tqdm_calls:
        if not tqdm_imports:
            errors.append("`tqdm.tqdm(` used but `import tqdm` missing.")
        if len(tqdm_calls) > 1:
            errors.append(f"`tqdm.tqdm(` must appear at most once (found {len(tqdm_calls)}).")
        call = tqdm_calls[0]
        present = {kw.arg for kw in call.keywords}
        for req in ("desc", "colour", "unit", "mininterval"):
            if req not in present:
                errors.append(f"`tqdm.tqdm(` missing required kwarg `{req}=`.")
        for kw in call.keywords:
            if kw.arg == "mininterval":
                if not (isinstance(kw.value, ast.Constant) and kw.value.value == 10.0):
                    errors.append("`tqdm.tqdm(` must have `mininterval=10.0`.")

        # Rule 3b: must be assigned as `pbar = tqdm.tqdm(total=TOTAL_PBAR_VALUE, ...)`
        if "total" not in present:
            errors.append("`tqdm.tqdm(` missing required kwarg `total=`.")
        else:
            total_kw = next(kw for kw in call.keywords if kw.arg == "total")
            if not (isinstance(total_kw.value, ast.Name) and total_kw.value.id == "TOTAL_PBAR_VALUE"):
                errors.append("`tqdm.tqdm(` must have `total=TOTAL_PBAR_VALUE`.")

        # Check assigned to `pbar`
        pbar_assign = False
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Assign)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "pbar"
                and isinstance(node.value, ast.Call)
                and _is_tqdm_tqdm_call(node.value)
            ):
                pbar_assign = True
                break
        if not pbar_assign:
            errors.append("`tqdm.tqdm(` must be assigned to `pbar` variable.")

        # Rule 3c: must have `pbar.update(1)` and `pbar.close()`
        has_update = False
        has_close = False
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "pbar"
            ):
                if node.func.attr == "update" and len(node.args) == 1:
                    has_update = True
                if node.func.attr == "close" and not node.args:
                    has_close = True
        if not has_update:
            errors.append("Must have `pbar.update(1)` call.")
        if not has_close:
            errors.append("Must have `pbar.close()` call.")

    # --- Rule 4: if __name__ == "__main__" with main() call ---
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
        # Check that main() is called somewhere inside
        has_main_call = any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "main"
            for node in ast.walk(name_main_block)
        )
        if not has_main_call:
            errors.append('`if __name__ == "__main__":` must call `main()`.')

    # --- Rule 6: DataModel + save_dataclass (when create_figure.py exists) ---
    has_create_figure = (path.parent / "create_figure.py").exists()
    if has_create_figure:
        has_datamodel_import = any(
            isinstance(node, ast.ImportFrom)
            and node.module == "data_for_figure_dataclass"
            and any(alias.name == "DataModel" for alias in node.names)
            for node in ast.walk(tree)
        )
        if not has_datamodel_import:
            errors.append("Must have `from data_for_figure_dataclass import DataModel`.")

        has_save = any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "save_dataclass"
            and any(isinstance(a, ast.Name) and a.id == "DataModel" for a in node.args)
            for node in ast.walk(tree)
        )
        if not has_save:
            errors.append("Must use `save_dataclass(..., DataModel)`.")

    # --- Rule 7: Must NOT use savefig/save_tex/save_tex_figure ---
    _FORBIDDEN_OUTPUT = {"savefig", "save_tex", "save_tex_figure"}
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in _FORBIDDEN_OUTPUT
        ):
            errors.append(
                f"experiment.py must NOT use `{node.func.attr}` (line {node.lineno}). "
                "Output functions belong in create_figure.py."
            )
            break

    # --- Rule 8: Must NOT define get_caption or get_test_caption ---
    _FORBIDDEN_DEFS = {"get_caption", "get_test_caption"}
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name in _FORBIDDEN_DEFS:
            errors.append(
                f"`{node.name}` must not be defined in experiment.py (line {node.lineno}). "
                "Caption functions belong in create_figure.py."
            )

    return errors


def main() -> None:
    files = [Path(f) for f in sys.argv[1:]]
    if not files:
        print(__doc__)
        sys.exit(1)

    # Prevent __pycache__ creation and disable SIGALRM from generated_output_manager
    sys.dont_write_bytecode = True
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    signal.alarm(0)

    # Add experiments root to path for imports
    experiments_root = files[0].resolve().parent
    while experiments_root.name != "experiments" and experiments_root != experiments_root.parent:
        experiments_root = experiments_root.parent
    stats_root = experiments_root.parent
    if str(stats_root) not in sys.path:
        sys.path.insert(0, str(stats_root))

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
