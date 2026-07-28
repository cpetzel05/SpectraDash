# Installation

## Requirements

- Raspberry Pi Zero 2 W or newer supported model
- Raspberry Pi OS
- Supported Waveshare Spectra display
- Stable power supply
- Network connection
- Weather-provider API credentials when required

## Recommended preparation

1. Install a fresh Raspberry Pi OS image.
2. Complete operating-system updates.
3. Enable required hardware interfaces for the display.
4. Confirm date, time, and DNS resolution.
5. Back up any existing SpectraDash configuration.

## Install from GitHub

```bash
git clone https://github.com/cpetzel05/SpectraDash.git
cd SpectraDash
sudo bash install.sh
```

The installer should create required directories, install dependencies, configure services, and display the web interface address.

## First launch

Open the web interface from another device on the same network. Complete the setup wizard and select:

- Display profile
- Location
- Weather provider
- Units
- Layout
- Theme
- Refresh interval

## Verification

After setup:

1. Open Developer Mode.
2. Test the weather API.
3. Render a browser preview.
4. Test the physical display.
5. Confirm scheduler and daemon heartbeat status.
