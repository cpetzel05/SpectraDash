from __future__ import annotations
import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path

CONFIG_PATH = Path(os.environ.get("SPECTRADASH_CONFIG", "/etc/spectradash/config.json"))

@dataclass
class AppConfig:
    provider: str = "open-meteo"
    location_query: str = "85050"
    location_name: str = "Phoenix, Arizona"
    latitude: float = 33.683
    longitude: float = -111.978
    units: str = "imperial"
    layout: str = "weather-station"
    theme: str = "desert"
    display_profile: str = "preview"
    refresh_minutes: int = 30
    auto_refresh: bool = True
    bind_host: str = "0.0.0.0"
    bind_port: int = 8080

def load_config(path: Path | None = None) -> AppConfig:
    target = path or CONFIG_PATH
    if not target.exists():
        return AppConfig()
    data = json.loads(target.read_text(encoding="utf-8"))
    allowed = asdict(AppConfig())
    return AppConfig(**{k: data[k] for k in allowed if k in data})

def save_config(config: AppConfig, path: Path | None = None) -> None:
    target = path or CONFIG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(".tmp")
    tmp.write_text(json.dumps(asdict(config), indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, target)
