#!/usr/bin/env bash
set -euo pipefail

TAG="${1:-v1.0.0-rc1}"
MODE="${2:---preview}"

if [[ ! -d .git ]]; then
  echo "Run this command from the SpectraDash Git repository root."
  exit 2
fi

git fetch --all --tags

if ! git rev-parse "$TAG^{commit}" >/dev/null 2>&1; then
  echo "Tag or commit '$TAG' was not found."
  echo "Available tags:"
  git tag --list
  exit 1
fi

echo "Current commit:"
git log -1 --oneline

echo
echo "Rollback target:"
git log -1 --oneline "$TAG"

echo
echo "Files that differ:"
git diff --stat "$TAG"..HEAD || true

if [[ "$MODE" != "--apply" ]]; then
  echo
  echo "Preview only. No files were changed."
  echo "To apply:"
  echo "  bash scripts/rollback_to_rc1.sh $TAG --apply"
  exit 0
fi

archive_branch="archive/pre-rollback-$(date +%Y%m%d-%H%M%S)"
git branch "$archive_branch"
echo "Created local archive branch: $archive_branch"

git reset --hard "$TAG"

echo
echo "Local repository restored to $TAG."
echo "Review and test before pushing."
echo "To replace remote main after testing:"
echo "  git push origin $archive_branch"
echo "  git push --force-with-lease origin HEAD:main"
