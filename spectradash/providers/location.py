from __future__ import annotations
import requests

def search_location(query: str, country_code: str = "US") -> list[dict]:
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": query,
            "count": 8,
            "language": "en",
            "format": "json",
            "countryCode": country_code,
        },
        timeout=15,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    cleaned = []
    for item in results:
        label_parts = [
            item.get("name"),
            item.get("admin1"),
            item.get("country_code"),
        ]
        cleaned.append({
            "name": ", ".join(p for p in label_parts if p),
            "latitude": item["latitude"],
            "longitude": item["longitude"],
            "timezone": item.get("timezone", "auto"),
        })
    return cleaned
