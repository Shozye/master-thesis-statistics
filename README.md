# submodule-statistics

Generates plots and tables for the master thesis. Output lands in `generated_output/` and gets copied to the LaTeX submodule via `just copy-generated-output`.

## Running

```bash
just run-experiment experiments/03_chapter/02_section/my-experiment/experiment.py
just run-all-experiments
just copy-generated-output  # copy output to LaTeX submodule
just statistics-check       # validate all contracts
```

## How things should look

Go into these files when you need more information:

- [generated_output_manager.py](generated_output_manager.py) — **important**: utility for saving figures and tables
- [schema/directory_schema_layout.yaml](schema/directory_schema_layout.yaml) — enforced directory structure
- [schema/experiment_py_contract.md](schema/experiment_py_contract.md) — rules every experiment.py must follow
- [schema/experiment_py_frontmatter_yaml_schema.json](schema/experiment_py_frontmatter_yaml_schema.json) — experiment.py frontmatter schema
- [schema/experiment_idea_schema.json](schema/experiment_idea_schema.json) — experiment-idea.md frontmatter schema
- [schema/experiments_index_schema.json](schema/experiments_index_schema.json) — index.json field definitions
- [guidance/experiments.md](guidance/experiments.md) — how experiments should be structured and parametrized
- [guidance/plot.md](guidance/plot.md) — how plots should look
