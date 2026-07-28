from __future__ import annotations
from datetime import datetime, timedelta
import math, requests

CODES = {
    0: ("Clear", "☀"), 1: ("Mostly clear", "🌤"), 2: ("Partly cloudy", "⛅"),
    3: ("Cloudy", "☁"), 45: ("Fog", "🌫"), 61: ("Light rain", "🌦"),
    63: ("Rain", "🌧"), 65: ("Heavy rain", "🌧"), 71: ("Snow", "🌨"),
    80: ("Showers", "🌦"), 95: ("Thunderstorm", "⛈"),
}

def mock_weather(location: str, units: str) -> dict:
    now = datetime.now().astimezone()
    conditions = [("Sunny","☀"),("Partly cloudy","⛅"),("Cloudy","☁"),
                  ("Rain","🌧"),("Sunny","☀"),("Windy","💨"),("Clear","☀")]
    forecast = []
    for i, (condition, icon) in enumerate(conditions):
        forecast.append({
            "date": (now.date() + timedelta(days=i)).isoformat(),
            "high": 74 + i, "low": 56 + i,
            "rain": (i * 13) % 80, "condition": condition, "icon": icon
        })
    return {
        "location": location, "units": units, "source": "Mock provider",
        "current": {
            "temperature": 72.4, "feels_like": 72.0, "humidity": 48,
            "wind_speed": 6.2, "pressure": 1016.3, "dew_point": 51.8,
            "condition": "Partly cloudy", "icon": "⛅",
            "observed_at": now.isoformat()
        },
        "forecast": forecast, "sunrise": "06:05", "sunset": "20:14"
    }

def _dew_point_c(temp_c: float, humidity: float) -> float:
    a, b = 17.625, 243.04
    gamma = math.log(max(humidity, 1) / 100.0) + (a * temp_c) / (b + temp_c)
    return (b * gamma) / (a - gamma)

def open_meteo_weather(latitude: float, longitude: float, location: str, units: str) -> dict:
    imperial = units == "imperial"
    params = {
        "latitude": latitude, "longitude": longitude, "timezone": "auto",
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,surface_pressure,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset",
        "temperature_unit": "fahrenheit" if imperial else "celsius",
        "wind_speed_unit": "mph" if imperial else "kmh", "forecast_days": 7
    }
    r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    current = data["current"]
    temp = float(current["temperature_2m"])
    humidity = int(current["relative_humidity_2m"])
    temp_c = (temp - 32) * 5 / 9 if imperial else temp
    dew_c = _dew_point_c(temp_c, humidity)
    dew = dew_c * 9 / 5 + 32 if imperial else dew_c
    condition, icon = CODES.get(int(current.get("weather_code", 0)), ("Unknown", "•"))
    daily = data["daily"]
    forecast = []
    for i, date in enumerate(daily["time"]):
        c, ic = CODES.get(int(daily["weather_code"][i]), ("Unknown", "•"))
        forecast.append({
            "date": date, "high": daily["temperature_2m_max"][i],
            "low": daily["temperature_2m_min"][i],
            "rain": daily["precipitation_probability_max"][i] or 0,
            "condition": c, "icon": ic
        })
    return {
        "location": location, "units": units, "source": "Open-Meteo",
        "current": {
            "temperature": temp, "feels_like": current["apparent_temperature"],
            "humidity": humidity, "wind_speed": current["wind_speed_10m"],
            "pressure": current["surface_pressure"], "dew_point": round(dew, 1),
            "condition": condition, "icon": icon, "observed_at": current["time"]
        },
        "forecast": forecast,
        "sunrise": daily["sunrise"][0].split("T")[-1],
        "sunset": daily["sunset"][0].split("T")[-1]
    }

def get_weather(config) -> dict:
    if config.provider == "mock":
        return mock_weather(config.location_name, config.units)
    if config.provider == "open-meteo":
        return open_meteo_weather(
            config.latitude, config.longitude, config.location_name, config.units
        )
    raise ValueError(f"Unsupported provider: {config.provider}")
