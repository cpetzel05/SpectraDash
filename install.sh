#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Run: sudo ./install.sh"; exit 1; }

APP=/opt/spectradash
CFG=/etc/spectradash
DATA=/var/lib/spectradash
STAMP="$(date +%Y%m%d-%H%M%S)"

apt-get update
apt-get install -y python3 python3-venv python3-pip git fonts-dejavu-core python3-lgpio python3-spidev

id spectradash >/dev/null 2>&1 || useradd --system --home "$DATA" --shell /usr/sbin/nologin spectradash
getent group gpio >/dev/null || groupadd gpio
getent group spi >/dev/null || groupadd spi
usermod -a -G gpio,spi spectradash

mkdir -p "$APP" "$CFG" "$DATA/backups"
if [[ -f "$CFG/config.json" ]]; then
  cp "$CFG/config.json" "$DATA/backups/config-before-install-$STAMP.json"
fi

rm -rf "$APP"
mkdir -p "$APP"
cp -a . "$APP/"
python3 -m venv --system-site-packages "$APP/venv"
"$APP/venv/bin/pip" install --upgrade pip
"$APP/venv/bin/pip" install "$APP"

[[ -f "$CFG/config.json" ]] || cp "$APP/config/default-config.json" "$CFG/config.json"
cp "$APP/systemd/spectradash.service" /etc/systemd/system/
cp "$APP/systemd/spectradash-worker.service" /etc/systemd/system/

chown -R spectradash:spectradash "$CFG" "$DATA"
chmod 750 "$CFG"
chmod 640 "$CFG/config.json"

systemctl daemon-reload
systemctl enable spectradash spectradash-worker
systemctl restart spectradash spectradash-worker

echo
echo "SpectraDash installed in preview mode."
echo "Open http://$(hostname -I | awk '{print $1}'):8080"
echo
echo "Before physical display use:"
echo "  sudo scripts/install-waveshare-driver.sh"
echo "  sudo scripts/test-waveshare-display.sh"
