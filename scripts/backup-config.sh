#!/usr/bin/env bash
set -euo pipefail
mkdir -p /var/lib/spectradash/backups
sudo cp /etc/spectradash/config.json "/var/lib/spectradash/backups/config-manual-$(date +%Y%m%d-%H%M%S).json"
sudo chown -R spectradash:spectradash /var/lib/spectradash/backups
echo "Backup created."
