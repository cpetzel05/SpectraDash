# Stable Development Baseline

SpectraDash `8.0.0-rc18.1` is the current known-good baseline for continued development.

This release is preserved as the source of truth because its web interface, configuration flow, daemon architecture, display profiles, preview rendering, plugin system, diagnostics, and Waveshare 13.3-inch Spectra 6 integration were already working together as a complete application.

## Development rule

Future changes must be introduced in small, independently testable updates. Large replacement packages must not overwrite the application architecture in a single step.

Each change should:

1. Start from `8.0.0-rc18.1`.
2. Modify only the files required for one feature or bug fix.
3. Preserve the web service and refresh daemon.
4. Pass the existing test suite.
5. Include a rollback path.
6. Be tested in preview mode before physical display output.

## Recommended branches

- `main` — known-good release baseline
- `develop` — integration testing
- `feature/<name>` — one feature per branch

## Planned sequence

- `8.0.0-rc18.2` — stability and installer fixes only
- `8.0.0-rc18.3` — focused user-interface improvements
- `8.0.0-rc18.4` — focused weather-data improvements
- `8.0.0-rc19` — consolidated release-candidate validation
- `8.0.0` — stable release
