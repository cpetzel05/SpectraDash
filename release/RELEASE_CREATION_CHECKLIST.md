# Release Creation Checklist

## Before creating the release

- [ ] Confirm the release ZIP was physically tested.
- [ ] Confirm version strings say `v1.0.0-beta.1`.
- [ ] Update `CHANGELOG.md`.
- [ ] Update known issues.
- [ ] Verify installation documentation.
- [ ] Verify upgrade documentation.
- [ ] Verify no secrets or private data are committed.
- [ ] Run repository validation.
- [ ] Confirm the documentation site works while logged out.

## Create the GitHub release

- [ ] Tag: `v1.0.0-beta.1`
- [ ] Target: `main`
- [ ] Title: `SpectraDash v1.0.0-beta.1`
- [ ] Mark as **Pre-release**
- [ ] Attach the tested release ZIP
- [ ] Paste `RELEASE_NOTES_v1.0.0-beta.1.md`
- [ ] Verify the asset downloads
- [ ] Verify the tag and source archives

## After publishing

- [ ] Pin the release announcement Discussion.
- [ ] Update the README download link.
- [ ] Update the documentation download page.
- [ ] Test installation from the public release asset.
- [ ] Begin the launch-day checklist.
