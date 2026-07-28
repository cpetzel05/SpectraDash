from __future__ import annotations

import json
import logging
from logging.handlers import RotatingFileHandler
import os
import signal
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .config import COMMAND_PATH, CONFIG_PATH, DATA_DIR, LOG_PATH, load_config, load_status, save_status
from .engine import iso_now, refresh_display

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
DATA_DIR.mkdir(parents=True, exist_ok=True)
_root_logger = logging.getLogger()
if not any(isinstance(handler, RotatingFileHandler) for handler in _root_logger.handlers):
    _file_handler = RotatingFileHandler(LOG_PATH, maxBytes=2_000_000, backupCount=3, encoding="utf-8")
    _file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    _root_logger.addHandler(_file_handler)
log = logging.getLogger("spectradash.daemon")
running = True


def stop(*_: Any) -> None:
    global running
    running = False


def write_command(payload: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=DATA_DIR, delete=False, encoding="utf-8") as tmp:
        json.dump(payload, tmp); tmp.flush(); os.fsync(tmp.fileno()); name = tmp.name
    os.replace(name, COMMAND_PATH)


def read_command() -> dict[str, Any] | None:
    try:
        payload = json.loads(COMMAND_PATH.read_text(encoding="utf-8"))
        COMMAND_PATH.unlink(missing_ok=True)
        return payload if isinstance(payload, dict) else None
    except FileNotFoundError:
        return None
    except Exception:
        log.exception("Unable to read daemon command")
        COMMAND_PATH.unlink(missing_ok=True)
        return None


def interval_minutes() -> int:
    return max(15, min(720, int(load_config().get("refresh_minutes", 45))))


def main() -> int:
    signal.signal(signal.SIGTERM, stop); signal.signal(signal.SIGINT, stop)
    log.info("SpectraDash refresh daemon starting")
    now = datetime.now()
    status = load_status()
    last = status.get("last_successful_refresh") or status.get("last_refresh")
    try:
        due = datetime.fromisoformat(str(last)) + timedelta(minutes=interval_minutes()) if last else now
    except Exception:
        due = now
    retry_due: datetime | None = None
    retry_attempt = 0
    last_config_mtime = CONFIG_PATH.stat().st_mtime if CONFIG_PATH.exists() else 0
    save_status(daemon_state="running", daemon_pid=os.getpid(), daemon_started=iso_now(), daemon_heartbeat=iso_now(),
                next_refresh=due.isoformat(timespec="seconds"))

    last_heartbeat_write = 0.0
    while running:
        now = datetime.now()
        if time.monotonic() - last_heartbeat_write >= 30:
            save_status(daemon_state="running", daemon_pid=os.getpid(), daemon_heartbeat=iso_now(),
                        next_refresh=(retry_due or due).isoformat(timespec="seconds"))
            last_heartbeat_write = time.monotonic()
        try:
            mtime = CONFIG_PATH.stat().st_mtime if CONFIG_PATH.exists() else 0
            if mtime != last_config_mtime:
                last_config_mtime = mtime
                due = now + timedelta(minutes=interval_minutes())
                retry_due = None; retry_attempt = 0
                log.info("Configuration changed; next refresh rescheduled for %s", due.isoformat(timespec="seconds"))
        except OSError:
            pass

        command = read_command()
        if command:
            action = str(command.get("action", "refresh"))
            log.info("Command received: %s", action)
            if action == "refresh":
                result = refresh_display(str(command.get("reason", "manual")),
                                         force_physical=bool(command.get("force_physical")),
                                         test_pattern=bool(command.get("test_pattern")))
                # A manual refresh resets the automatic countdown.
                if result.get("ok"):
                    due = datetime.now() + timedelta(minutes=interval_minutes())
                    retry_due = None; retry_attempt = 0
            elif action == "restart-scheduler":
                due = datetime.now()
                retry_due = None; retry_attempt = 0
                save_status(message="Scheduler restarted; refresh queued")

        now = datetime.now()
        target = retry_due or due
        if now >= target:
            reason = "retry" if retry_due else "schedule"
            result = refresh_display(reason)
            if result.get("ok"):
                retry_due = None; retry_attempt = 0
                due = datetime.now() + timedelta(minutes=interval_minutes())
            else:
                retry_attempt += 1
                if retry_attempt <= 3:
                    delay = min(15, 2 ** retry_attempt)
                    retry_due = datetime.now() + timedelta(minutes=delay)
                    log.warning("Refresh retry %d scheduled in %d minutes", retry_attempt, delay)
                    save_status(next_retry=retry_due.isoformat(timespec="seconds"), retry_attempt=retry_attempt)
                else:
                    log.error("Refresh retries exhausted; returning to normal interval")
                    retry_due = None; retry_attempt = 0
                    due = datetime.now() + timedelta(minutes=interval_minutes())
        time.sleep(2)

    save_status(daemon_state="stopped", daemon_heartbeat=iso_now())
    log.info("SpectraDash refresh daemon stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
