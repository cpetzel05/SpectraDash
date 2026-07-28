# Display support

| Profile | Resolution | Palette | Status | Notes |
|---|---:|---|---|---|
| Waveshare 13.3-inch Spectra 6 (E) | 1600×1200 | 6-color | Verified | Tested on the project owner's EL133UF1 panel. |
| Waveshare 7.3-inch Spectra 6 (E) | 800×480 | 6-color | Experimental | Driver mapping and preview included; physical validation requested. |
| Waveshare 7.5-inch V2 | 800×480 | B/W | Experimental | Monochrome rendering included; hardware revision matters. |
| Waveshare 5.65-inch (F) | 600×448 | 7-color | Experimental | Preview and generic driver adapter included. |
| Waveshare 4.2-inch V2 | 400×300 | B/W | Experimental | Compact preview; physical refresh behavior unverified. |
| Generic preview | 1024×600 | 6-color simulation | Preview only | No hardware driver. |

“Experimental” means the profile can be selected, rendered, validated by tests, and mapped to a likely vendor driver. It does **not** mean it has been proven on physical hardware.

## Adding a profile

Edit `spectradash/display_profiles.py`. Profiles contain dimensions, palette, likely driver module, vendor repository path, layout density, and verification state. Run:

```bash
pytest -q
python scripts/render_previews.py
```

Then follow the evidence checklist in `docs/HARDWARE_TESTING.md`.
