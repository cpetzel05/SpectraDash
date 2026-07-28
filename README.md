# SpectraDash

<p align="center">
  <strong>Weather, reimagined for color e-paper.</strong>
</p>

<p align="center">
  A polished, themeable weather dashboard for Raspberry Pi and Waveshare Spectra displays.
</p>

<p align="center">
  <a href="https://github.com/cpetzel05/SpectraDash/releases"><img alt="Release" src="https://img.shields.io/github/v/release/cpetzel05/SpectraDash?include_prereleases"></a>
  <a href="https://github.com/cpetzel05/SpectraDash/actions"><img alt="Build" src="https://img.shields.io/github/actions/workflow/status/cpetzel05/SpectraDash/validate.yml?branch=main"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="Python" src="https://img.shields.io/badge/python-3.10%2B-blue">
  <img alt="Raspberry Pi" src="https://img.shields.io/badge/Raspberry%20Pi-supported-c51a4a">
  <img alt="Status" src="https://img.shields.io/badge/status-public%20beta-orange">
</p>

> **Public testing:** SpectraDash v1.0 is entering public testing. Back up your configuration before upgrading and report problems using the included issue templates.

## Overview

SpectraDash turns a Raspberry Pi and a supported color e-paper display into a full-featured weather station. It combines premium dashboard layouts, detailed forecasts, astronomy, alerts, environmental data, and hardware-aware refresh controls in one extensible platform.

The initial hardware target is the Waveshare 13.3-inch Spectra 6 display using the EL133UF1 panel and a Raspberry Pi Zero 2 W. The software is designed around display profiles so additional Raspberry Pi models and e-paper panels can be supported over time.

## Highlights

- Weather Station and Premium LCD layouts
- Light, dark, and automatic appearance modes
- Seven-day forecast with current conditions
- Weather alerts across primary layouts
- Air quality, UV, pressure, wind, humidity, dew point, and precipitation
- Realistic Moon phases and expanded astronomy information
- Theme gallery and scheduled theme rotation
- First-run setup wizard
- Browser-based configuration and preview rendering
- Developer Mode with live diagnostics, logs, and test controls
- Watchdog, scheduler, and display refresh management
- Plugin SDK, theme system, and display-profile architecture
- Performance modes for lower-powered Raspberry Pi hardware

## Screenshots

Add optimized screenshots to `assets/screenshots/` using the names below:

| Layout | File |
|---|---|
| Weather Station | `weather-station.png` |
| Premium LCD Dark | `premium-lcd-dark.png` |
| Premium LCD Light | `premium-lcd-light.png` |
| Theme Gallery | `theme-gallery.png` |
| Setup Wizard | `setup-wizard.png` |
| Developer Mode | `developer-mode.png` |

Example:

```markdown
![Weather Station](assets/screenshots/weather-station.png)
```

## Supported hardware

### Primary tested configuration

- Raspberry Pi Zero 2 W
- Waveshare 13.3-inch Spectra 6 display
- EL133UF1 panel
- Raspberry Pi OS

### Intended Raspberry Pi support

| Model | Status | Notes |
|---|---|---|
| Raspberry Pi Zero 2 W | Primary target | Recommended for the reference installation |
| Raspberry Pi 3 | Community testing | Expected to work with supported display hardware |
| Raspberry Pi 4 | Community testing | Suitable for development and heavier preview use |
| Raspberry Pi 5 | Community testing | May require hardware-specific GPIO or driver adjustments |

See [Supported Hardware](docs/hardware/supported-hardware.md) for details.

## Quick start

### Install from GitHub

```bash
git clone https://github.com/cpetzel05/SpectraDash.git
cd SpectraDash
sudo bash install.sh
```

Then open the SpectraDash web interface from another device on the same network and complete the setup wizard.

### Update

```bash
cd ~/SpectraDash
git pull
sudo bash install.sh
```

Always back up your configuration before major upgrades.

## Documentation

### User documentation

- [Installation](docs/user/installation.md)
- [First-run setup](docs/user/first-run-setup.md)
- [Configuration](docs/user/configuration.md)
- [Updating](docs/user/updating.md)
- [Troubleshooting](docs/user/troubleshooting.md)
- [FAQ](docs/user/faq.md)

### Hardware documentation

- [Supported hardware](docs/hardware/supported-hardware.md)
- [Display profiles](docs/hardware/display-profiles.md)
- [Wiring and safety](docs/hardware/wiring-and-safety.md)

### Developer documentation

- [Architecture](docs/developer/architecture.md)
- [Development setup](docs/developer/development-setup.md)
- [Theme development](docs/developer/theme-development.md)
- [Plugin development](docs/developer/plugin-development.md)
- [API reference](docs/developer/api-reference.md)
- [Testing and release process](docs/developer/testing-and-releases.md)

### Community documentation

- [Public testing guide](docs/community/public-testing.md)
- [Hardware compatibility reports](docs/community/hardware-reporting.md)
- [Discussion categories](docs/community/discussions-setup.md)

## Public testing priorities

We especially need feedback on:

1. Fresh installation on Raspberry Pi OS
2. Upgrading from prior release candidates
3. Long-running stability over 24 to 72 hours
4. Display refresh synchronization
5. Theme switching and automatic theme rotation
6. Fahrenheit and Celsius handling
7. Weather-provider reliability
8. Hardware compatibility beyond the primary configuration

## Privacy and security

Never post API keys, Wi-Fi credentials, authentication tokens, precise home addresses, or private support bundles in public issues. See [SECURITY.md](SECURITY.md) for reporting security problems.

## Contributing

Bug reports, hardware reports, documentation improvements, themes, display profiles, and plugins are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Project status

SpectraDash is preparing for its first stable release. The current release path is:

```text
v1.0.0-beta.1 -> public testing -> v1.0.0-rc1 -> v1.0.0 stable
```

See [ROADMAP.md](ROADMAP.md) and [CHANGELOG.md](CHANGELOG.md).

## License

SpectraDash is released under the MIT License. See [LICENSE](LICENSE).
