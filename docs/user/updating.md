# Updating SpectraDash

## Before updating

- Read the release notes.
- Back up configuration and custom content.
- Export a support bundle if the current installation has unresolved problems.
- Confirm adequate disk space.

## Git-based update

```bash
cd ~/SpectraDash
git pull
sudo bash install.sh
```

## After updating

1. Reboot when instructed.
2. Perform a hard browser refresh.
3. Confirm the displayed version in Developer Mode.
4. Test the weather API.
5. Render a preview.
6. Confirm the physical display refreshes.

## Rollback

For public beta releases, keep a copy of the prior working release archive and configuration. Restore both together when configuration formats have changed.
