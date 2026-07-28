from pathlib import Path
from spectradash.config import AppConfig, load_config, save_config

def test_config_round_trip(tmp_path: Path):
    p = tmp_path / "config.json"
    save_config(AppConfig(theme="ocean", layout="premium-lcd"), p)
    loaded = load_config(p)
    assert loaded.theme == "ocean"
    assert loaded.layout == "premium-lcd"
