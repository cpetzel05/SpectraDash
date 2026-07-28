#!/usr/bin/env bash
set -euo pipefail

timestamp="$(date +%Y%m%d-%H%M%S)"
target="test-runs/rc1-${timestamp}"
mkdir -p "$target"

cp testing/RC1_REGRESSION_MATRIX.md "$target/regression-matrix.md"
cp testing/RC1_TEST_REPORT.md "$target/test-report.md"
cp testing/RC1_72_HOUR_PLAN.md "$target/72-hour-plan.md"
cp security/RC1_SECURITY_REVIEW.md "$target/security-review.md"

echo "Created RC1 test run: $target"
