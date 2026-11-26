# RC18.9 — Optional browser radar pilot

- New `/weather-radar` page linked in the navigation.
- Off by default; enable under Settings > Information density > Optional browser weather radar.
- Map and radar are loaded **only after the user presses Load radar map**.
- Leaflet, OpenStreetMap tiles, and RainViewer's public radar API are loaded by the **browser**, not by the Pi's display daemon.
- Shows the most recent available historical radar frame and its timestamp; it is not real-time or predictive radar. Browser page reload is needed for new frames.
- No radar is drawn on the physical e-paper screen in this pilot. No change to existing display refresh, NWS alerts, or weather providers.
- The map providers receive map tile requests and the area viewed. Requires internet access; browser content blockers and third-party service changes may affect availability.
- If unavailable, the page provides a link to NOAA radar. Not an emergency alerting system.

## Test
1. Save Settings with radar disabled; confirm Radar page shows disabled and normal display refresh works.
2. Enable radar, save; open Radar and click Load radar map.
3. Verify the map centers on the configured location, radar tiles and timestamp appear, and zoom/pan work.
4. Confirm Weather Alerts, the dashboard, custom quotes, and physical refresh still function.
5. Disable radar again if desired. No background processing is added.

## Rollback
Restore RC18.8 files or use your saved Git commit. Existing config remains compatible (new flag is ignored by older builds).
