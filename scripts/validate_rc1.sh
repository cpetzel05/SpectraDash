#!/usr/bin/env bash
set -euo pipefail

echo "Validating SpectraDash RC1 release package..."

required=(
  "release/RELEASE_NOTES_v1.0.0-rc1.md"
  "release/RC1_PUBLISH_CHECKLIST.md"
  "release/KNOWN_ISSUES_RC1.md"
  "testing/RC1_REGRESSION_MATRIX.md"
  "testing/RC1_TEST_REPORT.md"
  "testing/RC1_72_HOUR_PLAN.md"
  "security/RC1_SECURITY_REVIEW.md"
  "operations/RC1_ROLLBACK_PLAN.md"
)

for file in "${required[@]}"; do
  [[ -f "$file" ]] || { echo "Missing: $file"; exit 1; }
done

if grep -RInE   --exclude-dir=.git   --exclude='validate_rc1.sh'   'YOUR_USERNAME|YOUR_REPOSITORY_URL|YOUR_DOCS_URL|YOUR_RELEASE_URL' .; then
  echo "Unresolved placeholder found."
  exit 1
fi

find . -name '*.json' -not -path './.git/*' -print0 | while IFS= read -r -d '' file; do
  python3 -m json.tool "$file" >/dev/null
done

find scripts -name '*.sh' -print0 | while IFS= read -r -d '' file; do
  bash -n "$file"
done

echo "RC1 package validation passed."
