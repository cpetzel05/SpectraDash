from pathlib import Path
from spectradash.config import load_config
from spectradash.display.factory import create_display
from spectradash.providers.weather import fetch_weather
from spectradash.rendering.dashboard import render_dashboard

PREVIEW_PATH = Path("/var/lib/spectradash/preview.png")

def render_and_show(force_profile: str | None = None) -> Path:
    config = load_config()
    weather = fetch_weather(config)
    render_dashboard(weather, PREVIEW_PATH, config.theme, config.layout)
    display = create_display(force_profile or config.display_profile)
    display.show(PREVIEW_PATH)
    return PREVIEW_PATH
