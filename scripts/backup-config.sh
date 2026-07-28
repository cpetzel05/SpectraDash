#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Run with sudo."; exit 1; }
mkdir -p /var/lib/spectradash/backups
cp /etc/spectradash/config.json "/var/lib/spectradash/backups/config-$(date +%Y%m%d-%H%M%S).json"
chown -R spectradash:spectradash /var/lib/spectradash/backups
echo "Backup complete."
