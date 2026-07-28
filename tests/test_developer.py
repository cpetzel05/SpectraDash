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
