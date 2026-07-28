from __future__ import annotations
from datetime import datetime, timedelta, timezone
import math, requests

CODES = {
    0: ("Clear", "clear-day"), 1: ("Mostly clear", "partly-cloudy-day"),
    2: ("Partly cloudy", "partly-cloudy-day"), 3: ("Cloudy", "cloudy"),
    45: ("Fog", "fog"), 48: ("Freezing fog", "fog"),
    51: ("Light drizzle", "rain"), 53: ("Drizzle", "rain"),
    55: ("Heavy drizzle", "rain"), 61: ("Light rain", "rain"),
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

def _moon_phase(now: datetime) -> dict:
    known_new_moon = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    days = (now.astimezone(timezone.utc) - known_new_moon).total_seconds() / 86400
    age = days % 29.53058867
    fraction = age / 29.53058867
    phases = [
        (0.03, "New Moon"), (0.22, "Waxing Crescent"),
        (0.28, "First Quarter"), (0.47, "Waxing Gibbous"),
        (0.53, "Full Moon"), (0.72, "Waning Gibbous"),
        (0.78, "Last Quarter"), (0.97, "Waning Crescent"),
        (1.01, "New Moon"),
    ]
    name = next(label for cutoff, label in phases if fraction <= cutoff)
    illumination = round((1 - math.cos(2 * math.pi * fraction)) / 2 * 100)
    return {"name": name, "age_days": round(age, 1), "illumination": illumination}

def _alerts(code: int, wind_gust: float, rain_probability: int) -> list[dict]:
    alerts = []
    if code in {95, 96, 99}:
        alerts.append({"severity": "warning", "title": "Thunderstorm conditions", "body": "Lightning and strong storms may be possible."})
    if wind_gust >= 35:
        alerts.append({"severity": "watch", "title": "Strong wind", "body": f"Wind gusts may reach {wind_gust:.0f}."})
    if rain_probability >= 80:
        alerts.append({"severity": "info", "title": "High rain chance", "body": f"Precipitation probability is {rain_probability}%."})
    return alerts

def mock_weather(location: str, units: str) -> dict:
    now = datetime.now().astimezone()
    forecast = []
    sample = [
        ("Clear", "clear-day"), ("Partly cloudy", "partly-cloudy-day"),
        ("Cloudy", "cloudy"), ("Rain", "rain"), ("Clear", "clear-day"),
        ("Windy", "wind"), ("Clear", "clear-night")
    ]
    for i, (condition, icon) in enumerate(sample):
        forecast.append({
            "date": (now.date() + timedelta(days=i)).isoformat(),
            "high": 78 + i, "low": 59 + i, "rain": (i * 11) % 90,
            "condition": condition, "icon": icon,
        })
    return {
        "location": location, "units": units, "source": "Mock provider",
        "updated": now.isoformat(), "timezone": str(now.tzinfo),
        "current": {
            "temperature": 79.0, "feels_like": 81.0, "humidity": 45,
            "wind_speed": 8.0, "wind_gust": 14.0, "pressure": 1012.0,
            "dew_point": 56.0, "uv_index": 5.0, "weather_code": 1,
            "condition": "Mostly clear", "icon": "partly-cloudy-day",
            "precipitation": 0.0,
        },
        "forecast": forecast, "sunrise": "05:49", "sunset": "20:15",
        "moon": _moon_phase(now), "alerts": [], "air_quality": {"us_aqi": 42, "category": "Good"},
    }

def _aqi_category(value: int | None) -> str:
    if value is None: return "Unavailable"
    if value <= 50: return "Good"
    if value <= 100: return "Moderate"
    if value <= 150: return "Unhealthy for sensitive groups"
    if value <= 200: return "Unhealthy"
    if value <= 300: return "Very unhealthy"
    return "Hazardous"

def open_meteo_weather(latitude: float, longitude: float, location: str, units: str) -> dict:
    imperial = units == "imperial"
    weather_params = {
        "latitude": latitude, "longitude": longitude, "timezone": "auto",
        "current": (
            "temperature_2m,relative_humidity_2m,apparent_temperature,"
            "precipitation,weather_code,surface_pressure,wind_speed_10m,wind_gusts_10m"
        ),
        "daily": (
            "weather_code,temperature_2m_max,temperature_2m_min,"
            "precipitation_probability_max,sunrise,sunset,uv_index_max"
        ),
        "temperature_unit": "fahrenheit" if imperial else "celsius",
        "wind_speed_unit": "mph" if imperial else "kmh",
        "forecast_days": 7,
    }
    response = requests.get("https://api.open-meteo.com/v1/forecast", params=weather_params, timeout=20)
    response.raise_for_status()
    data = response.json()

    air = requests.get(
        "https://air-quality-api.open-meteo.com/v1/air-quality",
        params={
            "latitude": latitude, "longitude": longitude,
            "current": "us_aqi", "timezone": "auto",
        },
        timeout=20,
    )
    air.raise_for_status()
    aqi_value = air.json().get("current", {}).get("us_aqi")

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
            "high": float(daily["temperature_2m_max"][i]),
            "low": float(daily["temperature_2m_min"][i]),
            "rain": int(daily["precipitation_probability_max"][i] or 0),
            "condition": day_condition,
            "icon": day_icon,
            "uv_index": float(daily["uv_index_max"][i] or 0),
        })

    now = datetime.now().astimezone()
    gust = float(current.get("wind_gusts_10m") or 0)
    max_rain = int(forecast[0]["rain"])
    return {
        "location": location, "units": units, "source": "Open-Meteo",
        "updated": now.isoformat(), "timezone": data.get("timezone", "auto"),
        "current": {
            "temperature": temp,
            "feels_like": float(current["apparent_temperature"]),
            "humidity": humidity,
            "wind_speed": float(current["wind_speed_10m"]),
            "wind_gust": gust,
            "pressure": float(current["surface_pressure"]),
            "dew_point": round(dew, 1),
            "uv_index": float(daily["uv_index_max"][0] or 0),
            "weather_code": code,
            "condition": condition,
            "icon": icon,
            "precipitation": float(current.get("precipitation") or 0),
        },
        "forecast": forecast,
        "sunrise": daily["sunrise"][0].split("T")[-1],
        "sunset": daily["sunset"][0].split("T")[-1],
        "moon": _moon_phase(now),
        "alerts": _alerts(code, gust, max_rain),
        "air_quality": {"us_aqi": aqi_value, "category": _aqi_category(aqi_value)},
    }

def get_weather(config) -> dict:
    if config.provider == "mock":
        return mock_weather(config.location_name, config.units)
    return open_meteo_weather(config.latitude, config.longitude, config.location_name, config.units)
