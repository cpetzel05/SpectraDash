from pathlib import Path
import platform, shutil, socket, psutil
from flask import Flask, jsonify, redirect, render_template, request, send_file, url_for
from spectradash.config import AppConfig, load_config, save_config
from spectradash.providers.weather import get_weather
from spectradash.display.preview import render_preview

PREVIEW = Path("/var/lib/spectradash/preview.png")

def create_app(config_path: Path | None = None) -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def dashboard():
        config = load_config(config_path)
        return render_template("dashboard.html", weather=get_weather(config))

    @app.route("/setup", methods=["GET", "POST"])
    def setup():
        config = load_config(config_path)
        if request.method == "POST":
            updated = AppConfig(
                provider=request.form.get("provider", "mock"),
                latitude=float(request.form.get("latitude", config.latitude)),
                longitude=float(request.form.get("longitude", config.longitude)),
                location_name=request.form.get("location_name", config.location_name),
                units=request.form.get("units", "imperial"),
                refresh_minutes=max(5, int(request.form.get("refresh_minutes", 15))),
                display_profile="preview", bind_host=config.bind_host, bind_port=config.bind_port
            )
            save_config(updated, config_path)
            return redirect(url_for("dashboard"))
        return render_template("setup.html", config=config)

    @app.get("/api/weather")
    def api_weather():
        return jsonify(get_weather(load_config(config_path)))

    @app.get("/api/diagnostics")
    def diagnostics():
        disk = shutil.disk_usage("/")
        return jsonify({
            "hostname": socket.gethostname(), "platform": platform.platform(),
            "python": platform.python_version(), "cpu_percent": psutil.cpu_percent(0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": round(disk.used / disk.total * 100, 1)
        })

    @app.post("/refresh")
    def refresh():
        render_preview(get_weather(load_config(config_path)), PREVIEW)
        return redirect(url_for("preview"))

    @app.get("/preview")
    def preview():
        if not PREVIEW.exists():
            render_preview(get_weather(load_config(config_path)), PREVIEW)
        return send_file(PREVIEW, mimetype="image/png")

    return app

def main():
    config = load_config()
    create_app().run(host=config.bind_host, port=config.bind_port, debug=False)

if __name__ == "__main__":
    main()
