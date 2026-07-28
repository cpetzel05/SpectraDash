from pathlib import Path
from spectradash.app import create_app
from spectradash.config import AppConfig, save_config

def test_dashboard(tmp_path: Path):
    path = tmp_path / "config.json"
    save_config(AppConfig(provider="mock"), path)
    client = create_app(path).test_client()
    assert client.get("/").status_code == 200
    assert client.get("/api/weather").get_json()["source"] == "Mock provider"
