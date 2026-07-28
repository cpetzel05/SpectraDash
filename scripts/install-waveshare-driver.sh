#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Run with sudo."; exit 1; }

TARGET=/opt/waveshare-13in3e
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

apt-get update
apt-get install -y git python3-pil python3-numpy python3-spidev python3-lgpio

git clone --depth 1 --filter=blob:none --sparse https://github.com/waveshareteam/e-Paper.git "$TMP/e-Paper"
cd "$TMP/e-Paper"
git sparse-checkout set E-paper_Separate_Program/13.3inch_e-Paper_E/RaspberryPi/python

rm -rf "$TARGET"
mkdir -p "$TARGET"
cp -a E-paper_Separate_Program/13.3inch_e-Paper_E/RaspberryPi/python/. "$TARGET/"

echo "Official Waveshare 13.3-inch E driver installed to $TARGET"
