from __future__ import annotations
from datetime import datetime, timezone
import math
import requests

CODES = {
    0: ("Clear", "clear-day"), 1: ("Mostly clear", "partly-cloudy-day"),
    2: ("Partly cloudy", "partly-cloudy-day"), 3: ("Cloudy", "cloudy"),
    45: ("Fog", "fog"), 48: ("Freezing fog", "fog"),
    51: ("Light drizzle", "rain"), 53: ("Drizzle", "rain"),
    55: ("Heavy drizzle", "heavy-rain"), 61: ("Light rain", "rain"),
    63: ("Rain", "rain"), 65: ("Heavy rain", "heavy-rain"),
    71: ("Light snow", "snow"), 73: ("Snow", "snow"),
    75: ("Heavy snow", "snow"), 80: ("Showers", "rain"),
    81: ("Showers", "rain"), 82: ("Heavy showers", "heavy-rain"),
    95: ("Thunderstorm", "storm"), 96: ("Thunderstorm with hail", "storm"),
    99: ("Severe thunderstorm", "storm"),
}

def _dew_point_c(temp_c: float, humidity: float) -> float:
    a, b = 17.625, 243.04
    gamma = math.log(max(humidity, 1) / 100.0) + (a * temp_c) / (b + temp_c)
    return (b * gamma) / (a - gamma)

def _moon(now: datetime) -> dict:
    base = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    age = ((now.astimezone(timezone.utc) - base).total_seconds() / 86400) % 29.53058867
    fraction = age / 29.53058867
    names = [
        (0.03, "New Moon"), (0.22, "Waxing Crescent"),
        (0.28, "First Quarter"), (0.47, "Waxing Gibbous"),
        (0.53, "Full Moon"), (0.72, "Waning Gibbous"),
        (0.78, "Last Quarter"), (0.97, "Waning Crescent"),
        (1.01, "New Moon"),
    ]
    name = next(label for cutoff, label in names if fraction <= cutoff)
    illumination = round((1 - math.cos(2 * math.pi * fraction)) / 2 * 100)
    return {"name": name, "age": round(age, 1), "illumination": illumination}

def _aqi_category(value):
    if value is None: return "Unavailable"
    if value <= 50: return "Good"
    if value <= 100: return "Moderate"
    if value <= 150: return "Unhealthy for sensitive groups"
    if value <= 200: return "Unhealthy"
    if value <= 300: return "Very unhealthy"
    return "Hazardous"

def _notices(code: int, gust: float, rain: int, uv: float, aqi) -> list[dict]:
    notices = []
    if code in {95, 96, 99}:
        notices.append({"level": "danger", "title": "Thunderstorm conditions", "text": "Lightning and severe weather may be possible."})
    if gust >= 35:
        notices.append({"level": "warning", "title": "Strong wind", "text": f"Forecast gusts may reach {gust:.0f}."})
    if rain >= 80:
        notices.append({"level": "info", "title": "High rain probability", "text": f"Precipitation probability is {rain}%."})
    if uv >= 8:
        notices.append({"level": "warning", "title": "Very high UV", "text": f"UV index is {uv:.1f}."})
    if aqi is not None and aqi > 100:
        notices.append({"level": "warning", "title": "Air quality", "text": f"US AQI is {aqi}."})
    return notices

def fetch_weather(config) -> dict:
    imperial = config.units == "imperial"
    params = {
        "latitude": config.latitude,
        "longitude": config.longitude,
        "timezone": "auto",
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "precipitation,weather_code,surface_pressure,wind_speed_10m,"
            "wind_direction_10m,wind_gusts_10m"
        ),
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max,sunrise,sunset,uv_index_max"
        ),
        "temperature_unit": "fahrenheit" if imperial else "celsius",
        "wind_speed_unit": "mph" if imperial else "kmh",
        "forecast_days": 7,
    }
    weather_response = requests.get(
        "https://api.open-meteo.com/v1/forecast", params=params, timeout=25
    )
    weather_response.raise_for_status()
    data = weather_response.json()

    air_response = requests.get(
        "https://air-quality-api.open-meteo.com/v1/air-quality",
        params={
            "latitude": config.latitude,
            "longitude": config.longitude,
            "current": "us_aqi,pm2_5,pm10",
            "timezone": "auto",
        },
        timeout=25,
    )
    air_response.raise_for_status()
    air_current = air_response.json().get("current", {})

    current = data["current"]
    daily = data["daily"]
    code = int(current.get("weather_code", 0))
    condition, icon = CODES.get(code, ("Unknown", "unknown"))
    temp = float(current["temperature_2m"])
    humidity = int(current["relative_humidity_2m"])
    temp_c = (temp - 32) * 5 / 9 if imperial else temp
    dew_c = _dew_point_c(temp_c, humidity)
    dew = dew_c * 9 / 5 + 32 if imperial else dew_c

    forecast = []
    for i, date in enumerate(daily["time"]):
        day_condition, day_icon = CODES.get(int(daily["weather_code"][i]), ("Unknown", "unknown"))
        forecast.append({
            "date": date,
            "condition": day_condition,
            "icon": day_icon,
            "high": float(daily["temperature_2m_max"][i]),
            "low": float(daily["temperature_2m_min"][i]),
            "rain": int(daily["precipitation_probability_max"][i] or 0),
            "uv": float(daily["uv_index_max"][i] or 0),
        })

    now = datetime.now().astimezone()
    aqi = air_current.get("us_aqi")
    gust = float(current.get("wind_gusts_10m") or 0)
    uv = float(daily["uv_index_max"][0] or 0)
    rain = int(forecast[0]["rain"])

    return {
        "location": config.location_name,
        "units": config.units,
        "source": "Open-Meteo",
        "updated": now.isoformat(),
        "timezone": data.get("timezone", "auto"),
        "current": {
            "temperature": temp,
            "feels_like": float(current["apparent_temperature"]),
            "humidity": humidity,
            "dew_point": round(dew, 1),
            "wind_speed": float(current["wind_speed_10m"]),
            "wind_direction": int(current.get("wind_direction_10m") or 0),
            "wind_gust": gust,
            "pressure": float(current["surface_pressure"]),
            "precipitation": float(current.get("precipitation") or 0),
            "uv": uv,
            "condition": condition,
            "icon": icon,
        },
        "forecast": forecast,
        "sunrise": daily["sunrise"][0].split("T")[-1],
        "sunset": daily["sunset"][0].split("T")[-1],
        "moon": _moon(now),
        "air": {
            "aqi": aqi,
            "category": _aqi_category(aqi),
            "pm2_5": air_current.get("pm2_5"),
            "pm10": air_current.get("pm10"),
        },
        "notices": _notices(code, gust, rain, uv, aqi),
    }
