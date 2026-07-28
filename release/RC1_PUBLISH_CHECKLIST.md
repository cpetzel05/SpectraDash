# RC1 Publish Checklist

## Code and versioning

- [ ] Application version is `v1.0.0-rc1`.
- [ ] Changelog contains an RC1 section.
- [ ] Installer references RC1.
- [ ] Upgrade logic recognizes beta 1 and beta 2.
- [ ] No debug-only code is enabled by default.
- [ ] No secrets or development credentials are committed.

## Testing

- [ ] Fresh installation passed.
- [ ] Upgrade from beta 1 passed.
- [ ] Upgrade from beta 2 passed.
- [ ] Weather Station passed.
- [ ] Premium LCD Dark passed.
- [ ] Premium LCD Light passed.
- [ ] Fahrenheit and Celsius passed.
- [ ] Alerts passed.
- [ ] Astronomy passed.
- [ ] Theme switching passed.
- [ ] Automatic theme rotation passed.
- [ ] Browser preview passed.
- [ ] Physical display refresh passed.
- [ ] Reboot recovery passed.
- [ ] Network recovery passed.
- [ ] 72-hour stability test passed.

## Documentation

- [ ] Installation guide matches the RC1 installer.
- [ ] Upgrade guide is tested.
- [ ] Troubleshooting commands are correct.
- [ ] Known issues are current.
- [ ] Hardware compatibility matrix is current.
- [ ] Release notes are complete.

## GitHub release

- [ ] Tag: `v1.0.0-rc1`
- [ ] Title: `SpectraDash v1.0.0-rc1`
- [ ] Marked as pre-release.
- [ ] Tested release archive attached.
- [ ] SHA-256 checksums attached.
- [ ] Release notes pasted.
- [ ] Public download tested while logged out.
