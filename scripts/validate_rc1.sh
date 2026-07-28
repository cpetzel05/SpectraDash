#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f README.md || ! -d release || ! -d testing ]]; then
  echo "Run this command from the SpectraDash repository root."
  exit 2
fi

required=(
  "README.md"
  "LICENSE.txt"
  "CONTRIBUTING.md"
  "SECURITY.md"
  "CHANGELOG.md"
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

placeholder_regex='YOUR_(USERNAME|REPOSITORY_URL|DOCS_URL|RELEASE_URL|DISCUSSIONS_URL)'

if grep -RInE \
  --exclude-dir=.git \
  --exclude-dir=.archive \
  --exclude='validate_rc1.sh' \
  --exclude='repository_audit.sh' \
  "$placeholder_regex" \
  .github release testing operations security docs README.md CONTRIBUTING.md SECURITY.md; then
  echo "Unresolved placeholder found."
  exit 1
fi

find . -name '*.json' -not -path './.git/*' -print0 |
while IFS= read -r -d '' file; do
  python3 -m json.tool "$file" >/dev/null
done

find scripts -name '*.sh' -print0 |
while IFS= read -r -d '' file; do
  bash -n "$file"
done

echo "RC1 validation passed."
