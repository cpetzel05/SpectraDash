#!/usr/bin/env bash
set -euo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "Run this uninstaller with: sudo bash uninstall.sh"
  exit 1
fi

PURGE_DATA=false
REMOVE_DRIVER=false
ASSUME_YES=false
for arg in "$@"; do
  case "$arg" in
    --purge-data) PURGE_DATA=true ;;
    --remove-driver) REMOVE_DRIVER=true ;;
    --yes|-y) ASSUME_YES=true ;;
    --help|-h)
      echo "Usage: sudo bash uninstall.sh [--purge-data] [--remove-driver] [--yes]"
      echo "By default, configuration/data and the Waveshare driver are preserved."
      exit 0 ;;
    *) echo "Unknown option: $arg"; exit 2 ;;
  esac
done

if ! $ASSUME_YES; then
  echo "SpectraDash services and /opt/spectradash will be removed."
  $PURGE_DATA && echo "Configuration and data in /var/lib/spectradash will also be deleted." || echo "Configuration and data will be preserved."
  $REMOVE_DRIVER && echo "The shared Waveshare driver checkout will also be deleted." || echo "The Waveshare driver will be preserved."
  read -r -p "Type UNINSTALL to continue: " answer
  [[ "$answer" == "UNINSTALL" ]] || { echo "Cancelled."; exit 0; }
fi

systemctl disable --now spectradash-web.service spectradash-daemon.service spectradash-watchdog.timer 2>/dev/null || true
systemctl stop spectradash-watchdog.service 2>/dev/null || true
rm -f /etc/systemd/system/spectradash-web.service /etc/systemd/system/spectradash-daemon.service /etc/systemd/system/spectradash-watchdog.service /etc/systemd/system/spectradash-watchdog.timer
systemctl daemon-reload
systemctl reset-failed || true
rm -rf /opt/spectradash

if $PURGE_DATA; then rm -rf /var/lib/spectradash; fi
if $REMOVE_DRIVER; then rm -rf /opt/waveshare-e-paper; fi

echo "SpectraDash has been uninstalled."
$PURGE_DATA || echo "Preserved data: /var/lib/spectradash"
$REMOVE_DRIVER || echo "Preserved driver: /opt/waveshare-e-paper"
echo "System packages installed as dependencies were left in place."
