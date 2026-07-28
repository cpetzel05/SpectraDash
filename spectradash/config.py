from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from threading import RLock
from typing import Any

DATA_DIR = Path(os.environ.get("SPECTRADASH_DATA_DIR", "/var/lib/spectradash"))
CONFIG_PATH = DATA_DIR / "config.json"
STATUS_PATH = DATA_DIR / "status.json"
PREVIEW_PATH = DATA_DIR / "current_display.png"
UPLOAD_DIR = DATA_DIR / "uploads"
LOG_PATH = DATA_DIR / "spectradash.log"

DEFAULT_CONFIG: dict[str, Any] = {
    "location_name": "Phoenix, Arizona",
    "latitude": 33.4484,
    "longitude": -112.0740,
    "timezone": "auto",
    "units": "fahrenheit",
    "wind_units": "mph",
    "rotation": 0,
    "display_profile": "waveshare-13in3e",
    "layout_density": "auto",
    "refresh_minutes": 45,
    "physical_display": False,
    "theme": "sunrise",
    "auto_rotate_theme": False,
    "show_hourly": True,
    "show_air_quality": True,
    "show_moon": True,
    "show_sun_times": True,
    "show_environment": True,
    "show_hourly_graph": True,
    "first_day_of_week": "sunday",
    "forecast_date_style": "auto",
    "forecast_first_day_label": "today",
    "show_forecast_updated": True,
    "hourly_hours": 24,
    "show_weather_summary": True,
    "layout_preset": "weather-station",
    "premium_lcd_mode": "dark",
    "auto_day_night": True,
    "display_mode": "weather",
    "custom_title": "SpectraDash",
    "weather_provider": "open-meteo",
    "living_scene": True,
    "scene_style": "landscape",
    "theme_gallery": True,
    "studio_animations": True,
    "show_weather_alerts": True,
    "show_astronomy_details": True,
    "show_system_status": False,
    "graph_style": "premium",
    "gauge_style": "premium",
    "seasonal_mode": "automatic",
    "setup_complete": False,
    "animation_frames": 4,
    "icon_style": "premium",
    "enable_3d_icons": True,
    "icon_shadows": True,
    "icon_highlights": True,
    "scene_details": True,
    "seasonal_details": True,
    "living_details": True,
    "rainbow_effects": True,
    "performance_mode": "auto",
    "lite_disable_animations": True,
    "lite_cache_icons": True,
    "lite_reduced_dither": True,
    "designer_enabled": False,
    "developer_mode": False,
    "designer_layout": [
        {"id":"current","x":0,"y":0,"w":6,"h":4,"enabled":True},
        {"id":"metrics","x":6,"y":0,"w":6,"h":4,"enabled":True},
        {"id":"hourly","x":0,"y":4,"w":8,"h":3,"enabled":True},
        {"id":"sunmoon","x":8,"y":4,"w":4,"h":3,"enabled":True},
        {"id":"forecast","x":0,"y":7,"w":12,"h":5,"enabled":True}
    ],
}

_lock = RLock()


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _atomic_write(path: Path, payload: dict[str, Any]) -> None:
    ensure_dirs()
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8") as tmp:
        json.dump(payload, tmp, indent=2, sort_keys=True)
        tmp.flush()
        os.fsync(tmp.fileno())
        tmp_name = tmp.name
    os.replace(tmp_name, path)


def load_config() -> dict[str, Any]:
    ensure_dirs()
    with _lock:
        if not CONFIG_PATH.exists():
            _atomic_write(CONFIG_PATH, DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
        try:
            raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            raw = {}
        merged = DEFAULT_CONFIG.copy()
        merged.update(raw if isinstance(raw, dict) else {})
        return merged


def save_config(config: dict[str, Any]) -> None:
    with _lock:
        merged = DEFAULT_CONFIG.copy()
        merged.update(config)
        _atomic_write(CONFIG_PATH, merged)


def load_status() -> dict[str, Any]:
    ensure_dirs()
    with _lock:
        if not STATUS_PATH.exists():
            return {"state": "idle", "message": "Ready", "last_refresh": None, "last_error": None}
        try:
            data = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {"state": "unknown", "message": "Status unavailable"}


def save_status(**updates: Any) -> dict[str, Any]:
    with _lock:
        status = load_status()
        status.update(updates)
        _atomic_write(STATUS_PATH, status)
        return status

COMMAND_PATH = DATA_DIR / "daemon-command.json"
