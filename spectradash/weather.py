from __future__ import annotations

import math
from datetime import date, datetime, timedelta
from typing import Any

import requests

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "SpectraDash/5.0"})
TIMEOUT = 18

WEATHER_CODES = {
    0: ("Clear sky", "sun"), 1: ("Mostly clear", "sun-cloud"), 2: ("Partly cloudy", "sun-cloud"),
    3: ("Overcast", "cloud"), 45: ("Fog", "fog"), 48: ("Rime fog", "fog"),
    51: ("Light drizzle", "drizzle"), 53: ("Drizzle", "drizzle"), 55: ("Heavy drizzle", "rain"),
    61: ("Light rain", "rain"), 63: ("Rain", "rain"), 65: ("Heavy rain", "rain"),
    66: ("Freezing rain", "ice"), 67: ("Heavy freezing rain", "ice"),
    71: ("Light snow", "snow"), 73: ("Snow", "snow"), 75: ("Heavy snow", "snow"), 77: ("Snow grains", "snow"),
    80: ("Rain showers", "rain"), 81: ("Rain showers", "rain"), 82: ("Heavy showers", "storm"),
    85: ("Snow showers", "snow"), 86: ("Heavy snow showers", "snow"),
    95: ("Thunderstorms", "storm"), 96: ("Storms with hail", "storm"), 99: ("Severe storms", "storm"),
}


def geocode(query: str) -> dict[str, Any]:
    query = query.strip()
    if not query:
        raise ValueError("Enter a city, ZIP code, or place name.")
    response = SESSION.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": query, "count": 5, "language": "en", "format": "json"}, timeout=TIMEOUT)
    response.raise_for_status()
    results = response.json().get("results") or []
    if not results:
        raise ValueError(f"No location matched “{query}”. Try a city and state or a ZIP code.")
    item = results[0]
    parts = [item.get("name"), item.get("admin1"), item.get("country_code")]
    return {"location_name": ", ".join(str(x) for x in parts if x), "latitude": float(item["latitude"]), "longitude": float(item["longitude"]), "timezone": item.get("timezone", "auto")}


def _description(code: int) -> tuple[str, str]:
    return WEATHER_CODES.get(int(code), ("Unknown", "cloud"))


