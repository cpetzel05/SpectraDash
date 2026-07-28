#!/usr/bin/env bash
set -euo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "Run this installer with: sudo bash install.sh"
  exit 1
fi

INSTALL_USER=${SUDO_USER:-$(logname 2>/dev/null || echo pi)}
INSTALL_GROUP=$(id -gn "$INSTALL_USER")
APP_DIR=/opt/spectradash
DATA_DIR=/var/lib/spectradash
DRIVER_DIR=/opt/waveshare-e-paper
SOURCE_DIR=$(cd "$(dirname "$0")" && pwd)

echo "Installing SpectraDash 8.0.0-rc18.1 for $INSTALL_USER..."
apt-get update
apt-get install -y python3 python3-venv python3-pip python3-dev git libjpeg-dev zlib1g-dev libopenjp2-7 libtiff6 fonts-dejavu-core python3-spidev python3-gpiozero rsync

mkdir -p "$APP_DIR" "$DATA_DIR/uploads"
if [[ -f "$DATA_DIR/config.json" ]]; then
  cp "$DATA_DIR/config.json" "$DATA_DIR/config.json.backup.$(date +%Y%m%d%H%M%S)"
fi
rsync -a --delete --exclude '.venv' --exclude '__pycache__' --exclude '.pytest_cache' --exclude '*.pyc' "$SOURCE_DIR/" "$APP_DIR/"

python3 -m venv --system-site-packages "$APP_DIR/.venv"
"$APP_DIR/.venv/bin/python" -m pip install --upgrade pip
"$APP_DIR/.venv/bin/pip" install --upgrade --ignore-installed -r "$APP_DIR/requirements.txt"

echo "Running SpectraDash installation self-tests..."
(
  cd "$APP_DIR"
  "$APP_DIR/.venv/bin/python" -c "import spectradash; print('Package import OK:', spectradash.__file__)"
  "$APP_DIR/.venv/bin/python" -m spectradash.hardware_worker --help >/dev/null
)
echo "SpectraDash package and hardware worker checks passed."

if [[ ! -d "$DRIVER_DIR/.git" ]]; then
  rm -rf "$DRIVER_DIR"
  git clone --depth 1 https://github.com/waveshareteam/e-Paper.git "$DRIVER_DIR"
else
  git -C "$DRIVER_DIR" pull --ff-only || true
fi

if command -v raspi-config >/dev/null 2>&1; then
  raspi-config nonint do_spi 0 || true
fi
usermod -aG spi,gpio "$INSTALL_USER" || true
chown -R "$INSTALL_USER:$INSTALL_GROUP" "$APP_DIR" "$DATA_DIR"
chmod +x "$APP_DIR/install.sh" "$APP_DIR/scripts/watchdog.sh"

for unit in spectradash-web.service spectradash-daemon.service; do
  sed -e "s/__USER__/$INSTALL_USER/g" -e "s/__GROUP__/$INSTALL_GROUP/g" "$APP_DIR/systemd/$unit" > "/etc/systemd/system/$unit"
done
cp "$APP_DIR/systemd/spectradash-watchdog.service" /etc/systemd/system/
cp "$APP_DIR/systemd/spectradash-watchdog.timer" /etc/systemd/system/

systemctl disable --now spectradash.service 2>/dev/null || true
rm -f /etc/systemd/system/spectradash.service
systemctl daemon-reload
systemctl enable --now spectradash-daemon.service spectradash-web.service spectradash-watchdog.timer
systemctl restart spectradash-daemon.service spectradash-web.service

IP=$(hostname -I | awk '{print $1}')
echo
echo "SpectraDash 8.0.0-rc18.1 is installed."
echo "Open: http://${IP:-raspberrypi.local}:8080"
echo "Web status: sudo systemctl status spectradash-web"
echo "Daemon status: sudo systemctl status spectradash-daemon"
echo "Daemon logs: sudo journalctl -u spectradash-daemon -f"
echo "Web logs: sudo journalctl -u spectradash-web -f"
