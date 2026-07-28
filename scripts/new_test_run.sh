#!/usr/bin/env bash
set -euo pipefail

timestamp="$(date +%Y%m%d-%H%M%S)"
target="test-runs/${timestamp}"
mkdir -p "$target"

cp testing/LONG_RUN_TEST_LOG.md "$target/long-run-test.md"
cp testing/REGRESSION_MATRIX.md "$target/regression-matrix.md"
cp testing/PERFORMANCE_BASELINE.md "$target/performance-baseline.md"

cat > "$target/README.md" <<EOF
# SpectraDash Test Run

Created: $(date -Is)

Files:

- long-run-test.md
- regression-matrix.md
- performance-baseline.md
EOF

echo "Created test run: $target"
