from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from threading import Lock
from typing import Any

from PIL import Image, ImageDraw, ImageFont

from .display_profiles import DEFAULT_PROFILE_ID, get_profile

DISPLAY_LOCK = Lock()
DRIVER_REPO = Path(os.environ.get("WAVESHARE_REPO", "/opt/waveshare-e-paper"))


def image_sha256(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGB").tobytes()).hexdigest()


def _candidate_roots(profile_id: str) -> list[Path]:
    profile = get_profile(profile_id)
    roots: list[Path] = []
    override = os.environ.get("WAVESHARE_PYTHON")
    if override:
        roots.append(Path(override))
    if profile.driver_root:
        roots.append(DRIVER_REPO / profile.driver_root)
        roots.append(DRIVER_REPO / "E-paper_Separate_Program" / profile.driver_root)
    roots.extend([
        DRIVER_REPO / "RaspberryPi_JetsonNano/python",
        DRIVER_REPO / "E-paper_Separate_Program/13.3inch_e-Paper_E/RaspberryPi/python",
    ])
    return list(dict.fromkeys(roots))


def driver_diagnostics(profile_id: str = DEFAULT_PROFILE_ID) -> dict[str, Any]:
    profile = get_profile(profile_id)
    result: dict[str, Any] = {"profile": profile.to_dict(), "candidate_roots": [str(p) for p in _candidate_roots(profile_id)]}
    if not profile.driver_module:
        result.update({"import_ok": False, "preview_only": True, "import_error": "This profile has no physical driver."})
        return result
    found = []
    for root in _candidate_roots(profile_id):
        for candidate in (root / "lib" / f"{profile.driver_module}.py", root / "waveshare_epd" / f"{profile.driver_module}.py", root / f"{profile.driver_module}.py"):
            if candidate.exists():
                found.append(str(candidate))
    result["driver_candidates"] = found
    result["import_ok"] = bool(found)
    if not found:
        result["import_error"] = f"Could not find {profile.driver_module}.py in the Waveshare repository."
    return result


def prepare_for_driver(image: Image.Image, profile_id: str = DEFAULT_PROFILE_ID, rotation: int = 0) -> Image.Image:
    profile = get_profile(profile_id)
    prepared = image.convert("RGB")
    expected = profile.size if rotation in {0, 180} else (profile.height, profile.width)
    if prepared.size != expected:
        raise ValueError(f"Display image is {prepared.width}x{prepared.height}; expected {expected[0]}x{expected[1]} for {profile.name}.")
    return prepared


def send_to_display(image: Image.Image, *, profile_id: str = DEFAULT_PROFILE_ID, rotation: int = 0, clear_first: bool = False) -> dict[str, Any]:
    profile = get_profile(profile_id)
    if not profile.driver_module:
        raise RuntimeError(f"{profile.name} is preview-only and cannot write to physical hardware.")
    started = time.monotonic()
    with DISPLAY_LOCK:
        prepared = prepare_for_driver(image, profile_id, rotation)
        worker = Path(__file__).with_name("hardware_worker.py")
        with tempfile.NamedTemporaryFile(prefix="spectradash-panel-", suffix=".png", delete=False) as handle:
            temp_path = Path(handle.name)
        try:
            prepared.save(temp_path, "PNG")
            # Launch the worker as a package module rather than as a file path.
            # Direct file execution sets sys.path[0] to spectradash/, which can make
            # absolute imports such as ``import spectradash`` fail on fresh installs.
            completed = subprocess.run(
                [sys.executable, "-m", "spectradash.hardware_worker", str(temp_path), "--profile", profile_id],
                cwd=str(worker.parent.parent), env=os.environ.copy(), text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900, check=False,
            )
            output = completed.stdout or ""
            if completed.returncode != 0:
                raise RuntimeError(f"Standalone display worker failed ({completed.returncode}). Output: {output[-4000:]}")
            worker_result: dict[str, Any] = {}
            for line in output.splitlines():
                if line.startswith("SPECTRADASH_RESULT="):
                    worker_result = json.loads(line.split("=", 1)[1])
            return {**worker_result, "profile_id": profile_id, "sha256": image_sha256(prepared),
                    "duration_seconds": round(time.monotonic() - started, 2), "clear_first_requested": clear_first,
                    "worker_output": output[-4000:]}
        finally:
            temp_path.unlink(missing_ok=True)


def make_hardware_test_pattern(profile_id: str = DEFAULT_PROFILE_ID) -> Image.Image:
    profile = get_profile(profile_id)
    image = Image.new("RGB", profile.size, "white")
    draw = ImageDraw.Draw(image)
    palette = {"black": (0,0,0), "white": (255,255,255), "yellow": (255,255,0), "red": (255,0,0), "blue": (0,0,255), "green": (0,180,0), "orange": (255,128,0)}
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", max(18, profile.height // 18))
        body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", max(13, profile.height // 30))
    except OSError:
        title_font = body_font = ImageFont.load_default()
    colors = list(profile.colors)
    band_h = max(1, int(profile.height * 0.72 / len(colors)))
    for index, name in enumerate(colors):
        y1, y2 = index * band_h, (index + 1) * band_h
        draw.rectangle((0, y1, profile.width, y2), fill=palette[name])
        draw.text((profile.width // 2, (y1 + y2) // 2), name.upper(), fill="white" if name in {"black","red","blue","green"} else "black", font=title_font, anchor="mm")
    draw.text((profile.width // 2, int(profile.height * .83)), "SpectraDash hardware test", fill="black", font=title_font, anchor="mm")
    draw.text((profile.width // 2, int(profile.height * .91)), f"{profile.name} · {profile.width} x {profile.height}", fill="black", font=body_font, anchor="mm")
    return image
