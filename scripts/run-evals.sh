#!/usr/bin/env bash
# Runs the eval suite and fails when a case fails twice in a row.
#
# Usage: scripts/run-evals.sh
# Needs the claude CLI and a Claude credential, such as ANTHROPIC_API_KEY, in the environment.

set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

MODEL="${EVAL_MODEL:-claude-haiku-5-5}"
JUDGE_MODEL="${EVAL_JUDGE_MODEL:-claude-haiku-5-5}"
RESULTS="${EVAL_RESULTS:-evals/results/ci}"

mkdir -p "$RESULTS"

# The suite with no baseline arm, once per case, on the small model, with a spending ceiling and stdin closed.
evaluate() {
  local output="$1"
  shift
  claude plugin eval . --trust-plugin --ablation none --runs 1 --threshold 1.0 \
    --model "$MODEL" --judge-model "$JUDGE_MODEL" --no-publish --max-cost-usd 1 \
    --concurrency 4 "$@" --json "$output" < /dev/null
}

# The names of the cases below the threshold in a result file.
failed_cases() {
  python3 -I -c '
import json
import sys

with open(sys.argv[1]) as result:
    document = json.load(result)
for case in document["cases"]:
    if case["aggregates"]["score"] < document["suite"]["threshold"]:
        print(case["name"])
' "$1"
}

evaluate "$RESULTS/first.json"
status=$?

if [ "$status" -eq 0 ]; then
  echo "evals: every case passed"
  exit 0
fi

if [ "$status" -ne 1 ] || [ ! -s "$RESULTS/first.json" ]; then
  echo "evals: the suite did not run to its end (exit $status)"
  exit 1
fi

again="$(failed_cases "$RESULTS/first.json")"
if [ -z "$again" ]; then
  echo "evals: the suite failed without a case below the threshold"
  exit 1
fi

result=0
while IFS= read -r name; do
  echo "evals: $name failed, running it once more"
  if evaluate "$RESULTS/$name.json" --case "$name"; then
    echo "evals: $name passed on the second run"
  else
    echo "evals: $name failed twice"
    result=1
  fi
done <<< "$again"

exit "$result"
