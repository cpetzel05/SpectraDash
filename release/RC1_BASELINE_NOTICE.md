# SpectraDash RC1 Baseline Notice

SpectraDash development has returned to the last known working `v1.0.0-rc1` baseline.

The larger Sprint 8 replacement is not part of the supported baseline because it changed too many application components at once and introduced a web-service regression.

## Supported baseline

The supported development baseline is the application version that:

- Installed successfully on Raspberry Pi 4
- Started through systemd
- Loaded the web interface on port 8080
- Displayed live Open-Meteo weather
- Saved configuration changes
- Returned system diagnostics
- Rendered a seven-day forecast

## Development policy

New features will be added one at a time. Every feature update must:

1. Start from the known-good RC1 baseline.
2. Pass automated tests.
3. Install on a clean Raspberry Pi.
4. Preserve the existing web interface.
5. Include a rollback procedure.
6. Be merged only after validation.
