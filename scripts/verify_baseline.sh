#!/usr/bin/env bash
set -euo pipefail

required=(
  "README.md"
  "release/RC1_BASELINE_NOTICE.md"
  "release/DEVELOPMENT_RELEASE_PLAN.md"
  "docs/ROLLBACK_TO_RC1.md"
  "docs/FEATURE_CHANGE_POLICY.md"
)

for file in "${required[@]}"; do
  [[ -f "$file" ]] || { echo "Missing: $file"; exit 1; }
done

if grep -RInE \
  --exclude-dir=.git \
  --exclude='verify_baseline.sh' \
  'YOUR_USERNAME|YOUR_REPOSITORY_URL|YOUR_DOCS_URL' \
  README.md release docs operations project community; then
  echo "Unresolved placeholder found."
  exit 1
fi

find scripts -name '*.sh' -print0 |
while IFS= read -r -d '' file; do
  bash -n "$file"
done

echo "RC1 baseline documentation package passed validation."
