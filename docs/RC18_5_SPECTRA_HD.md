# RC18.5 — Spectra HD Graphics

This release adds a flagship graphics path while preserving the stable layouts.

## New rendering modes

- **Standard** — fastest preparation.
- **Spectra HD** — enhanced local contrast, edge clarity, premium icon details, and selective six-color dithering.
- **Spectra HD+** — maximum sharpening/detail preparation for the 1600×1200 panel.

## Premium HD layout

Choose **Settings → Layout → Premium HD flagship**. It builds on Premium LCD but automatically enables the premium icon treatment and HD graphics path.

## New instruments

- Current-day high/low
- Daylight progress arc
- 12-hour pressure trend sparkline
- Six-period precipitation timeline
- Weather-sensitive background accents

All instruments can be disabled independently in Settings.

## Pi Zero 2 W

The existing Lite performance mode is retained. If HD+ preparation feels slow, use **Spectra HD** or **Standard** while keeping the Premium HD layout. Physical e-paper refresh time is unchanged.

## Test checklist

1. Render Weather Station in Standard and HD.
2. Render Premium LCD Dark, Light, and Automatic.
3. Render Premium HD in HD and HD+.
4. Confirm alerts remain readable and override decorative content.
5. Confirm Moon, AQI, UV, system status, high/low, pressure, daylight, and precipitation graphics do not overlap.
6. Test on Pi 4 and Pi Zero 2 W before tagging the release.
