## 8.0.0-rc19.2
- Bundled original photorealistic weather icons for HD+ across layouts using shared icon renderer.
- Default rendering quality set to HD+ for new installs. Existing saved settings remain unchanged.
- Classic artwork preserved as fallback.

## 8.0.0-rc19.0 — Spectra HD Graphics 2.0 pilot
- Supersampled weather icons, lunar contrast refinement, selective HD+ dithering, improved label fitting, and on-demand Graphics Lab.
- Preserves existing features and configuration.

## 8.0.0-rc18.9 — Optional browser radar pilot

- Opt-in browser radar map, with RainViewer overlay and OpenStreetMap base map.
- Lazy-loaded on button click; no display daemon or physical refresh changes.
- Provider failure messaging and NOAA radar fallback.

## 8.0.0-rc18.8 — Official alert details

- Added dedicated NWS alert details page in the web UI, with complete safety instructions and direct source links.
- Preserved RC18.7 display rendering and refresh behavior.

## 8.0.0-rc18.6 — Global Custom Quote Header

- Added a configurable custom quote/header ribbon across Weather Station, Forecast First, Minimal, Premium LCD, Premium HD, and Screen Designer layouts.
- Added fixed and rotating quote modes with up to 20 user messages.
- Added left/center/right alignment, small/medium/large sizing, bold text, optional quotation marks, and palette-safe accent selection.
- Added per-layout visibility controls.
- Added automatic font fitting and a collision-free inset composition so quotes cannot overlap weather content.
- Quote settings are included in configuration export/import and reset with normal display settings.

## 8.0.0-rc18.5 — Spectra HD Graphics

- Added new **Premium HD** flagship layout option without removing existing Weather Station or Premium LCD layouts.
- Added Standard, Spectra HD, and Spectra HD+ rendering quality modes.
- Added palette-aware contrast, sharpening, and edge preparation before six-color conversion.
- Added atmospheric condition accents for clear, night, rain, storm, and snow scenes.
- Added current-day high/low instrument.
- Added daylight progress arc with sunrise and sunset endpoints.
- Added 12-hour pressure trend sparkline.
- Added compact precipitation probability timeline.
- Preserved realistic Moon, premium illustrated icons, system-health footer, alerts, Screen Designer, and existing display profiles.
- Kept all new graphics optional so Pi Zero 2 W users can choose Standard or Lite rendering.

## 8.0.0-rc18.4 — Display Health & Visual Polish

- Unified Raspberry Pi health/status footer across Weather Station and Premium LCD e-paper layouts.
- Added GOOD / WARM / ATTENTION health badge based on CPU temperature, CPU load, RAM, and disk use.
- Added uptime to the e-paper status footer.
- Premium LCD now shows the same full CPU / temperature / RAM / disk health information as Weather Station.
- Preserved existing layout, forecast, alert, icon, and theme behavior.

# Changelog

## 8.0.0-rc18.3 — Phase 1 GitHub Polish

- Rebuilt the README with GitHub installation as the primary quick-start method.
- Added a project banner, badges, screenshots, documentation map, roadmap, and community testing guidance.
- Added user, installation, first-run, upgrade, uninstall, display, troubleshooting, developer, plugin, testing, and release documentation.
- Added test-pilot, showcase, compatibility, tested-hardware, known-issues, feature-request, roadmap, and release-checklist documents.
- Added structured GitHub issue templates and a pull-request template.
- Preserved the RC18.2 application code and behavior.

## 8.0.0-rc18.2

- Removed the preset Phoenix location from clean installations.
- Added first-run redirection and prevented weather refreshes until location setup is complete.
- Added configuration export, validated JSON import, reset-to-defaults, and factory reset.
- Added a safe uninstall script that preserves user data and the Waveshare driver unless explicitly requested.
- Added first-run, configuration-management, and uninstall documentation.

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

## 8.0.0-rc18.1

### Developer Mode hotfix
- Restored the full performance snapshot and runtime information alongside the temperature-unit selector.
- Added live five-second diagnostics updates for daemon health, refresh timing, CPU, memory, disk, temperature, host, theme, layout, and display profile.
- Improved unit selection feedback and responsive Developer Mode layout.
- Preserved the original test bench, logs, support bundle, and maintenance actions.

## 8.0.0-rc18

- Added the universal weather-alert ribbon to the Weather Station layout.
- Unified visibility controls for environmental data, AQI, graphs, astronomy, and system status.
- Added an optional Raspberry Pi health footer to Weather Station and Premium LCD layouts.
- Added a Developer Mode Fahrenheit/Celsius switch that saves the setting and queues a refresh.
- Preserved the shared realistic Moon renderer across all layouts.
