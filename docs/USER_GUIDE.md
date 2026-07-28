# SpectraDash User Guide

[README](../README.md) · [Installation](INSTALLATION.md) · [FAQ](FAQ.md) · [Troubleshooting](TROUBLESHOOTING.md)

## Main pages

- **Dashboard:** current weather, forecast, status, and manual refresh controls.
- **Settings / Setup Wizard:** location, units, display profile, refresh schedule, and feature options.
- **Weather Studio:** layout, theme, and Premium LCD appearance settings.
- **Screen Designer:** position and size dashboard regions on a resolution-independent grid.
- **Plugins:** enable or disable supported extensions.
- **Diagnostics:** review services, configuration, display profile, and system health.
- **Developer Mode:** logs, profiling, test controls, and redacted support bundles.

## Daily operation

SpectraDash normally runs unattended. The refresh daemon downloads weather data, renders the selected layout, and updates the configured display on schedule. The watchdog checks the service heartbeat and restarts stalled components.

## Configuration safety

Export configuration before major changes. Reset restores application defaults while preserving location. Factory reset clears the location and returns the program to first-run setup.