def _compass(degrees: float) -> str:
    names = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return names[int((degrees + 22.5) // 45) % 8]


def _moon_phase(day: date) -> dict[str, Any]:
    # Synodic-month approximation; accurate enough for a dashboard label.
    known_new = date(2000, 1, 6)
    age = ((day - known_new).days % 29.53058867)
    fraction = age / 29.53058867
    illumination = round((1 - math.cos(2 * math.pi * fraction)) * 50)
    labels = [
        (1.84566, "New moon"), (5.53699, "Waxing crescent"), (9.22831, "First quarter"),
        (12.91963, "Waxing gibbous"), (16.61096, "Full moon"), (20.30228, "Waning gibbous"),
        (23.99361, "Last quarter"), (27.68493, "Waning crescent"), (30, "New moon"),
    ]
    label = next(name for limit, name in labels if age < limit)
    return {"label": label, "age": round(age, 1), "illumination": illumination, "fraction": fraction}



def _astronomy_details(day: date, moon: dict[str, Any]) -> dict[str, Any]:
    age = float(moon.get("age", 0))
    synodic = 29.53058867
    to_new = (synodic - age) % synodic
    to_full = (synodic / 2 - age) % synodic
    return {
        "moon_age": round(age, 1),
        "next_new_moon": (day + timedelta(days=round(to_new))).strftime("%b %-d"),
        "next_full_moon": (day + timedelta(days=round(to_full))).strftime("%b %-d"),
    }

def _local_alerts(current: dict[str, Any], daily: list[dict[str, Any]], hourly: list[dict[str, Any]]) -> list[dict[str, str]]:
    alerts=[]
    code=int(current.get("weather_code",0))
    wind=float(current.get("wind_speed_10m") or 0)
    temp=float(current.get("temperature_2m") or 0)
    rain=max((float(h.get("precip_probability") or 0) for h in hourly[:12]), default=0)
    if code in {95,96,99}: alerts.append({"severity":"warning","title":"Thunderstorm conditions","message":"Lightning, gusty winds, or hail may be possible nearby."})
    if wind >= 30: alerts.append({"severity":"warning","title":"Strong wind","message":f"Current wind is near {round(wind)}."})
    if rain >= 80: alerts.append({"severity":"watch","title":"Heavy rain potential","message":"High precipitation probability during the next 12 hours."})
    if temp >= 105: alerts.append({"severity":"warning","title":"Extreme heat","message":"Limit prolonged outdoor activity and stay hydrated."})
    return alerts[:2]

def _aqi_label(aqi: int | None) -> str:
    if aqi is None: return "Unavailable"
    if aqi <= 50: return "Good"
    if aqi <= 100: return "Moderate"
    if aqi <= 150: return "Sensitive groups"
    if aqi <= 200: return "Unhealthy"
    if aqi <= 300: return "Very unhealthy"
    return "Hazardous"


def _plain_summary(current: dict[str, Any], daily: list[dict[str, Any]], hourly: list[dict[str, Any]], symbol: str) -> str:
    high = daily[0]["high"] if daily else round(current["temperature_2m"])
    rain = max((h["precip_probability"] for h in hourly[:12]), default=0)
    wind = round(current["wind_speed_10m"])
    parts = [f"{_description(current['weather_code'])[0]} now, with a high near {high}{symbol}."]
    if rain >= 60:
        parts.append("Rain is likely later today.")
    elif rain >= 30:
        parts.append("A few showers are possible.")
    if wind >= 20:
        parts.append("Expect breezy conditions.")
    return " ".join(parts)


def fetch_weather(config: dict[str, Any]) -> dict[str, Any]:
    fahrenheit = config.get("units") == "fahrenheit"
    params = {
        "latitude": config["latitude"], "longitude": config["longitude"], "timezone": config.get("timezone") or "auto",
        "temperature_unit": "fahrenheit" if fahrenheit else "celsius", "wind_speed_unit": config.get("wind_units", "mph"),
        "precipitation_unit": "inch" if fahrenheit else "mm",
        "current": ",".join(["temperature_2m", "apparent_temperature", "relative_humidity_2m", "dew_point_2m", "precipitation", "weather_code", "cloud_cover", "surface_pressure", "wind_speed_10m", "wind_direction_10m", "visibility"]),
        "hourly": "temperature_2m,apparent_temperature,precipitation_probability,weather_code,uv_index,surface_pressure",
        "daily": ",".join(["weather_code", "temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum", "precipitation_probability_max", "wind_speed_10m_max", "uv_index_max"]),
        "forecast_days": 8,
    }
    response = SESSION.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=TIMEOUT)
    response.raise_for_status()
    raw = response.json(); current = raw["current"]
    desc, icon = _description(current["weather_code"])

    aqi = None
    try:
        aq = SESSION.get("https://air-quality-api.open-meteo.com/v1/air-quality", params={"latitude": config["latitude"], "longitude": config["longitude"], "timezone": config.get("timezone") or "auto", "current": "us_aqi,pm2_5"}, timeout=TIMEOUT).json().get("current", {})
        aqi = int(round(aq.get("us_aqi"))) if aq.get("us_aqi") is not None else None
        pm25 = round(aq.get("pm2_5"), 1) if aq.get("pm2_5") is not None else None
    except Exception:
        pm25 = None

    daily = []
    for i, stamp in enumerate(raw["daily"]["time"]):
        ddesc, dicon = _description(raw["daily"]["weather_code"][i])
        daily.append({"date": stamp, "label": datetime.fromisoformat(stamp).strftime("%a"), "description": ddesc, "icon": dicon,
            "high": round(raw["daily"]["temperature_2m_max"][i]), "low": round(raw["daily"]["temperature_2m_min"][i]),
            "precip_probability": raw["daily"]["precipitation_probability_max"][i] or 0, "precip_sum": raw["daily"]["precipitation_sum"][i] or 0,
            "wind": round(raw["daily"]["wind_speed_10m_max"][i]), "sunrise": raw["daily"]["sunrise"][i], "sunset": raw["daily"]["sunset"][i],
            "uv_max": round(raw["daily"]["uv_index_max"][i], 1) if raw["daily"]["uv_index_max"][i] is not None else None})
    hourly = []
    now = datetime.fromisoformat(current["time"])
    for i, stamp in enumerate(raw["hourly"]["time"]):
        when = datetime.fromisoformat(stamp)
        if when >= now and len(hourly) < int(config.get("hourly_hours", 24)):
            hdesc, hicon = _description(raw["hourly"]["weather_code"][i])
            hourly.append({"time": when.strftime("%I %p").lstrip("0"), "temperature": round(raw["hourly"]["temperature_2m"][i]),
                "feels_like": round(raw["hourly"]["apparent_temperature"][i]), "precip_probability": raw["hourly"]["precipitation_probability"][i] or 0,
                "description": hdesc, "icon": hicon, "uv": raw["hourly"]["uv_index"][i] or 0, "pressure": raw["hourly"]["surface_pressure"][i]})
    pressure_delta = 0
    if len(hourly) >= 4 and hourly[0]["pressure"] is not None and hourly[3]["pressure"] is not None:
        pressure_delta = round(hourly[3]["pressure"] - hourly[0]["pressure"])
    sunrise = datetime.fromisoformat(daily[0]["sunrise"]).strftime("%I:%M %p").lstrip("0")
    sunset = datetime.fromisoformat(daily[0]["sunset"]).strftime("%I:%M %p").lstrip("0")
    current_hour = now.hour
    moon = _moon_phase(now.date())
    astronomy = _astronomy_details(now.date(), moon)
    alerts = _local_alerts(current, daily, hourly)
    return {
        "location": config["location_name"], "timezone": raw.get("timezone"), "updated": current["time"],
        "temperature": round(current["temperature_2m"]), "feels_like": round(current["apparent_temperature"]),
        "humidity": current["relative_humidity_2m"], "dew_point": round(current["dew_point_2m"]), "precipitation": current["precipitation"],
        "cloud_cover": current["cloud_cover"], "pressure": round(current["surface_pressure"]), "pressure_delta": pressure_delta,
        "wind_speed": round(current["wind_speed_10m"]), "wind_direction": current["wind_direction_10m"], "wind_compass": _compass(current["wind_direction_10m"]),
        "visibility": round((current.get("visibility") or 0) / (1609.344 if fahrenheit else 1000), 1),
        "description": desc, "icon": icon, "daily": daily, "hourly": hourly, "sunrise": sunrise, "sunset": sunset,
        "uv_index": daily[0]["uv_max"], "aqi": aqi, "aqi_label": _aqi_label(aqi), "pm25": pm25, "moon": {**moon, **astronomy}, "alerts": alerts,
        "summary": _plain_summary(current, daily, hourly, "°F" if fahrenheit else "°C"),
        "is_night": current_hour < datetime.fromisoformat(daily[0]["sunrise"]).hour or current_hour >= datetime.fromisoformat(daily[0]["sunset"]).hour,
        "temperature_symbol": "°F" if fahrenheit else "°C", "precipitation_unit": "in" if fahrenheit else "mm",
        "visibility_unit": "mi" if fahrenheit else "km", "wind_unit": config.get("wind_units", "mph"),
    }
