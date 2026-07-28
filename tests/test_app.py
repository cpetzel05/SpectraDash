from pathlib import Path
from spectradash.app import create_app
from spectradash.config import AppConfig, save_config

def test_dashboard(tmp_path: Path):
    p = tmp_path / "config.json"
    save_config(AppConfig(provider="mock"), p)
    client = create_app(p).test_client()
    assert client.get("/").status_code == 200
    assert client.get("/api/weather").status_code == 200
    assert client.get("/diagnostics").status_code == 200
