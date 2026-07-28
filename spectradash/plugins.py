from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

from PIL import Image, ImageDraw

from .config import DATA_DIR

PLUGIN_DIR = DATA_DIR / "plugins"
BUNDLED_PLUGIN_DIR = Path(__file__).resolve().parent.parent / "bundled_plugins"
PLUGIN_ID_PREFIX = "plugin:"


@dataclass(frozen=True)
class PluginInfo:
    plugin_id: str
    name: str
    version: str
    description: str
    author: str
    widget_name: str
    default_size: tuple[int, int]
    path: Path
    enabled: bool
    module_name: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.plugin_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "widget_name": self.widget_name,
            "default_size": list(self.default_size),
            "enabled": self.enabled,
        }


def ensure_plugin_dirs() -> None:
    PLUGIN_DIR.mkdir(parents=True, exist_ok=True)
    if BUNDLED_PLUGIN_DIR.exists():
        for source in BUNDLED_PLUGIN_DIR.iterdir():
            if source.is_dir() and (source / "manifest.json").exists():
                target = PLUGIN_DIR / source.name
                if not target.exists():
                    shutil.copytree(source, target)


def _safe_id(value: str) -> str:
    cleaned = "".join(ch for ch in value.lower() if ch.isalnum() or ch in "-_").strip("-_")
    if not cleaned:
        raise ValueError("Plugin id is missing or invalid.")
    return cleaned[:64]


def _read_manifest(path: Path) -> PluginInfo:
    raw = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("manifest.json must contain an object.")
    short_id = _safe_id(str(raw.get("id", path.name)))
    entry = str(raw.get("entry", "plugin.py"))
    if Path(entry).name != entry or not entry.endswith(".py"):
        raise ValueError("Plugin entry must be a Python file in the plugin folder.")
    if not (path / entry).is_file():
        raise ValueError(f"Plugin entry file {entry} was not found.")
    size = raw.get("default_size", [4, 3])
    try:
        w = max(2, min(12, int(size[0])))
        h = max(2, min(12, int(size[1])))
    except (TypeError, ValueError, IndexError):
        w, h = 4, 3
    enabled_file = path / ".disabled"
    return PluginInfo(
        plugin_id=PLUGIN_ID_PREFIX + short_id,
        name=str(raw.get("name", short_id)).strip()[:80],
        version=str(raw.get("version", "1.0.0")).strip()[:24],
        description=str(raw.get("description", "")).strip()[:240],
        author=str(raw.get("author", "Unknown")).strip()[:80],
        widget_name=str(raw.get("widget_name", raw.get("name", short_id))).strip()[:80],
        default_size=(w, h),
        path=path,
        enabled=not enabled_file.exists(),
        module_name=entry,
    )


def discover_plugins(*, include_disabled: bool = True) -> list[PluginInfo]:
    ensure_plugin_dirs()
    found: list[PluginInfo] = []
    for path in sorted(PLUGIN_DIR.iterdir()):
        if not path.is_dir() or not (path / "manifest.json").exists():
            continue
        try:
            info = _read_manifest(path)
        except Exception:
            continue
        if include_disabled or info.enabled:
            found.append(info)
    return found


def plugin_map() -> dict[str, PluginInfo]:
    return {plugin.plugin_id: plugin for plugin in discover_plugins(include_disabled=False)}


def _load_module(info: PluginInfo) -> ModuleType:
    module_path = info.path / info.module_name
    unique = f"spectradash_user_plugin_{info.plugin_id.replace(':', '_').replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(unique, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load plugin module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[unique] = module
    spec.loader.exec_module(module)
    return module


def render_plugin(plugin_id: str, image: Image.Image, box: tuple[int, int, int, int], context: dict[str, Any]) -> None:
    info = plugin_map().get(plugin_id)
    draw = ImageDraw.Draw(image)
    if info is None:
        draw.rectangle(box, outline=(0, 0, 0), width=3)
        draw.text((box[0] + 12, box[1] + 12), "Plugin unavailable", fill=(0, 0, 0))
        return
    try:
        module = _load_module(info)
        renderer = getattr(module, "render", None)
        if not callable(renderer):
            raise RuntimeError("Plugin does not provide render(image, box, context).")
        renderer(image, box, context)
    except Exception as exc:
        draw.rounded_rectangle(box, radius=18, fill=(255, 255, 255), outline=(255, 0, 0), width=4)
        draw.text((box[0] + 14, box[1] + 14), info.widget_name, fill=(255, 0, 0))
        draw.text((box[0] + 14, box[1] + 45), f"Plugin error: {str(exc)[:90]}", fill=(0, 0, 0))


def install_plugin_zip(upload_path: Path) -> PluginInfo:
    ensure_plugin_dirs()
    if not zipfile.is_zipfile(upload_path):
        raise ValueError("The uploaded file is not a valid ZIP archive.")
    with tempfile.TemporaryDirectory(prefix="spectradash-plugin-") as tmp_name:
        tmp = Path(tmp_name)
        with zipfile.ZipFile(upload_path) as archive:
            for member in archive.infolist():
                destination = (tmp / member.filename).resolve()
                if tmp.resolve() not in destination.parents and destination != tmp.resolve():
                    raise ValueError("Plugin archive contains an unsafe path.")
                if member.file_size > 5 * 1024 * 1024:
                    raise ValueError("A file in the plugin archive is too large.")
            archive.extractall(tmp)
        roots = [p for p in tmp.iterdir() if p.is_dir()]
        candidate = tmp if (tmp / "manifest.json").exists() else (roots[0] if len(roots) == 1 else None)
        if candidate is None or not (candidate / "manifest.json").exists():
            raise ValueError("Plugin ZIP must contain manifest.json and its entry file.")
        info = _read_manifest(candidate)
        target = PLUGIN_DIR / info.plugin_id.removeprefix(PLUGIN_ID_PREFIX)
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(candidate, target)
    return _read_manifest(target)


def set_plugin_enabled(plugin_id: str, enabled: bool) -> PluginInfo:
    short_id = _safe_id(plugin_id.removeprefix(PLUGIN_ID_PREFIX))
    path = PLUGIN_DIR / short_id
    info = _read_manifest(path)
    marker = path / ".disabled"
    if enabled:
        marker.unlink(missing_ok=True)
    else:
        marker.touch()
    return _read_manifest(path)


def remove_plugin(plugin_id: str) -> None:
    short_id = _safe_id(plugin_id.removeprefix(PLUGIN_ID_PREFIX))
    path = PLUGIN_DIR / short_id
    if not path.exists():
        raise FileNotFoundError("Plugin not found.")
    shutil.rmtree(path)
