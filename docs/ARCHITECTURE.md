# Architecture

SpectraDash separates the web interface from display scheduling:

- `spectradash-web.service`: Flask/Gunicorn settings, designer, plugins, diagnostics, and developer tools.
- `spectradash-daemon.service`: scheduling, weather retrieval, rendering, retries, and physical display writes.
- `display_profiles.py`: immutable hardware capabilities and verification state.
- `render.py`: canonical 1600×1200 composition, resolution scaling, and palette conversion.
- `display.py`: profile-aware diagnostics and isolated hardware-worker invocation.
- `hardware_worker.py`: imports the selected vendor driver and owns SPI/GPIO access for one update.

The canonical renderer keeps layouts stable while profile output is tested. Future profile-specific renderers can replace conservative scaling without changing the scheduler or driver interface.
