#!/usr/bin/env bash
set -u

report="audit/REPOSITORY_AUDIT.md"
mkdir -p audit
passes=0
warnings=0
blockers=0

pass(){ echo "- PASS: $1" >> "$report"; passes=$((passes+1)); }
warn(){ echo "- WARNING: $1" >> "$report"; warnings=$((warnings+1)); }
fail(){ echo "- BLOCKER: $1" >> "$report"; blockers=$((blockers+1)); }

cat > "$report" <<EOF
# SpectraDash Repository Audit

Generated: $(date -Is)

EOF

if bash scripts/validate_rc1.sh >> "$report" 2>&1; then
  pass "RC1 validation passed"
else
  fail "RC1 validation failed"
fi

if [[ -d .git ]]; then
  pass "Git repository detected"
else
  warn "No .git directory detected"
fi

if git status --porcelain 2>/dev/null | grep -q .; then
  warn "Working tree contains uncommitted changes"
else
  pass "Working tree is clean or Git status is unavailable"
fi

cat >> "$report" <<EOF

## Summary

- Passes: $passes
- Warnings: $warnings
- Blockers: $blockers
EOF

if [[ $blockers -eq 0 ]]; then
  echo "READY FOR RC1" | tee -a "$report"
  exit 0
else
  echo "NOT READY FOR RC1" | tee -a "$report"
  exit 1
fi
