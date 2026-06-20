"""Manages generated_output/ paths

Usage:
    from generated_output_manager import GeneratedOutputManager, DRAFT, DraftLevel

    out = GeneratedOutputManager(__file__)
    out.savefig(fig, "mse_comparison")
    out.save_tex_figure("mse_comparison", caption="MSE comparison.", label="fig:mse")

    # Quality parameters via match/case:
    match DRAFT:
        case DraftLevel.DRAFT_FINAL_VERSION:
            N_REPS = 500
        case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
            N_REPS = 50
        case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
            N_REPS = 3

"""

from pathlib import Path
from dataclasses import asdict

from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import subprocess
import json


ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
GENERATED_OUTPUT = ROOT / "generated_output"


from enum import Enum


class DraftLevel(Enum):
    DRAFT_FINAL_VERSION = 0
    DRAFT_FOR_HUMAN_TO_VIEW_LATEX = 1
    DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES = 2


import os


def _load_draft_environment_variable() -> DraftLevel:
    val = os.environ.get("DRAFT", "2")
    if val.isdigit():
        try:
            return DraftLevel(int(val))
        except ValueError:
            pass
    return DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES


DRAFT: DraftLevel = _load_draft_environment_variable()

if DRAFT == DraftLevel.DRAFT_FINAL_VERSION:
    _TIMEOUT = 3600
elif DRAFT == DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX :
    _TIMEOUT = 100
else:
    _TIMEOUT = 20

import signal

def _timeout_handler(*_):
    raise SystemExit(f"DRAFT SHOULD RUN IN LESS THAN {_TIMEOUT} SECONDS")

signal.signal(signal.SIGALRM, _timeout_handler)
signal.alarm(_TIMEOUT)



class GeneratedOutputManager:
    """Manages generated_output/ paths"""

    def __init__(self, script_file: str | Path):
        p = Path(script_file).resolve()
        # Expected layout: experiments/XX_chapter/XX_section/experiment_dir/experiment.py
        # Always reference experiment.py regardless of which script instantiates us
        self._script_rel = (p.parent / "experiment.py").relative_to(ROOT)
        experiment = p.parent.name
        section = p.parent.parent.name
        chapter = p.parent.parent.parent.name
        self._base = GENERATED_OUTPUT / chapter / section / experiment
        self._base.mkdir(parents=True, exist_ok=True)

    def _path(self, filename: str) -> Path:
        return self._base / filename

    def _save_png(self, fig: Figure, stem: str, **kwargs) -> Path:
        kwargs.setdefault("dpi", 90)
        kwargs.setdefault("bbox_inches", "tight")
        p = self._path(f"{stem}.png")
        fig.savefig(str(p), **kwargs)
        return p

    def _save_pdf(self, fig: Figure, stem: str, **kwargs) -> Path:
        kwargs.setdefault("bbox_inches", "tight")
        p = self._path(f"{stem}.pdf")
        fig.savefig(str(p), **kwargs)
        return p

    def savefig(self, fig: Figure, stem: str, **kwargs) -> Path:
        path = self._save_pdf(fig, stem, **kwargs)
        plt.close(fig)
        return path

    def save_text(self, content: str, filename: str) -> Path:
        p = self._path(filename)
        p.write_text(content)
        return p

    def save_tex_figure(
        self,
        filename_stem: str,
        caption: str = "",
        label: str = "",
        width: str = r"\textwidth",
        placement: str = "htbp",
    ) -> Path:
        rel_path = self._base.relative_to(GENERATED_OUTPUT)
        ext = "pdf"
        img_path = rel_path / f"{filename_stem}.{ext}"

        if not label:
            label = "-".join([*rel_path.parts, filename_stem])

        base_url = "https://github.com/Shozye/master-thesis-statistics/tree/main"
        url = f"{base_url}/{self._script_rel}"
        url_tex = url.replace("_", r"\_")
        footnote_mark = r"\protect\footnotemark"
        footnote_text = (
            f"\\footnotetext{{\\url{{{url}}}}}\n"
        )

        tex = (
            f"\\begin{{figure}}[{placement}]\n"
            f"  \\centering\n"
            f"  \\includegraphics[width={width}]{{generated_output/{img_path}}}\n"
            f"  \\caption{{{caption}{footnote_mark}}}\n"
            f"  \\label{{fig:{label}}}\n"
            f"\\end{{figure}}\n"
            f"{footnote_text}"
        )
        return self.save_text(tex, f"{filename_stem}.tex")

    def save_dataclass(self, instance, cls: type) -> Path:
        p = self._path("saved_data.json")
        p.write_text(json.dumps(asdict(instance), indent=2))
        return p

    def load_dataclass(self, cls):
        p = self._path("saved_data.json")
        return cls(**json.loads(p.read_text()))
