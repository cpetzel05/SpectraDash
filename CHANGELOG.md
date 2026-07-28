## 8.0.0-rc17

- Added visual Theme Gallery and community theme-pack foundation.
- Added browser-only animated Weather Studio preview.
- Added astronomy details, local condition alert banners, graph/gauge style controls.
- Added nine background scene choices and automatic/manual seasonal modes.
- Added a guided first-run setup wizard.
- Added bundled NOAA, Aviation, Marine, Retro CRT, Modern Glass, and Seasonal theme manifests.

# Changelog

## 8.0.0-rc16

- Added a universal high-detail procedural lunar texture shared by Premium LCD and Weather Station layouts.
- Replaced the earlier simple crater pattern with irregular maria, multi-scale terrain, ray craters, and dense micro-cratering.
- Applied phase-accurate curved illumination, soft terminators, limb darkening, and subtle earthshine to the shared texture.
- Kept the Moon strictly neutral grayscale through black-and-white dithering for reliable Spectra 6 output.
- Used original procedural artwork instead of embedding an image with unknown redistribution rights.

## 8.0.0-rc15

- Reworked the Premium LCD moon as a neutral grayscale illustration.
- Added physically curved waxing and waning phase shading.
- Added monochrome maria, crater rims, limb shading, and subtle earthshine.
- Uses black-and-white dithering only, eliminating multicolor lunar pixels.

## 8.0.0-rc13

- Fixed Premium LCD air-quality text overlap by placing the section title, AQI value, and condition label on three separate rows.

- Added **Dark**, **Light**, and **Automatic** appearance modes for the Premium LCD-inspired layout.
- Automatic mode follows the weather provider day/night state at each scheduled refresh.
- Added light-mode-specific borders, text, temperature accents, Moon outlines, and forecast-card contrast.
- Added separate release previews for Premium LCD Light and Dark.

# Changelog

## 8.0.0-rc10

- Added a selectable **Premium LCD-inspired** dashboard layout.
- Added a dark, high-contrast instrument panel with a large current-condition scene.
- Added a dedicated information panel with wind compass, dew point, precipitation, and air quality.
- Added seven tall premium forecast cards with gold high temperatures, blue lows, and detailed weather art.
- Preserved the existing Weather Station, Forecast First, Minimal, and Screen Designer layouts.


## 8.0.0-rc9

- Reworked the Premium weather artwork to use dense layered clouds, sculpted highlights, deeper undersides, and deterministic texture.
- Added finer multi-length sun rays, denser tapered rainfall, and more detailed snowfall for an LCD weather-station look.
- Kept all artwork original and optimized for the six-colour Spectra e-paper palette.

## 8.0.0-rc7

- Rounded the top corners of every seven-day forecast header so the colored day/date band follows the card shape instead of bleeding into the outer rounded corners.
- Preserved a clean square divider at the bottom of the header for a unified premium card appearance.
- Kept the TODAY accent border aligned with the same card radius.


## 8.0.0-rc6

- Reduced sun-ray length in seven-day forecast icons to prevent the artwork from touching or overlapping card headers.
- Preserved the larger sun artwork in the current-conditions panel.

## 8.0.0-rc5

- Added a configurable first-card label: **Today** or the weekday name.
- Made **Today** the default for clearer rolling seven-day forecasts.
- Added a subtle accent outline around the current-day card.
- Added regression tests for both first-card label modes.

## 8.0.0-rc4

- Raised seven-day forecast weather artwork by 24 pixels.
- Reduced forecast icon canvas height slightly so rain, snow, and storm details remain clear of the high/low temperature row.
- Applied the spacing correction to expanded, compact, automatic, and no-date layouts.

## 8.0.0-rc3

- Added configurable forecast date labels: Automatic, Expanded, Compact, and Off.
- Added an optional forecast freshness timestamp.
- Automatic date labels adapt to display profile size and layout density.
- Added regression coverage for the new settings and renderer helpers.
- Kept the rolling seven-day forecast in chronological order so Today always appears first.

## 8.0.0-rc2

- Fixed physical display refreshes on fresh installations by launching the hardware worker with `python -m spectradash.hardware_worker`.
- Added installer import and worker-launch self-tests before services are enabled.
- Added regression coverage for the packaged hardware-worker command.

## 8.0.0-rc1

- Added a data-driven display profile registry.
- Preserved verified 13.3-inch Spectra 6 support.
- Added experimental software profiles for 7.3-inch Spectra 6, 7.5-inch B/W V2, 5.65-inch seven-color, and 4.2-inch B/W V2.
- Added generic physical-driver loading and profile-aware diagnostics.
- Added resolution-independent rendering output and profile palette conversion.
- Added display selection and density controls to Settings.
- Added profile API, automated profile tests, preview generator, CI, contribution guide, hardware test matrix, and GitHub issue templates.
- Removed generated caches from the release package.
