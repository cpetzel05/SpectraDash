# Public Beta Test Plan

## Objective

Validate that SpectraDash can be installed, configured, refreshed, recovered, and maintained by users outside the original development environment.

## Test groups

### Installation

- Fresh Raspberry Pi OS installation
- Installer success
- Dependency installation
- Service creation
- First browser connection
- Setup Wizard completion

### Weather

- Provider authentication
- Current conditions
- Seven-day forecast
- Fahrenheit and Celsius
- AQI and UV
- Dew point, pressure, wind, and precipitation
- Weather alerts
- Provider outage behavior

### Layouts and themes

- Weather Station
- Premium LCD Dark
- Premium LCD Light
- Theme Gallery
- Manual theme switching
- Automatic theme rotation
- Seasonal options
- Browser preview accuracy

### Astronomy

- Moon phase
- Realistic Moon rendering
- Sunrise and sunset
- Astronomy panels across layouts

### Hardware and services

- Physical display test
- Scheduled refresh
- Manual refresh
- Reboot recovery
- Network interruption
- Weather API interruption
- Daemon heartbeat
- Watchdog recovery
- Long-running memory and CPU behavior

## Minimum beta pass

A configuration qualifies as a successful beta pass when:

- Installation completes without undocumented manual repair.
- The Setup Wizard saves a working configuration.
- Both main layouts render in the browser.
- At least one layout refreshes successfully on the physical display.
- Units can be changed.
- Scheduled refresh survives a reboot.
- The system recovers after temporary network loss.
- The dashboard runs for 24 hours without a blocking failure.
