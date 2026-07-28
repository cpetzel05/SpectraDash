from pathlib import Path
from spectradash.rendering.dashboard import render_dashboard

def test_render(tmp_path: Path):
    weather = {
        "location":"Test","updated":"2026-01-01T12:00","source":"Test",
        "current":{"temperature":70,"condition":"Clear","feels_like":70,"humidity":40,
        "dew_point":45,"wind_speed":5,"wind_gust":8,"pressure":1012,"uv":3,"precipitation":0},
        "air":{"aqi":20,"category":"Good","pm2_5":2,"pm10":5},
        "moon":{"name":"Full Moon","illumination":100},
        "sunrise":"06:00","sunset":"18:00",
        "forecast":[{"date":f"2026-01-0{i+1}","condition":"Clear","high":75,"low":55,"rain":0,"uv":3} for i in range(7)],
    }
    output = tmp_path / "preview.png"
    render_dashboard(weather, output, "light", "weather-station")
    assert output.exists()
