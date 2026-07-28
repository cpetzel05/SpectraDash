#!/usr/bin/env bash
set -euo pipefail

echo "Validating SpectraDash Sprint 5 files..."

required=(
  "testing/REGRESSION_MATRIX.md"
  "testing/RELEASE_CANDIDATE_TEST_PLAN.md"
  "testing/LONG_RUN_TEST_LOG.md"
  "operations/SUPPORT_BUNDLE_SPEC.md"
  "release/STABLE_EXIT_CRITERIA.md"
  "release/RC1_RELEASE_CHECKLIST.md"
)

for file in "${required[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing required file: $file"
    exit 1
  fi
done

if grep -RInE   --exclude-dir=.git   --exclude='validate_sprint5.sh'   'YOUR_USERNAME|YOUR_REPOSITORY_URL|YOUR_DOCS_URL|YOUR_RELEASE_URL' .; then
  echo "Unresolved placeholder found."
  exit 1
fi

find . -name '*.json' -not -path './.git/*' -print0 | while IFS= read -r -d '' file; do
  python3 -m json.tool "$file" >/dev/null
done

echo "Sprint 5 validation passed."
