#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Run: sudo ./uninstall.sh"; exit 1; }
systemctl disable --now spectradash 2>/dev/null || true
rm -f /etc/systemd/system/spectradash.service
systemctl daemon-reload
rm -rf /opt/spectradash
echo "Application removed. Configuration remains in /etc/spectradash."
