from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
import time
from pathlib import Path
from PIL import Image

from spectradash.display import _candidate_roots
from spectradash.display_profiles import get_profile


def import_driver(profile_id: str):
    profile = get_profile(profile_id)
    if not profile.driver_module:
        raise RuntimeError(f"{profile.name} has no physical driver")
    errors = []
    for root in _candidate_roots(profile_id):
        for candidate in (root / "lib", root):
            value = str(candidate)
            if value not in sys.path:
                sys.path.insert(0, value)
        for name in (profile.driver_module, f"waveshare_epd.{profile.driver_module}"):
            try:
                return importlib.import_module(name)
            except Exception as exc:
                errors.append(f"{name} @ {root}: {exc}")
    raise RuntimeError("Could not import display driver. " + " | ".join(errors[-8:]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Standalone SpectraDash Waveshare display worker")
    parser.add_argument("image")
    parser.add_argument("--profile", default="waveshare-13in3e")
    args = parser.parse_args()
    profile = get_profile(args.profile)
    image = Image.open(args.image).convert("RGB")
    if image.size not in {profile.size, (profile.height, profile.width)}:
        raise ValueError(f"Expected {profile.size} (or rotated), got {image.size}")
    started = time.monotonic()
    module = import_driver(args.profile)
    epd = module.EPD()
    try:
        init = getattr(epd, "Init", None) or getattr(epd, "init", None)
        if not init:
            raise RuntimeError("Driver exposes neither Init() nor init()")
        init()
        packed = epd.getbuffer(image)
        epd.display(packed)
    finally:
        try:
            epd.sleep()
        except Exception as exc:
            print(f"Sleep warning: {exc}", flush=True)
    print("SPECTRADASH_RESULT=" + json.dumps({"ok": True, "profile": args.profile,
          "driver_file": str(getattr(module, "__file__", "unknown")), "image_size": f"{image.width}x{image.height}",
          "duration_seconds": round(time.monotonic() - started, 2), "worker_pid": os.getpid()}), flush=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
