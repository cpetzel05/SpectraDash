# Release Candidate Test Plan

## RC1 purpose

The release candidate is a feature-frozen build intended to prove that SpectraDash is ready for v1.0.0 Stable.

## Entry criteria

- No open beta blockers.
- Beta 2 has been publicly tested.
- Primary hardware passes the complete regression matrix.
- Upgrade from beta 1 and beta 2 succeeds.
- Known issues are documented.
- Installation and troubleshooting guides match actual behavior.
- Extension APIs are marked stable or provisional.

## Required RC tests

### Installation

- Fresh installation on the primary target
- Upgrade from beta 1
- Upgrade from beta 2
- Reinstall over an existing configuration
- Uninstall and reinstall where supported

### Reliability

- 72-hour continuous run
- Reboot during normal operation
- Power interruption recovery
- Network outage recovery
- Weather-provider outage recovery
- Scheduler restart
- Display worker restart

### Data correctness

- Fahrenheit
- Celsius
- Sunrise and sunset
- Moon phase
- Alert timestamps
- Forecast date boundaries
- Daylight-saving-time behavior when applicable

### User experience

- Setup Wizard
- Theme Gallery
- Developer Mode
- Browser preview
- Error messages
- Mobile browser access

## Exit criteria

- All required tests pass.
- No release-blocking regressions remain.
- No known data-loss issues.
- No unresolved secret-exposure issue.
- Documentation is complete enough for a new user to install without private assistance.
