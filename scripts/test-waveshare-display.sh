#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Run with sudo."; exit 1; }

if [[ ! -f /opt/waveshare-13in3e/python/examples/epd_13in3E_test.py ]]; then
  echo "Driver test not found. Run install-waveshare-driver.sh first."
  exit 1
fi

echo "This test will refresh and clear the physical display."
read -r -p "Type TEST to continue: " answer
[[ "$answer" == "TEST" ]] || { echo "Cancelled."; exit 1; }

cd /opt/waveshare-13in3e/python/examples
python3 epd_13in3E_test.py
