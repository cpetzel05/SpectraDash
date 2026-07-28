# Hardware testing guide

## Safety first

Confirm the panel model, HAT/controller, cable orientation, and voltage before powering hardware. Do not assume two panels with the same diagonal size use the same driver.

## Test procedure

1. Install SpectraDash on a fresh supported Raspberry Pi OS image.
2. In Settings, select the exact display profile and leave **Send to physical display** disabled.
3. Refresh the software preview and verify orientation, legibility, colors, and clipping.
4. Open Developer Mode and run the weather/API test.
5. Run the hardware test pattern once.
6. Enable physical display output and perform at least ten scheduled refreshes.
7. Reboot and confirm both services restart automatically.
8. Export a support bundle and attach it to the hardware-test issue.

## Required report data

- Display product URL, exact model/revision, and controller/HAT.
- Raspberry Pi model and RAM.
- Raspberry Pi OS release and architecture.
- Photo of the rendered panel.
- `systemctl status` for web and daemon services.
- Daemon log covering a successful refresh.
- Any rotation, cable, GPIO, or driver-path changes.

A profile is promoted to verified only after repeatable physical results.
