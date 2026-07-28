import io
import json

import spectradash.app as app_module
from spectradash.config import default_config


def test_dashboard_redirects_to_setup(monkeypatch):
    monkeypatch.setattr(app_module, "load_config", default_config)
    client = app_module.create_app().test_client()
    response = client.get("/")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/setup")


def test_import_rejects_unknown_keys(monkeypatch):
    monkeypatch.setattr(app_module, "load_config", default_config)
    client = app_module.create_app().test_client()
    response = client.post(
        "/settings/import",
        data={"settings_file": (io.BytesIO(json.dumps({"bad_key": True}).encode()), "settings.json")},
        content_type="multipart/form-data",
    )
    assert response.status_code == 302
    assert "Import" in response.headers["Location"]
