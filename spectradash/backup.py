from __future__ import annotations
from pathlib import Path
from datetime import datetime
import json, shutil

def create_backup(config_path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / f"config-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    shutil.copy2(config_path, target)
    return target

def restore_backup(source: Path, config_path: Path) -> None:
    json.loads(source.read_text(encoding="utf-8"))
    shutil.copy2(source, config_path)
