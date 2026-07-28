from pathlib import Path
import platform
import shutil
import socket
import subprocess
import psutil
from flask import Flask, flash, jsonify, redirect, render_template, request, send_file, url_for

from spectradash.config import AppConfig, CONFIG_PATH, load_config, save_config
from spectradash.jobs import PREVIEW_PATH, render_and_show
from spectradash.providers.location import search_location
from spectradash.providers.weather import fetch_weather
from spectradash.rendering.dashboard import render_dashboard

def create_app(config_path: Path | None = None):
    app = Flask(__name__)
    app.secret_key = "spectradash-local-only"
    target = config_path or CONFIG_PATH

    def config():
        return load_config(target)

    def weather():
        return fetch_weather(config())

    @app.get("/")
    def dashboard():
        return render_template("dashboard.html", config=config(), weather=weather())

    @app.route("/setup", methods=["GET", "POST"])
    def setup():
        current = config()
        if request.method == "POST":
            updated = AppConfig(
                provider="open-meteo",
                location_query=request.form.get("location_query", current.location_query),
                location_name=request.form.get("location_name", current.location_name),
                latitude=float(request.form.get("latitude", current.latitude)),
                longitude=float(request.form.get("longitude", current.longitude)),
                units=request.form.get("units", current.units),
                layout=request.form.get("layout", current.layout),
                theme=request.form.get("theme", current.theme),
                display_profile=request.form.get("display_profile", current.display_profile),
                refresh_minutes=max(3, int(request.form.get("refresh_minutes", current.refresh_minutes))),
                auto_refresh=request.form.get("auto_refresh") == "on",
                bind_host=current.bind_host,
                bind_port=current.bind_port,
            )
            save_config(updated, target)
            flash("Configuration saved. Restarting the refresh worker.")
            subprocess.run(["systemctl", "restart", "spectradash-worker"], check=False)
            return redirect(url_for("dashboard"))
        return render_template("setup.html", config=current)

    @app.get("/api/location-search")
    def location_search():
        query = request.args.get("q", "").strip()
        return jsonify(search_location(query) if len(query) >= 2 else [])

    @app.get("/api/weather")
    def api_weather():
        return jsonify(weather())

    @app.get("/diagnostics")
    def diagnostics():
        return render_template("diagnostics.html", config=config())

    @app.get("/api/diagnostics")
    def api_diagnostics():
        disk = shutil.disk_usage("/")
        return jsonify({
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "python": platform.python_version(),
            "cpu_percent": psutil.cpu_percent(0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": round(disk.used / disk.total * 100, 1),
            "web_service": subprocess.run(
                ["systemctl", "is-active", "spectradash"],
                capture_output=True, text=True
            ).stdout.strip(),
            "worker_service": subprocess.run(
                ["systemctl", "is-active", "spectradash-worker"],
                capture_output=True, text=True
            ).stdout.strip(),
            "display_profile": config().display_profile,
        })

    @app.post("/render-preview")
    def render_preview():
        current = config()
        render_dashboard(weather(), PREVIEW_PATH, current.theme, current.layout)
        flash("Preview rendered.")
        return redirect(url_for("preview"))

    @app.post("/refresh-display")
    def refresh_display():
        try:
            render_and_show()
            flash("Display refresh completed.")
        except Exception as exc:
            flash(f"Display refresh failed: {exc}")
        return redirect(url_for("dashboard"))

    @app.get("/preview")
    def preview():
        if not PREVIEW_PATH.exists():
            current = config()
            render_dashboard(weather(), PREVIEW_PATH, current.theme, current.layout)
        return send_file(PREVIEW_PATH, mimetype="image/png")

    @app.post("/backup")
    def backup():
        backup_dir = Path("/var/lib/spectradash/backups")
        backup_dir.mkdir(parents=True, exist_ok=True)
        destination = backup_dir / "config-latest.json"
        shutil.copy2(target, destination)
        flash(f"Backup saved to {destination}.")
        return redirect(url_for("setup"))

    return app

def main():
    current = load_config()
    create_app().run(host=current.bind_host, port=current.bind_port, debug=False)

if __name__ == "__main__":
    main()
