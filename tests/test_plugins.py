import json
from pathlib import Path

from spectradash import plugins


def test_manifest_and_discovery(tmp_path, monkeypatch):
    monkeypatch.setattr(plugins, "PLUGIN_DIR", tmp_path / "plugins")
    monkeypatch.setattr(plugins, "BUNDLED_PLUGIN_DIR", tmp_path / "bundled")
    folder = plugins.PLUGIN_DIR / "demo"
    folder.mkdir(parents=True)
    (folder / "manifest.json").write_text(json.dumps({"id":"demo","name":"Demo","entry":"plugin.py"}))
    (folder / "plugin.py").write_text("def render(image, box, context):\n    return None\n")
    found = plugins.discover_plugins()
    assert found[0].plugin_id == "plugin:demo"
    assert found[0].enabled is True


def test_rejects_unsafe_entry(tmp_path):
    folder = tmp_path / "bad"
    folder.mkdir()
    (folder / "manifest.json").write_text(json.dumps({"id":"bad","entry":"../bad.py"}))
    try:
        plugins._read_manifest(folder)
    except ValueError as exc:
        assert "entry" in str(exc).lower()
    else:
        raise AssertionError("unsafe entry was accepted")
