# SpectraDash Sprint 8 — Full Interface Upgrade

This package upgrades the working Sprint 7 foundation with:

- Weather Station and Premium LCD layouts
- Dark, light, ocean, desert, and high-contrast themes
- ZIP code and city lookup
- Open-Meteo live weather
- AQI and UV data
- Weather alerts panel
- Moon phase and astronomy
- Local SVG weather icons
- Dashboard auto-refresh
- Preview rendering
- Diagnostics page
- Backup and restore tools
- Safer service update script

Physical Waveshare refresh remains disabled until the exact EL133UF1 driver is validated.

## Upgrade an existing installation

```bash
cd ~/SpectraDash
git pull origin main
chmod +x install.sh scripts/*.sh
sudo ./install.sh
```

Then open `http://PI_ADDRESS:8080`.
