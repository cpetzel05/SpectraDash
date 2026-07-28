#!/usr/bin/env bash
set -euo pipefail

if [[ ! -d .git ]]; then
  echo "Run from the repository root."
  exit 2
fi

git switch main
git pull --ff-only origin main
git switch -c develop 2>/dev/null || git switch develop
git push -u origin develop
echo "Develop branch is ready."
