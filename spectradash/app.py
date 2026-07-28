from __future__ import annotations

import json
import os
import tempfile
import io
import zipfile
import platform
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename

from . import __version__
from .config import (
    COMMAND_PATH, CONFIG_PATH, DATA_DIR, DEFAULT_CONFIG, LOG_PATH, PREVIEW_PATH, STATUS_PATH, UPLOAD_DIR,
    default_config, load_config, load_status, location_is_configured, save_config, save_status,
)
from .display import driver_diagnostics
from .display_profiles import DEFAULT_PROFILE_ID, PROFILES, get_profile, list_profiles
from .render import THEMES, render_error
from .plugins import discover_plugins, install_plugin_zip, remove_plugin, set_plugin_enabled
from .system import system_info
from .weather import geocode, fetch_weather

def _queue_daemon_command(**payload: Any) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=DATA_DIR, delete=False, encoding="utf-8") as tmp:
        json.dump(payload, tmp)
        tmp.flush()
        os.fsync(tmp.fileno())
        name = tmp.name
    os.replace(name, COMMAND_PATH)


def _daemon_health() -> dict[str, Any]:
    status = load_status()
    heartbeat = status.get("daemon_heartbeat")
    age = None
    healthy = False
    if heartbeat:
        try:
            age = max(0, (datetime.now() - datetime.fromisoformat(str(heartbeat))).total_seconds())
            healthy = age < 90 and status.get("daemon_state") == "running"
        except Exception:
            pass
    return {"healthy": healthy, "heartbeat_age_seconds": round(age, 1) if age is not None else None,
            "state": status.get("daemon_state", "unknown"), "pid": status.get("daemon_pid")}


