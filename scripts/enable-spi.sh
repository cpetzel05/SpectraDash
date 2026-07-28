#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Run with sudo."; exit 1; }
raspi-config nonint do_spi 0
echo "SPI enabled. Reboot recommended."
