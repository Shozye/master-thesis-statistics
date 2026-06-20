PIP_WHEELS_DIR := $(HOME)/pip-wheels
WCE_PATH ?=
VENV := .venv

.PHONY: setup-git-hooks download-wheels clean statistics-check venv

# Create venv and install deps (no WCE)
venv:
	uv venv --clear $(VENV)
	uv pip install --python $(VENV) --find-links $(PIP_WHEELS_DIR) --no-index .

# Validate all experiment frontmatter and regenerate index.json
statistics-check:
	$(VENV)/bin/python scripts/validate_directory_schema.py schema/directory_schema_layout.yaml
	files=$$(find experiments -name "experiment.py" -path "experiments/*_chapter/*_section/*/experiment.py" | sort) && \
	$(VENV)/bin/python scripts/validate_frontmatter.py validate schema/experiment_py_frontmatter_yaml_schema.json $${files} && \
	$(VENV)/bin/python scripts/validate_experiments.py $${files}
	@cf_files=$$(find experiments -name "create_figure.py" -path "experiments/*_chapter/*_section/*/create_figure.py" | sort); \
	if [ -n "$$cf_files" ]; then $(VENV)/bin/python scripts/validate_create_figure.py $$cf_files; fi
	$(VENV)/bin/python scripts/validate_experiment_idea.py
	bash scripts/regenerate_index.sh

setup-git-hooks:
	git config core.hooksPath .githooks
	@echo "Git hooks configured: core.hooksPath = .githooks"

# Download all deps into a local wheel cache (for offline installs)
download-wheels:
	uv run --no-project --with pip -- pip download . -d $(PIP_WHEELS_DIR)

clean:
	rm -rf generated_output .venv master_thesis_statistics.egg-info .mypy_cache
	rm -rf build
	find . -name __pycache__ -type d | xargs rm -rf
