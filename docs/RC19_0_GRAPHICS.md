# RC19.0 — Spectra HD Graphics 2.0 (pilot)

- Standard: original native-resolution icon renderer and palette quantizer.
- HD: 2× supersampled icon artwork, improved lunar contrast, existing edge enhancement.
- HD+: 3× supersampled icon artwork, enhanced lunar contrast, and selective dithering that avoids speckling flat panels.
- Graphics Lab: browser-only, on-demand side-by-side previews from a single weather fetch. Never triggers physical panel writes or saves settings.
- Typography: long fitted labels now shrink to 14 pt and gracefully ellipsize instead of disappearing. Existing layout geometry, alerts, radar, and custom quotes retained.

## Validation
1. Export configuration from Settings before installing.
2. Install the patch, open Graphics Lab, and click Generate three previews.
3. Compare image details and render times. HD+ may be noticeably slower on Pi Zero 2 W.
4. Select desired quality in Settings and run a normal preview before writing to the panel.
5. If graphics are slow, select Standard or Lite performance mode.

Pilot limitations: no on-panel testing here; image quality depends on actual six-ink panel behavior. The graphics lab makes three large in-memory images, so avoid using it repeatedly on memory-limited boards.
