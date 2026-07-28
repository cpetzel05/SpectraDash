# SpectraDash Sprint 7 — Application Source

This package adds a working, installable SpectraDash application foundation.

Included:

- Local Flask web dashboard
- Setup page
- Mock weather provider
- Open-Meteo weather provider
- Seven-day forecast
- Browser display preview
- Raspberry Pi diagnostics
- Safe preview-only display adapter
- systemd service
- Installer, uninstaller, and tests

Physical Waveshare refresh is intentionally disabled in this sprint until the exact panel driver is validated.

## Install on Raspberry Pi 4

```bash
git clone https://github.com/cpetzel05/SpectraDash.git
cd SpectraDash
chmod +x install.sh uninstall.sh scripts/*.sh
sudo ./install.sh
```

Open `http://PI_ADDRESS:8080`.
