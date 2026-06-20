#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
EXTRACT="scripts/validate_frontmatter.py"

scripts=()
while IFS= read -r script; do scripts+=("${script}"); done < <(find "experiments" -name "*.py" \
    ! -name "run_all.py" -path "experiments/*/*/*.py" | sort)

entries="[]"
while IFS= read -r line; do
    echo "${line}" | jq -e '._error' >/dev/null 2>&1 && continue
    file=$(echo "${line}" | jq -r '._file')
    desc=$(echo "${line}" | jq -r '.description // empty')
    [[ -z "${desc}" ]] && continue
    rel="${file#"$(pwd)/"}"
    entry=$(jq -n --arg path "${rel}" --arg desc "${desc}" \
        '{path: $path, description: $desc}')
    entries=$(echo "${entries}" | jq --argjson e "${entry}" '. + [$e]')
done < <(python3 "${EXTRACT}" extract "${scripts[@]}")

echo "${entries}" | jq '.' > "index.json"
