# First-run setup and configuration management

SpectraDash 8.0.0-rc18.2 ships without a preset location. A new installation opens the Setup Wizard and does not request weather data until the user enters a city, state, ZIP code, or place name.

## Configuration tools

Settings includes:

- **Export configuration** — downloads a JSON backup.
- **Import JSON** — validates and restores a SpectraDash configuration.
- **Reset settings to defaults** — restores display and feature defaults while preserving the configured location.
- **Factory reset SpectraDash** — clears the location and returns to the first-run wizard.

## Uninstall

```bash
sudo bash /opt/spectradash/uninstall.sh
```

The default uninstall preserves `/var/lib/spectradash` and `/opt/waveshare-e-paper`. To remove everything owned by SpectraDash:

```bash
sudo bash /opt/spectradash/uninstall.sh --purge-data --remove-driver
```
