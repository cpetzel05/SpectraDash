# RC18.4 Display Health & Visual Polish

This update intentionally changes only the e-paper renderer and system-information helper.

## Fixed

The optional Raspberry Pi status footer is now visually and functionally consistent in both:

- Weather Station
- Premium LCD

When **Settings → Raspberry Pi system status** is enabled, both layouts show:

- Health badge: GOOD, WARM, or ATTENTION
- CPU load
- CPU temperature
- RAM usage
- Disk usage
- Uptime
- Last updated time
- Active layout / Premium LCD mode

## Health thresholds

**GOOD** — normal operating range.

**WARM** — CPU temperature ≥ 70°C, CPU load ≥ 90%, RAM ≥ 85%, or disk ≥ 90%.

**ATTENTION** — CPU temperature ≥ 80°C, RAM ≥ 95%, or disk ≥ 98%.

These are dashboard indicators, not hardware-failure diagnostics.

## Test checklist

1. Enable **Raspberry Pi system status** in Settings.
2. Render Weather Station preview.
3. Confirm the footer is present and readable.
4. Switch to Premium LCD Dark and render.
5. Switch to Premium LCD Light and render.
6. Confirm all three show the same Pi health metrics.
7. Refresh the physical e-paper display.
8. Confirm the footer remains fully inside the 1600×1200 canvas.
