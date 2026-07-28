from __future__ import annotations
import json, os
from dataclasses import dataclass, asdict
from pathlib import Path

DEFAULT_PATH = Path(os.environ.get("SPECTRADASH_CONFIG", "/etc/spectradash/config.json"))

@dataclass
class AppConfig:
    provider: str = "mock"
    latitude: float = 40.7128
    longitude: float = -74.0060
    location_name: str = "New York"
    units: str = "imperial"
    refresh_minutes: int = 15
    display_profile: str = "preview"
    bind_host: str = "0.0.0.0"
    bind_port: int = 8080

def load_config(path: Path | None = None) -> AppConfig:
    target = path or DEFAULT_PATH
    if not target.exists():
        return AppConfig()
    data = json.loads(target.read_text(encoding="utf-8"))
    allowed = asdict(AppConfig())
    return AppConfig(**{k: data[k] for k in allowed if k in data})

def save_config(config: AppConfig, path: Path | None = None) -> None:
    target = path or DEFAULT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(asdict(config), indent=2) + "\n", encoding="utf-8")
