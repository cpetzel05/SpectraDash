# Testing Guide

## Automated tests

```bash
pytest -q
```

## Preview tests

```bash
python scripts/render_previews.py
```

Check every output for clipping, overlapping text, incorrect palette conversion, and unreadable type.

## Hardware tests

Follow [HARDWARE_TESTING.md](HARDWARE_TESTING.md). Record the exact panel, Pi model, OS, refresh time, orientation, colors, artifacts, and logs.
