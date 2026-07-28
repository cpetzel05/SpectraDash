import requests

def search_location(query: str) -> list[dict]:
    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": query, "count": 10, "language": "en", "format": "json", "countryCode": "US"},
        timeout=15,
    )
    response.raise_for_status()
    output = []
    for item in response.json().get("results", []):
        parts = [item.get("name"), item.get("admin1"), item.get("country_code")]
        output.append({
            "label": ", ".join(x for x in parts if x),
            "latitude": item["latitude"],
            "longitude": item["longitude"],
            "timezone": item.get("timezone", "auto"),
        })
    return output
