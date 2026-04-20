#!/usr/bin/env python3
"""Read Open-Meteo geocode JSON from geocode.json; emit Tampa, FL coordinates and place."""
from __future__ import annotations

import json
import sys

GEOCODE_REQUEST_URL = (
    "https://geocoding-api.open-meteo.com/v1/search?"
    "name=Tampa&count=10&language=en&format=json"
)


def pick_tampa_florida(geocode: object) -> tuple[float, float, dict]:
    results = geocode.get("results") if isinstance(geocode, dict) else None
    if not results:
        raise SystemExit("Geocoding returned no results for Tampa")

    chosen = None
    for r in results:
        if not isinstance(r, dict):
            continue
        if r.get("country_code") != "US":
            continue
        admin1 = (r.get("admin1") or "").lower()
        name = (r.get("name") or "").lower()
        if "florida" in admin1 or (name == "tampa" and admin1):
            chosen = r
            break

    if chosen is None:
        for r in results:
            if isinstance(r, dict) and r.get("country_code") == "US":
                chosen = r
                break
    if chosen is None:
        chosen = results[0]

    lat = float(chosen["latitude"])
    lon = float(chosen["longitude"])
    return lat, lon, chosen


def main() -> None:
    with open("geocode.json", encoding="utf-8") as f:
        geo = json.load(f)
    lat, lon, place = pick_tampa_florida(geo)
    out = {
        "latitude": lat,
        "longitude": lon,
        "place": place,
        "geocode_request_url": GEOCODE_REQUEST_URL,
    }
    print(json.dumps(out))


if __name__ == "__main__":
    try:
        main()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({"error": "pick_tampa_failed", "detail": str(e)}), file=sys.stderr)
        sys.exit(1)
