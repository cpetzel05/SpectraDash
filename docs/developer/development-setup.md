# Development Setup

## Requirements

- Python 3.10 or newer
- Git
- A virtual environment
- Development dependencies

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/SpectraDash.git
cd SpectraDash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
```

## Run tests

```bash
python -m pytest -q
```

## Compile check

```bash
python -m compileall -q .
```

## Browser-only development

Use a mock or development display profile when physical hardware is not connected. Hardware drivers should not prevent the web application from starting in development mode.

## Secrets

Store development credentials in ignored local configuration or environment variables. Never commit them.
