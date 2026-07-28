#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Run: sudo ./install.sh"; exit 1; }

APP=/opt/spectradash
CONFIG=/etc/spectradash
DATA=/var/lib/spectradash
STAMP="$(date +%Y%m%d-%H%M%S)"

apt-get update
apt-get install -y python3 python3-venv python3-pip fonts-dejavu-core
id spectradash >/dev/null 2>&1 || useradd --system --home "$DATA" --shell /usr/sbin/nologin spectradash
mkdir -p "$APP" "$CONFIG" "$DATA/backups"

if [[ -f "$CONFIG/config.json" ]]; then
  cp "$CONFIG/config.json" "$DATA/backups/config-before-upgrade-$STAMP.json"
fi

find "$APP" -mindepth 1 -maxdepth 1 ! -name venv -exec rm -rf {} +
cp -a . "$APP/"
python3 -m venv "$APP/venv"
"$APP/venv/bin/pip" install --upgrade pip
"$APP/venv/bin/pip" install "$APP"

[[ -f "$CONFIG/config.json" ]] || cp "$APP/config/default-config.json" "$CONFIG/config.json"
cp "$APP/systemd/spectradash.service" /etc/systemd/system/
chown -R spectradash:spectradash "$CONFIG" "$DATA"
chmod 750 "$CONFIG"
chmod 640 "$CONFIG/config.json"
systemctl daemon-reload
systemctl enable spectradash
systemctl restart spectradash

echo
echo "SpectraDash Sprint 8 installed."
echo "Open http://$(hostname -I | awk '{print $1}'):8080"
