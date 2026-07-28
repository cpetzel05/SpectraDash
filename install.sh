#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo "Run: sudo ./install.sh"; exit 1; }

apt-get update
apt-get install -y python3 python3-venv python3-pip fonts-dejavu-core
id spectradash >/dev/null 2>&1 || useradd --system --home /var/lib/spectradash --shell /usr/sbin/nologin spectradash
mkdir -p /opt/spectradash /etc/spectradash /var/lib/spectradash
cp -a . /opt/spectradash/
python3 -m venv /opt/spectradash/venv
/opt/spectradash/venv/bin/pip install --upgrade pip
/opt/spectradash/venv/bin/pip install /opt/spectradash
[[ -f /etc/spectradash/config.json ]] || cp /opt/spectradash/config/default-config.json /etc/spectradash/config.json
cp /opt/spectradash/systemd/spectradash.service /etc/systemd/system/
chown -R spectradash:spectradash /etc/spectradash /var/lib/spectradash
chmod 750 /etc/spectradash
chmod 640 /etc/spectradash/config.json
systemctl daemon-reload
systemctl enable --now spectradash
echo "Open http://$(hostname -I | awk '{print $1}'):8080"
