venv_dir := ".venv"
draft := "1"

export DRAFT := draft

default:
    just --list

# Create venv and install deps (no WCE)
venv:
    make venv

# Run all experiments 
run-all:
    {{venv_dir}}/bin/python scripts/run_experiments.py experiments

# Run experiment(s) matching a pattern (substring match, parallel if multiple)
run-experiment path:
    {{venv_dir}}/bin/python scripts/run_experiments.py "{{path}}" --mode experiment

# Run create_figure.py for experiment(s) matching a pattern
create-figure path:
    {{venv_dir}}/bin/python scripts/run_experiments.py "{{path}}" --mode figure

# Run all create_figure.py scripts
create-all-figures:
    {{venv_dir}}/bin/python scripts/run_experiments.py experiments --mode figure

# Run all experiments, then run all create_figure.py scripts
regenerate-all-figures:
    just run-all
    just create-all-figures

# Validate all experiment frontmatter and regenerate index.json
statistics-check:
    make statistics-check

# Remove generated outputs and venv
clean:
    make clean
