#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from spectradash.display_profiles import list_profiles
from spectradash.render import render_weather


def sample_weather() -> dict:
    now = datetime.now().replace(second=0, microsecond=0)
    daily = []
    labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    icons = ["sun-cloud", "sun", "rain", "cloud", "storm", "sun", "sun-cloud"]
    for i in range(7):
        daily.append({"date": (now.date()+timedelta(days=i)).isoformat(), "label": labels[(now.weekday()+i)%7],
                      "icon": icons[i], "high": 88-i, "low": 68-i//2, "precip_probability": [10,5,55,25,65,10,15][i],
                      "wind": 8+i, "uv_max": max(3, 9-i), "description": ["Partly sunny","Sunny","Afternoon showers","Mostly cloudy","Thunderstorms","Clear and warm","Partly cloudy"][i]})
    hourly=[]
    for i in range(12):
        hourly.append({"time": (now+timedelta(hours=i)).strftime("%-I%p"), "temperature": 78+i//2,
                       "precip_probability": 10 if i<5 else 35 if i<8 else 15})
    return {"updated": now.isoformat(), "location": "SpectraDash Test Lab", "description": "Partly cloudy",
            "wind_compass": "NW", "wind_speed": 9, "wind_unit": "mph", "is_night": False,
            "temperature": 82, "feels_like": 84, "temperature_symbol": "°F", "icon": "sun-cloud", "humidity": 42,
            "dew_point": 57, "aqi": 31, "aqi_label": "Good", "uv_index": 6, "pressure": 1015,
            "pressure_delta": 1.4, "visibility": 10, "visibility_unit": "mi", "cloud_cover": 38,
            "wind_direction": 315, "sunrise": "5:34 AM", "sunset": "7:38 PM",
            "moon": {"label": "Waxing crescent", "illumination": 28},
            "summary": "Warm and partly cloudy today, with a small chance of an afternoon shower.",
            "daily": daily, "hourly": hourly}


def main() -> None:
    output = ROOT / "screenshots"
    output.mkdir(exist_ok=True)
    weather = sample_weather()
    for profile in list_profiles():
        config = {"display_profile": profile.id, "theme": "windows-xp", "performance_mode": "lite",
                  "refresh_minutes": 30, "custom_title": "SpectraDash", "living_scene": True,
                  "scene_style": "landscape", "animation_frames": 1, "show_hourly_graph": True,
                  "show_weather_summary": True, "first_day_of_week": "sunday", "auto_day_night": True,
                  "icon_style": "3d", "enable_3d_icons": True, "icon_shadows": False, "icon_highlights": False,
                  "scene_details": False, "seasonal_details": False, "living_details": False,
                  "rainbow_effects": False, "designer_enabled": False, "lite_disable_animations": True,
                  "lite_reduced_dither": True}
        image = render_weather(weather, config)
        image.save(output / f"preview-{profile.id}.png")
        print(f"Rendered {profile.id}: {image.width}x{image.height}")

    premium_base = {"display_profile": "waveshare-13in3e", "layout_preset": "premium-lcd",
                    "performance_mode": "lite", "refresh_minutes": 30, "show_moon": True,
                    "forecast_first_day_label": "today", "forecast_date_style": "expanded",
                    "icon_style": "premium", "lite_reduced_dither": True}
    for appearance in ("dark", "light"):
        premium_config = {**premium_base, "premium_lcd_mode": appearance}
        image = render_weather(weather, premium_config)
        image.save(output / f"preview-premium-lcd-{appearance}-13in3.png")
        print(f"Rendered Premium LCD {appearance}: {image.width}x{image.height}")

if __name__ == "__main__":
    main()
