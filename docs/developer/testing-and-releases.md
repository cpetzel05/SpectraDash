# Testing and Releases

## Local validation

```bash
python -m compileall -q .
python -m pytest -q
```

## Regression checklist

- Fresh install
- Upgrade from previous release
- Setup wizard
- Weather API test
- Weather Station preview
- Premium LCD preview
- Physical display test
- Alerts
- Fahrenheit and Celsius
- Theme switching
- Theme rotation
- Scheduler
- Watchdog
- Developer diagnostics
- Support bundle
- 24-hour stability run

## Release flow

```text
beta -> public testing -> release candidate -> stable
```

## Versioning

Use semantic versioning:

- Major: incompatible changes
- Minor: backward-compatible features
- Patch: backward-compatible fixes

## Release artifacts

A release should include:

- Source archive
- Installer package when applicable
- Release notes
- Checksums
- Upgrade notes
- Known issues
