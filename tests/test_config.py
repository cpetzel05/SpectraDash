from pathlib import Path
from spectradash.config import AppConfig, load_config, save_config

def test_round_trip(tmp_path: Path):
    path = tmp_path / "config.json"
    save_config(AppConfig(theme="ocean", display_profile="preview"), path)
    result = load_config(path)
    assert result.theme == "ocean"
    assert result.display_profile == "preview"
