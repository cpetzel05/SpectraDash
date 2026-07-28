from __future__ import annotations

import logging
import threading
import time
from datetime import datetime, timedelta
from typing import Any

from .config import PREVIEW_PATH, load_config, load_status, save_status
from .display import make_hardware_test_pattern, send_to_display
from .render import THEMES, render_error, render_weather, rotate_for_panel
from .weather import fetch_weather

log = logging.getLogger("spectradash.refresh")
_refresh_lock = threading.Lock()


def iso_now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def next_refresh_iso(minutes: int) -> str:
    return (datetime.now() + timedelta(minutes=minutes)).isoformat(timespec="seconds")


def theme_for_refresh(config: dict[str, Any]) -> tuple[dict[str, Any], str]:
    selected = str(config.get("theme", "sunrise"))
    if selected not in THEMES:
        selected = "sunrise"
    if not config.get("auto_rotate_theme", False):
        effective = config.copy(); effective["theme"] = selected
        return effective, selected
    order = list(THEMES)
    previous = str(load_status().get("active_theme") or "")
    try:
        selected = order[(order.index(previous) + 1) % len(order)] if previous else selected
    except ValueError:
        pass
    effective = config.copy(); effective["theme"] = selected
    return effective, selected


def refresh_display(reason: str = "schedule", *, force_physical: bool = False, test_pattern: bool = False) -> dict[str, Any]:
    if not _refresh_lock.acquire(blocking=False):
        log.warning("Refresh skipped: another refresh is already running")
        save_status(last_skipped_refresh=iso_now(), last_skip_reason="A refresh is already running")
        return {"ok": False, "message": "A refresh is already running.", "skipped": True}
    started = time.monotonic()
    started_at = iso_now()
    try:
        config = load_config()
        minutes = max(15, min(720, int(config.get("refresh_minutes", 45))))
        render_config, active_theme = theme_for_refresh(config)
        log.info("Refresh started reason=%s physical=%s test=%s", reason, bool(config.get("physical_display")) or force_physical, test_pattern)
        save_status(state="refreshing", message="Preparing display...", refresh_reason=reason,
                    refresh_started=started_at, last_error=None, daemon_heartbeat=iso_now())
        if test_pattern:
            panel_image = make_hardware_test_pattern(str(render_config.get("display_profile", "waveshare-13in3e")))
        else:
            save_status(state="refreshing", message="Fetching weather...")
            weather = fetch_weather(render_config)
            save_status(state="refreshing", message="Rendering six-color image...")
            image = render_weather(weather, render_config)
            panel_image = rotate_for_panel(image, int(render_config.get("rotation", 0)))

        PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
        panel_image.save(PREVIEW_PATH, "PNG")
        physical = bool(config.get("physical_display")) or force_physical or test_pattern
        hardware_result = None
        if physical:
            save_status(state="refreshing", message="Writing to the physical e-paper panel...")
            hardware_result = send_to_display(panel_image, profile_id=str(render_config.get("display_profile", "waveshare-13in3e")), rotation=int(render_config.get("rotation", 0)), clear_first=test_pattern)

        now = iso_now()
        duration = round(time.monotonic() - started, 2)
        previous_physical = load_status().get("last_physical_refresh")
        save_status(state="idle", message="Physical display refreshed" if physical else "Preview refreshed (physical output is disabled)",
                    last_refresh=now, last_successful_refresh=now, last_physical_refresh=now if physical else previous_physical,
                    next_refresh=next_refresh_iso(minutes), last_error=None, hardware=hardware_result,
                    preview_only=not physical, active_theme=active_theme, refresh_duration_seconds=duration,
                    last_refresh_reason=reason, consecutive_failures=0)
        log.info("Refresh completed reason=%s duration=%.2fs physical=%s", reason, duration, physical)
        return {"ok": True, "message": "Refresh finished", "last_refresh": now, "hardware": hardware_result, "duration": duration}
    except Exception as exc:
        message = str(exc) or exc.__class__.__name__
        duration = round(time.monotonic() - started, 2)
        failures = int(load_status().get("consecutive_failures", 0)) + 1
        log.exception("Refresh failed reason=%s duration=%.2fs: %s", reason, duration, message)
        save_status(state="error", message="Refresh failed", last_error=message, last_failed_refresh=iso_now(),
                    refresh_duration_seconds=duration, last_refresh_reason=reason, consecutive_failures=failures)
        if not PREVIEW_PATH.exists():
            render_error(message, load_config()).save(PREVIEW_PATH, "PNG")
        return {"ok": False, "message": message, "duration": duration}
    finally:
        _refresh_lock.release()
