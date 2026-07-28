#!/usr/bin/env bash
set -euo pipefail

version="${1:-v1.0.0-rc1}"
output_dir="${2:-dist}"
mkdir -p "$output_dir"

archive="$output_dir/SpectraDash-${version}.tar.gz"

tar   --exclude='.git'   --exclude='dist'   --exclude='test-runs'   --exclude='*.log'   -czf "$archive" .

sha256sum "$archive" > "${archive}.sha256"

echo "Created:"
echo "  $archive"
echo "  ${archive}.sha256"
