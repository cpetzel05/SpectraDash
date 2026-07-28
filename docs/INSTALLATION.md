# Installation

[README](../README.md) · [First Run](FIRST_RUN.md) · [Troubleshooting](TROUBLESHOOTING.md)

## Recommended GitHub installation

```bash
sudo apt update
sudo apt install -y git
git clone https://github.com/cpetzel05/SpectraDash.git
cd SpectraDash
chmod +x install.sh
sudo ./install.sh
```

The installer places the application under `/opt/spectradash`, configuration under `/var/lib/spectradash`, installs systemd units, enables SPI, downloads the official Waveshare repository, and starts the web and refresh services.

## Open the interface

```text
http://raspberrypi.local:8080
```

Use `hostname -I` if mDNS is unavailable.

## Verify services

```bash
sudo systemctl status spectradash-web --no-pager
sudo systemctl status spectradash-daemon --no-pager
sudo systemctl status spectradash-watchdog.timer --no-pager
```
