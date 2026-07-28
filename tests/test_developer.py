import os
os.environ.setdefault("SPECTRADASH_DATA_DIR", "/tmp/spectradash-test-developer")
from spectradash.app import create_app
from spectradash.config import load_config, save_config

def test_developer_disabled_redirects():
    cfg=load_config(); cfg["developer_mode"]=False; save_config(cfg)
    client=create_app().test_client()
    assert client.get("/developer").status_code==302

def test_developer_logs_when_enabled():
    cfg=load_config(); cfg["developer_mode"]=True; save_config(cfg)
    client=create_app().test_client()
    assert client.get("/developer").status_code==200
    assert client.get("/api/developer/logs").status_code==200

def test_developer_page_keeps_diagnostics_and_units():
    cfg=load_config(); cfg["developer_mode"]=True; save_config(cfg)
    client=app.test_client()
    response=client.get("/developer")
    assert response.status_code==200
    body=response.get_data(as_text=True)
    assert "Performance snapshot" in body
    assert "Runtime information" in body
    assert "Units &amp; localization" in body or "Units & localization" in body
    assert "Test bench" in body
    assert "Application log" in body


def test_developer_live_status_when_enabled():
    cfg=load_config(); cfg["developer_mode"]=True; save_config(cfg)
    client=app.test_client()
    response=client.get("/api/developer/status")
    assert response.status_code==200
    payload=response.get_json()
    assert payload["ok"] is True
    assert "system" in payload
    assert "daemon" in payload
    assert "status" in payload
