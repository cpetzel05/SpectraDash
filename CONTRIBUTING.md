# Contributing to SpectraDash

Thank you for helping improve SpectraDash. Hardware support must be evidence-based.

## Development setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pip install pytest
pytest -q
```

## Display contributions

A new or promoted display profile should include:

1. Exact manufacturer model and revision.
2. Native resolution, palette, orientation, and Waveshare driver module.
3. A software preview produced by `scripts/render_previews.py`.
4. Test results from `pytest -q`.
5. For “verified” status: a photo of the physical panel, daemon logs from a completed refresh, Raspberry Pi model, Raspberry Pi OS version, and any required wiring changes.

Do not mark a profile verified based only on matching dimensions or an importable driver.

## Pull requests

Keep changes focused, update documentation, and avoid committing `.venv`, caches, logs, configuration files, API tokens, or generated support bundles.
