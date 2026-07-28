# Developer Guide

## Local environment

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pip install pytest
pytest -q
python scripts/render_previews.py
```

## Contribution rules

- Start from the verified baseline.
- Keep one feature or fix per branch.
- Do not combine display-driver work with unrelated UI changes.
- Add or update tests.
- Render all software previews.
- Document rollback and compatibility impact.

See [ARCHITECTURE.md](ARCHITECTURE.md), [TESTING_GUIDE.md](TESTING_GUIDE.md), and [CONTRIBUTING.md](../CONTRIBUTING.md).
