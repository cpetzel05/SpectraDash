# Troubleshooting

## Website does not load

```bash
sudo systemctl status spectradash-web --no-pager
sudo journalctl -u spectradash-web -n 100 --no-pager
```

## Display does not refresh

```bash
sudo systemctl status spectradash-daemon --no-pager
sudo journalctl -u spectradash-daemon -n 150 --no-pager
```

Confirm SPI is enabled, the profile matches the panel, and the Waveshare repository was downloaded successfully.

## Weather is missing

Complete first-run setup, verify network access, and confirm the saved latitude and longitude.

## Recover from a bad setting

Import a known-good configuration, reset settings while preserving location, or use factory reset to restart setup.

## Create support evidence

Use Developer Mode to generate a redacted support bundle. Remove secrets and precise personal information before posting logs publicly.
