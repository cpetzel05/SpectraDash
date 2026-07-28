# 8.0 release checklist

## Automated

- [x] Python 3.13 local test suite passes.
- [x] Every profile renders at its declared native resolution.
- [x] Monochrome profiles contain only black and white output.
- [x] Hardware test patterns match profile dimensions.
- [x] Profile metadata API returns verified and experimental states.
- [x] Installer and Python source pass syntax checks.
- [ ] GitHub Actions passes on Python 3.11, 3.12, and 3.13 after repository publication.

## Verified 13.3-inch regression

- [ ] Upgrade an existing 7.3 installation and confirm settings remain intact.
- [ ] Refresh preview.
- [ ] Refresh physical display.
- [ ] Confirm 30-minute scheduling for 48 hours.
- [ ] Test reboot recovery.
- [ ] Test Developer Mode support bundle.
- [ ] Test plugin widgets and Screen Designer.

## Experimental hardware

Use the hardware-test issue template. No experimental display should be described as verified until the evidence requirements in `HARDWARE_TESTING.md` are met.
