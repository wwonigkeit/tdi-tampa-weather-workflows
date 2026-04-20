#!/usr/bin/env python3
"""Combine Tampa pick + forecast JSON; verify grid coords vs geocode and print final payload."""
from __future__ import annotations

import json
import sys


def main() -> None:
    with open("tampa.json", encoding="utf-8") as f:
        tampa = json.load(f)
    with open("forecast.json", encoding="utf-8") as f:
        weather = json.load(f)

    lat = float(tampa["latitude"])
    lon = float(tampa["longitude"])
    if not isinstance(weather, dict):
        raise SystemExit("Forecast response is not a JSON object")

    w_lat = float(weather.get("latitude", lat))
    w_lon = float(weather.get("longitude", lon))
    verified = abs(w_lat - lat) < 0.05 and abs(w_lon - lon) < 0.05

    q = (
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )
    forecast_url = f"https://api.open-meteo.com/v1/forecast?{q}"

    out = {
        "reference": {
            "source": "Open-Meteo Geocoding API (https://open-meteo.com/en/docs/geocoding-api)",
            "request_url": tampa.get("geocode_request_url", ""),
            "place": tampa.get("place"),
        },
        "verification": {
            "coordinates_from_geocode": {"latitude": lat, "longitude": lon},
            "weather_request_url": forecast_url,
            "coordinates_match": verified,
        },
        "weather": weather,
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({"error": "assemble_failed", "detail": str(e)}), file=sys.stderr)
        sys.exit(1)
