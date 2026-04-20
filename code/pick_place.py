#!/usr/bin/env python3
"""Read Open-Meteo geocode JSON; pick best match (first result = API relevance order)."""
from __future__ import annotations

import json
import os
import sys


def main() -> None:
    with open("geocode.json", encoding="utf-8") as f:
        geo = json.load(f)
    results = geo.get("results") if isinstance(geo, dict) else None
    if not results:
        print(json.dumps({"error": "no_results", "detail": "Geocoding returned no results"}), file=sys.stderr)
        sys.exit(1)

    chosen = results[0]
    if not isinstance(chosen, dict):
        print(json.dumps({"error": "invalid_result", "detail": "Unexpected geocode entry"}), file=sys.stderr)
        sys.exit(1)

    lat = float(chosen["latitude"])
    lon = float(chosen["longitude"])
    out = {
        "latitude": lat,
        "longitude": lon,
        "place": chosen,
        "geocode_request_url": os.environ.get("GEOCODE_REQUEST_URL", ""),
    }
    print(json.dumps(out))


if __name__ == "__main__":
    try:
        main()
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(json.dumps({"error": "pick_place_failed", "detail": str(e)}), file=sys.stderr)
        sys.exit(1)
