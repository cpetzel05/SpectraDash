# Development Baseline

All future SpectraDash application work must begin from the known-good `v1.0.0-rc1` application code.

Large replacement packages should not be merged directly into `main`.

## Required branches

- `main` — known-good release baseline
- `develop` — integration branch
- `feature/<name>` — one feature per branch

## Merge requirements

A feature must demonstrate:

- Successful application startup
- Working dashboard
- Successful configuration save
- Clean service restart
- No regression in existing weather data
- Clear rollback instructions
