# Contributing to SpectraDash

Thank you for helping improve SpectraDash.

## Ways to contribute

- Report reproducible bugs
- Test new releases on Raspberry Pi hardware
- Submit hardware compatibility results
- Improve documentation
- Create themes and artwork packs
- Build plugins
- Add display profiles
- Review pull requests

## Before opening an issue

1. Search existing issues and discussions.
2. Confirm you are using the latest release or pre-release.
3. Perform a hard browser refresh after upgrading.
4. Reproduce the problem a second time when possible.
5. Export a Developer Mode support bundle.
6. Remove secrets and private information from logs.

## Pull request process

1. Fork the repository.
2. Create a focused branch from `main`.
3. Make the smallest practical change.
4. Add or update tests when behavior changes.
5. Update documentation and `CHANGELOG.md` when appropriate.
6. Run validation locally.
7. Open a pull request with clear testing notes.

Example branch names:

```text
fix/display-refresh-timeout
feature/new-weather-provider
docs/theme-sdk-example
```

## Coding expectations

- Support Python 3.10 or newer unless the project changes its baseline.
- Prefer clear, maintainable code over clever shortcuts.
- Keep hardware-specific behavior behind display or platform abstractions.
- Do not commit API keys, tokens, local configuration, logs, or private addresses.
- Preserve backward compatibility for documented configuration where practical.
- Include type hints for new public functions when reasonable.

## Visual changes

For layout, theme, and web-interface changes, include:

- Before and after screenshots
- Browser preview results
- Physical display results when hardware behavior is affected
- Notes about the target resolution and display profile

## Commit messages

Use concise, descriptive messages:

```text
Fix stale daemon heartbeat status
Add Spectra 6 display profile validation
Document theme manifest fields
```

## Community standards

Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
