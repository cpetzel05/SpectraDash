from __future__ import annotations
from pathlib import Path
import platform, shutil, socket, psutil
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for, flash
from apscheduler.schedulers.background import BackgroundScheduler

from spectradash.backup import create_backup
from spectradash.config import AppConfig, DEFAULT_PATH, load_config, save_config
from spectradash.display.preview import render_preview
from spectradash.providers.location import search_location
from spectradash.providers.weather import get_weather

PREVIEW = Path("/var/lib/spectradash/preview.png")
BACKUPS = Path("/var/lib/spectradash/backups")

def create_app(config_path: Path | None = None) -> Flask:
    app = Flask(__name__)
    app.secret_key = "spectradash-local-session"
    target_config = config_path or DEFAULT_PATH

    def snapshot():
        return get_weather(load_config(target_config))

    @app.get("/")
    def dashboard():
        config = load_config(target_config)
        return render_template(
            "dashboard.html", weather=snapshot(), config=config,
            themes=["light","dark","ocean","desert","high-contrast"],
            layouts=["weather-station","premium-lcd"]
        )

    @app.route("/setup", methods=["GET", "POST"])
    def setup():
        config = load_config(target_config)
        if request.method == "POST":
            updated = AppConfig(
                provider=request.form.get("provider", "open-meteo"),
                latitude=float(request.form.get("latitude", config.latitude)),
                longitude=float(request.form.get("longitude", config.longitude)),
                location_name=request.form.get("location_name", config.location_name),
                location_query=request.form.get("location_query", config.location_query),
                units=request.form.get("units", "imperial"),
                refresh_minutes=max(5, int(request.form.get("refresh_minutes", 15))),
                display_profile="preview",
                layout=request.form.get("layout", "weather-station"),
                theme=request.form.get("theme", "desert"),
                auto_refresh=request.form.get("auto_refresh") == "on",
                bind_host=config.bind_host, bind_port=config.bind_port,
            )
            save_config(updated, target_config)
            flash("Configuration saved.")
            return redirect(url_for("dashboard"))
        return render_template("setup.html", config=config)

    @app.get("/api/location-search")
    def location_search():
        query = request.args.get("q", "").strip()
        if len(query) < 2:
            return jsonify([])
        return jsonify(search_location(query))

    @app.get("/api/weather")
    def api_weather():
        return jsonify(snapshot())

    @app.get("/api/diagnostics")
    def diagnostics_api():
        disk = shutil.disk_usage("/")
        return jsonify({
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "python": platform.python_version(),
            "cpu_percent": psutil.cpu_percent(0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": round(disk.used / disk.total * 100, 1),
            "service": "spectradash",
            "preview_path": str(PREVIEW),
        })

    @app.get("/diagnostics")
    def diagnostics():
        return render_template("diagnostics.html")

    @app.post("/refresh")
    def refresh():
        config = load_config(target_config)
        render_preview(snapshot(), PREVIEW, config.theme, config.layout)
        return redirect(url_for("preview"))

    @app.get("/preview")
    def preview():
        config = load_config(target_config)
        if not PREVIEW.exists():
            render_preview(snapshot(), PREVIEW, config.theme, config.layout)
        return send_file(PREVIEW, mimetype="image/png")

    @app.post("/backup")
    def backup():
        if not target_config.exists():
            save_config(load_config(target_config), target_config)
        created = create_backup(target_config, BACKUPS)
        flash(f"Backup created: {created.name}")
        return redirect(url_for("setup"))

    scheduler = BackgroundScheduler(daemon=True)
    def scheduled_preview():
        config = load_config(target_config)
        if config.auto_refresh:
            render_preview(snapshot(), PREVIEW, config.theme, config.layout)

    config = load_config(target_config)
    scheduler.add_job(
        scheduled_preview, "interval",
        minutes=max(5, config.refresh_minutes),
        id="preview-refresh", replace_existing=True
    )
    scheduler.start()

    return app

def main():
    config = load_config()
    create_app().run(host=config.bind_host, port=config.bind_port, debug=False)

if __name__ == "__main__":
    main()
