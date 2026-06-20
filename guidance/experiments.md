# General guidance
## Draft versions
Experiment shall contain Quality parameters set on the start for different draft versions.
Draft types are:
- DRAFT = 0 Final Version is for the end product of master thesis. It will be set by ME later on.
- DRAFT = 1 Human View is to create a .pdf for viable working with the .tex. Experiments with this value should run in ~60 seconds if possible and they throw error when run for more than 70 seconds.
- DRAFT = 2 Fix is to be fast one to focus on fixing experiments or some runs. Experiments should run in 5 seconds and they throw error when run for more than 30 seconds.

## Directory structure
experiments
-> \d\d_chapter/
    .gitkeep (allowed)
    -> \d\d_section/ or na_section
        .gitkeep (allowed)
        -> 22-to-30-character-experiment-description/
            -> experiment.py
            -> experiment-idea.md

## how to get section index? 
You can find section index by referring to the submodule latex and see which section of the chapter inputs generated figures

## Rules per file:
see `experiment_py_contract.md`