def _parse_settings(form: Any, current: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    updated = current.copy()
    error = None
    submitted_location = str(form.get("location", current["location_name"])).strip()
    if submitted_location and submitted_location.casefold() != str(current.get("location_name", "")).casefold():
        try:
            updated.update(geocode(submitted_location))
        except Exception as exc:
            error = str(exc)
    updated["units"] = "celsius" if form.get("units") == "celsius" else "fahrenheit"
    updated["wind_units"] = "kmh" if form.get("wind_units") == "kmh" else "mph"
    try:
        rotation = int(form.get("rotation", current.get("rotation", 0)))
    except (TypeError, ValueError):
        rotation = 0
    updated["rotation"] = rotation if rotation in {0, 90, 180, 270} else 0
    try:
        updated["refresh_minutes"] = max(15, min(720, int(form.get("refresh_minutes", 45))))
    except (TypeError, ValueError):
        updated["refresh_minutes"] = 45
    profile_id = str(form.get("display_profile", current.get("display_profile", DEFAULT_PROFILE_ID)))
    updated["display_profile"] = profile_id if profile_id in PROFILES else DEFAULT_PROFILE_ID
    updated["layout_density"] = str(form.get("layout_density", "auto")) if str(form.get("layout_density", "auto")) in {"auto","compact","standard","expanded"} else "auto"
    updated["physical_display"] = form.get("physical_display") == "on"
    updated["auto_rotate_theme"] = form.get("auto_rotate_theme") == "on"
    updated["show_hourly"] = form.get("show_hourly") == "on"
    updated["show_air_quality"] = form.get("show_air_quality") == "on"
    updated["show_moon"] = form.get("show_moon") == "on"
    updated["show_sun_times"] = form.get("show_sun_times") == "on"
    updated["show_environment"] = form.get("show_environment") == "on"
    updated["show_hourly_graph"] = form.get("show_hourly_graph") == "on"
    updated["auto_day_night"] = form.get("auto_day_night") == "on"
    updated["show_weather_summary"] = form.get("show_weather_summary") == "on"
    updated["living_scene"] = form.get("living_scene") == "on"
    updated["enable_3d_icons"] = form.get("enable_3d_icons") == "on"
    updated["icon_shadows"] = form.get("icon_shadows") == "on"
    updated["icon_highlights"] = form.get("icon_highlights") == "on"
    updated["scene_details"] = form.get("scene_details") == "on"
    updated["seasonal_details"] = form.get("seasonal_details") == "on"
    updated["living_details"] = form.get("living_details") == "on"
    updated["rainbow_effects"] = form.get("rainbow_effects") == "on"
    updated["theme_gallery"] = form.get("theme_gallery") == "on"
    updated["studio_animations"] = form.get("studio_animations") == "on"
    updated["show_weather_alerts"] = form.get("show_weather_alerts") == "on"
    updated["show_astronomy_details"] = form.get("show_astronomy_details") == "on"
    updated["show_system_status"] = form.get("show_system_status") == "on"
    updated["graph_style"] = form.get("graph_style") if form.get("graph_style") in {"premium","simple","off"} else "premium"
    updated["gauge_style"] = form.get("gauge_style") if form.get("gauge_style") in {"premium","compact"} else "premium"
    updated["seasonal_mode"] = form.get("seasonal_mode") if form.get("seasonal_mode") in {"automatic","spring","summer","autumn","winter","off"} else "automatic"
    updated["performance_mode"] = form.get("performance_mode") if form.get("performance_mode") in {"auto", "full", "lite"} else "auto"
    updated["lite_disable_animations"] = form.get("lite_disable_animations") == "on"
    updated["lite_cache_icons"] = form.get("lite_cache_icons") == "on"
    updated["lite_reduced_dither"] = form.get("lite_reduced_dither") == "on"
    updated["designer_enabled"] = form.get("designer_enabled") == "on"
    updated["developer_mode"] = form.get("developer_mode") == "on"
    updated["icon_style"] = form.get("icon_style") if form.get("icon_style") in {"premium", "3d", "flat", "minimal"} else "premium"
    updated["scene_style"] = form.get("scene_style") if form.get("scene_style") in {"landscape", "coastal", "desert", "forest", "lake", "prairie", "tropical", "winter", "city"} else "landscape"
    try:
        updated["animation_frames"] = max(1, min(8, int(form.get("animation_frames", 4))))
    except (TypeError, ValueError):
        updated["animation_frames"] = 4
    updated["first_day_of_week"] = "monday" if form.get("first_day_of_week") == "monday" else "sunday"
    forecast_date_style = str(form.get("forecast_date_style", current.get("forecast_date_style", "auto")))
    updated["forecast_date_style"] = forecast_date_style if forecast_date_style in {"auto", "off", "compact", "expanded"} else "auto"
    first_day_label = str(form.get("forecast_first_day_label", current.get("forecast_first_day_label", "today")))
    updated["forecast_first_day_label"] = first_day_label if first_day_label in {"today", "weekday"} else "today"
    updated["show_forecast_updated"] = form.get("show_forecast_updated") == "on"
    try:
        updated["hourly_hours"] = 12 if int(form.get("hourly_hours", 24)) == 12 else 24
    except (TypeError, ValueError):
        updated["hourly_hours"] = 24
    updated["layout_preset"] = form.get("layout_preset") if form.get("layout_preset") in {"weather-station", "minimal", "forecast-first", "premium-lcd", "designer"} else "weather-station"
    premium_lcd_mode = str(form.get("premium_lcd_mode", current.get("premium_lcd_mode", "dark")))
    updated["premium_lcd_mode"] = premium_lcd_mode if premium_lcd_mode in {"light", "dark", "automatic"} else "dark"
    submitted_theme = str(form.get("theme", "sunrise"))
    updated["theme"] = submitted_theme if submitted_theme in THEMES else "sunrise"
    title = str(form.get("custom_title", "SpectraDash")).strip()
    updated["custom_title"] = title[:40] or "SpectraDash"
    return updated, error


def _start_refresh(**kwargs: Any) -> tuple[Any, int]:
    health = _daemon_health()
    if not health["healthy"]:
        return jsonify({"ok": False, "message": "Refresh daemon is not healthy. Open Diagnostics or restart the service."}), 503
    _queue_daemon_command(action="refresh", **kwargs)
    save_status(message="Refresh queued", queued_refresh_reason=kwargs.get("reason", "manual"))
    return jsonify({"ok": True, "message": "Refresh queued for the daemon."}), 202


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024


    @app.route("/setup", methods=["GET", "POST"])
    def setup_wizard():
        current = load_config()
        if request.method == "POST":
            updated = current.copy()
            error = None
            location = str(request.form.get("location", current.get("location_name", ""))).strip()
            if not location:
                error = "Enter a city, state, ZIP code, or place name to finish setup."
            elif (
                location.casefold() != str(current.get("location_name", "")).casefold()
                or current.get("latitude") is None
                or current.get("longitude") is None
            ):
                try:
                    updated.update(geocode(location))
                except Exception as exc:
                    error = str(exc)
            updated["units"] = "celsius" if request.form.get("units") == "celsius" else "fahrenheit"
            updated["wind_units"] = "kmh" if request.form.get("wind_units") == "kmh" else "mph"
            profile = str(request.form.get("display_profile", DEFAULT_PROFILE_ID))
            updated["display_profile"] = profile if profile in PROFILES else DEFAULT_PROFILE_ID
            try:
                updated["refresh_minutes"] = max(15, min(720, int(request.form.get("refresh_minutes", 45))))
            except (TypeError, ValueError):
                updated["refresh_minutes"] = 45
            layout = str(request.form.get("layout_preset", "weather-station"))
            updated["layout_preset"] = layout if layout in {"weather-station", "minimal", "forecast-first", "premium-lcd"} else "weather-station"
            appearance = str(request.form.get("premium_lcd_mode", "automatic"))
            updated["premium_lcd_mode"] = appearance if appearance in {"light", "dark", "automatic"} else "automatic"
            if error:
                return render_template("setup.html", config=updated, profiles=list_profiles(), error=error, version=__version__)
            updated["setup_complete"] = True
            save_config(updated)
            return redirect(url_for("dashboard", message="Setup complete."))
        return render_template("setup.html", config=current, profiles=list_profiles(), error=None, version=__version__)

    @app.get("/theme-gallery")
    def theme_gallery():
        return render_template("theme_gallery.html", config=load_config(), themes=THEMES, version=__version__)

    @app.get("/studio-preview")
    def studio_preview():
        return render_template("studio_preview.html", config=load_config(), version=__version__)

    @app.get("/theme-marketplace")
    def theme_marketplace():
        return render_template("theme_marketplace.html", config=load_config(), version=__version__)

    @app.get("/")
    def dashboard():
        config = load_config()
        if not location_is_configured(config):
            return redirect(url_for("setup_wizard"))
        return render_template("dashboard.html", config=config, status=load_status(), system=system_info(), version=__version__)

    @app.route("/settings", methods=["GET", "POST"])
    def settings():
        current = load_config()
        message = request.args.get("message")
        error = request.args.get("error")
        if request.method == "POST":
            updated, validation_error = _parse_settings(request.form, current)
            if validation_error:
                for key in ("location_name", "latitude", "longitude", "timezone"):
                    updated[key] = current.get(key)
                save_config(updated)
                return redirect(url_for("settings", error=validation_error))
            save_config(updated)
            return redirect(url_for("settings", message="Settings saved."))
        return render_template("settings.html", config=current, status=load_status(), message=message, error=error, profiles=list_profiles(), version=__version__)

    @app.get("/settings/export")
    def export_settings():
        payload = load_config()
        body = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        return send_file(
            io.BytesIO(body.encode("utf-8")),
            mimetype="application/json",
            as_attachment=True,
            download_name=f"spectradash-settings-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json",
        )

    @app.post("/settings/import")
    def import_settings():
        upload = request.files.get("settings_file")
        if not upload or not upload.filename:
            return redirect(url_for("settings", error="Choose a SpectraDash JSON settings file."))
        if Path(upload.filename).suffix.lower() != ".json":
            return redirect(url_for("settings", error="The imported settings file must use the .json extension."))
        try:
            payload = json.load(upload.stream)
            if not isinstance(payload, dict):
                raise ValueError("The settings file must contain a JSON object.")
            unknown = sorted(set(payload) - set(DEFAULT_CONFIG))
            if unknown:
                raise ValueError("Unsupported setting keys: " + ", ".join(unknown[:8]))
            merged = default_config()
            merged.update(payload)
            if merged.get("setup_complete") and not location_is_configured(merged):
                raise ValueError("A completed setup must include a valid location, latitude, and longitude.")
            save_config(merged)
            _queue_daemon_command(action="restart-scheduler")
            destination = "settings" if location_is_configured(merged) else "setup_wizard"
            return redirect(url_for(destination, message="Settings imported."))
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            return redirect(url_for("settings", error=f"Import failed: {exc}"))

    @app.post("/settings/reset-defaults")
    def reset_defaults():
        current = load_config()
        reset = default_config()
        for key in ("location_name", "latitude", "longitude", "timezone", "setup_complete"):
            reset[key] = current.get(key)
        save_config(reset)
        _queue_daemon_command(action="restart-scheduler")
        return redirect(url_for("settings", message="Display and feature settings were reset. Your location was preserved."))

    @app.post("/settings/factory-reset")
    def factory_reset():
        save_config(default_config())
        for path in (STATUS_PATH, PREVIEW_PATH, COMMAND_PATH):
            path.unlink(missing_ok=True)
        return redirect(url_for("setup_wizard", message="Factory reset complete. Enter a location to begin again."))

    @app.get("/designer")
    def designer():
        plugins = [item.to_dict() for item in discover_plugins(include_disabled=False)]
        return render_template("designer.html", config=load_config(), plugins=plugins, version=__version__)

    @app.get("/plugins")
    def plugins_page():
        return render_template("plugins.html", plugins=discover_plugins(), message=request.args.get("message"), error=request.args.get("error"), version=__version__)

    @app.post("/plugins/install")
    def plugins_install():
        upload = request.files.get("plugin")
        if not upload or not upload.filename:
            return redirect(url_for("plugins_page", error="Choose a plugin ZIP first."))
        if Path(upload.filename).suffix.lower() != ".zip":
            return redirect(url_for("plugins_page", error="Plugins must be ZIP archives."))
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        temp_path = UPLOAD_DIR / ("plugin-" + secure_filename(upload.filename))
        upload.save(temp_path)
        try:
            info = install_plugin_zip(temp_path)
            return redirect(url_for("plugins_page", message=f"Installed {info.name} {info.version}."))
        except Exception as exc:
            return redirect(url_for("plugins_page", error=str(exc)))
        finally:
            temp_path.unlink(missing_ok=True)

    @app.post("/plugins/<path:plugin_id>/toggle")
    def plugins_toggle(plugin_id: str):
        try:
            current = next(item for item in discover_plugins() if item.plugin_id == plugin_id)
            updated = set_plugin_enabled(plugin_id, not current.enabled)
            action = "Enabled" if updated.enabled else "Disabled"
            return redirect(url_for("plugins_page", message=f"{action} {updated.name}."))
        except Exception as exc:
            return redirect(url_for("plugins_page", error=str(exc)))

    @app.post("/plugins/<path:plugin_id>/remove")
    def plugins_remove(plugin_id: str):
        try:
            remove_plugin(plugin_id)
            config = load_config()
            config["designer_layout"] = [item for item in config.get("designer_layout", []) if item.get("id") != plugin_id]
            save_config(config)
            return redirect(url_for("plugins_page", message="Plugin removed."))
        except Exception as exc:
            return redirect(url_for("plugins_page", error=str(exc)))

    @app.post("/api/designer-layout")
    def save_designer_layout():
        payload = request.get_json(silent=True) or {}
        layout = payload.get("layout")
        if not isinstance(layout, list) or len(layout) > 24:
            return jsonify({"ok": False, "message": "Invalid layout."}), 400
        allowed = {"current","metrics","hourly","sunmoon","forecast","summary","air","wind","clock","calendar","custom"}
        allowed.update(item.plugin_id for item in discover_plugins(include_disabled=False))
        cleaned = []
        for item in layout:
            if not isinstance(item, dict) or item.get("id") not in allowed:
                continue
            try:
                cleaned.append({
                    "id": item["id"],
                    "x": max(0, min(11, int(item.get("x", 0)))),
                    "y": max(0, min(11, int(item.get("y", 0)))),
                    "w": max(2, min(12, int(item.get("w", 4)))),
                    "h": max(2, min(12, int(item.get("h", 3)))),
                    "enabled": bool(item.get("enabled", True)),
                })
            except (TypeError, ValueError):
                continue
        config = load_config()
        config["designer_layout"] = cleaned
        config["designer_enabled"] = bool(payload.get("enabled", True))
        if config["designer_enabled"]:
            config["layout_preset"] = "designer"
        save_config(config)
        return jsonify({"ok": True, "message": "Designer layout saved.", "layout": cleaned})

    @app.get("/preview.png")
    def preview():
        if not PREVIEW_PATH.exists():
            render_error("No preview yet. Press Refresh Preview.", load_config()).save(PREVIEW_PATH, "PNG")
        return send_file(PREVIEW_PATH, mimetype="image/png", max_age=0)

    @app.post("/api/refresh")
    def api_refresh():
        return _start_refresh(reason="manual")

    @app.post("/api/refresh-physical")
    def api_refresh_physical():
        return _start_refresh(reason="manual-force", force_physical=True)

    @app.post("/api/hardware-test")
    def api_hardware_test():
        return _start_refresh(reason="hardware-test", force_physical=True, test_pattern=True)

    @app.get("/api/status")
    def api_status():
        payload = load_status()
        payload["system"] = system_info()
        payload["physical_display_enabled"] = bool(load_config().get("physical_display"))
        payload["daemon"] = _daemon_health()
        return jsonify(payload)

    @app.get("/diagnostics")
    def diagnostics():
        return render_template("diagnostics.html", config=load_config(), status=load_status(), system=system_info(), driver=driver_diagnostics(load_config().get("display_profile", DEFAULT_PROFILE_ID)), daemon=_daemon_health(), version=__version__)

    @app.post("/api/restart-scheduler")
    def api_restart_scheduler():
        if not _daemon_health()["healthy"]:
            return jsonify({"ok": False, "message": "Daemon heartbeat is stale; restart spectradash-daemon.service over SSH."}), 503
        _queue_daemon_command(action="restart-scheduler")
        return jsonify({"ok": True, "message": "Scheduler restart queued."}), 202

    @app.post("/upload")
    def upload():
        file = request.files.get("image")
        if not file or not file.filename:
            return redirect(url_for("dashboard", error="Choose an image first."))
        name = secure_filename(file.filename)
        if Path(name).suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            return redirect(url_for("dashboard", error="Use a PNG, JPG, or WebP image."))
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        file.save(UPLOAD_DIR / name)
        return redirect(url_for("dashboard", message=f"Uploaded {name}."))


    @app.get("/api/display-profiles")
    def display_profiles_api():
        return jsonify({"default": DEFAULT_PROFILE_ID, "profiles": [p.to_dict() for p in list_profiles()]})

    def _developer_allowed() -> bool:
        return bool(load_config().get("developer_mode"))

    @app.get("/developer")
    def developer():
        if not _developer_allowed():
            return redirect(url_for("settings", error="Enable Developer Mode in Settings first."))
        return render_template("developer.html", config=load_config(), status=load_status(), system=system_info(), daemon=_daemon_health(), version=__version__)

    @app.post("/api/developer/temperature-units")
    def developer_temperature_units():
        if not _developer_allowed():
            return jsonify({"ok": False, "message": "Developer Mode is disabled."}), 403
        payload = request.get_json(silent=True) or {}
        units = "celsius" if payload.get("units") == "celsius" else "fahrenheit"
        config = load_config()
        config["units"] = units
        save_config(config)
        _queue_daemon_command(action="refresh", reason="developer-units")
        return jsonify({"ok": True, "units": units, "message": f"Temperature units changed to {units.title()}. A refresh was queued."})

    @app.get("/api/developer/status")
    def developer_status():
        if not _developer_allowed():
            return jsonify({"ok": False, "message": "Developer Mode is disabled."}), 403
        config = load_config()
        safe_config = {
            "units": config.get("units", "fahrenheit"),
            "display_profile": config.get("display_profile"),
            "layout": config.get("layout"),
            "dashboard_layout": config.get("dashboard_layout"),
            "theme": config.get("theme"),
            "palette": config.get("palette"),
        }
        return jsonify({
            "ok": True,
            "version": __version__,
            "config": safe_config,
            "status": load_status(),
            "system": system_info(),
            "daemon": _daemon_health(),
        })

    @app.get("/api/developer/logs")
    def developer_logs():
        if not _developer_allowed():
            return jsonify({"ok": False, "message": "Developer Mode is disabled."}), 403
        try:
            lines = LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()[-250:]
        except FileNotFoundError:
            lines = []
        return jsonify({"ok": True, "lines": lines, "path": str(LOG_PATH)})

    @app.post("/api/developer/clear-logs")
    def developer_clear_logs():
        if not _developer_allowed():
            return jsonify({"ok": False, "message": "Developer Mode is disabled."}), 403
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        LOG_PATH.write_text("", encoding="utf-8")
        return jsonify({"ok": True, "message": "Application log cleared."})

    @app.post("/api/developer/test-weather")
    def developer_test_weather():
        if not _developer_allowed():
            return jsonify({"ok": False, "message": "Developer Mode is disabled."}), 403
        started = datetime.now()
        try:
            weather = fetch_weather(load_config())
            elapsed = round((datetime.now() - started).total_seconds(), 2)
            current = weather.get("current", {}) if isinstance(weather, dict) else {}
            return jsonify({"ok": True, "message": "Weather API test passed.", "duration_seconds": elapsed, "temperature": current.get("temperature_2m"), "weather_code": current.get("weather_code")})
        except Exception as exc:
            return jsonify({"ok": False, "message": str(exc) or exc.__class__.__name__}), 502

    @app.get("/api/developer/support-bundle")
    def developer_support_bundle():
        if not _developer_allowed():
            return jsonify({"ok": False, "message": "Developer Mode is disabled."}), 403
        config = load_config().copy()
        for key in list(config):
            if any(token in key.lower() for token in ("key", "token", "password", "secret")):
                config[key] = "REDACTED"
        payload = io.BytesIO()
        with zipfile.ZipFile(payload, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("config-redacted.json", json.dumps(config, indent=2, sort_keys=True))
            archive.writestr("status.json", json.dumps(load_status(), indent=2, sort_keys=True))
            archive.writestr("system.json", json.dumps(system_info(), indent=2, sort_keys=True))
            archive.writestr("daemon-health.json", json.dumps(_daemon_health(), indent=2, sort_keys=True))
            archive.writestr("runtime.txt", f"SpectraDash {__version__}\nPython {platform.python_version()}\nPlatform {platform.platform()}\n")
            if LOG_PATH.exists():
                archive.writestr("spectradash.log", "\n".join(LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()[-1000:]))
        payload.seek(0)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return send_file(payload, mimetype="application/zip", as_attachment=True, download_name=f"spectradash-support-{stamp}.zip")

    @app.get("/health")
    def health():
        health = _daemon_health()
        return jsonify({"ok": health["healthy"], "version": __version__, "status": load_status(), "daemon": health, "driver": driver_diagnostics(load_config().get("display_profile", DEFAULT_PROFILE_ID))})

    return app
