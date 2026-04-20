#!/usr/bin/env python3
"""Expand weather bundle JSON for Mustache (WMO labels, hero URL, form echo)."""
from __future__ import annotations

import json
import os
import sys

WMO = {
    0: ("☀️", "Clear sky"),
    1: ("🌤️", "Mainly clear"),
    2: ("⛅", "Partly cloudy"),
    3: ("☁️", "Overcast"),
    45: ("🌫️", "Fog"),
    48: ("🌫️", "Depositing rime fog"),
    51: ("🌦️", "Light drizzle"),
    53: ("🌦️", "Moderate drizzle"),
    55: ("🌧️", "Dense drizzle"),
    61: ("🌧️", "Slight rain"),
    63: ("🌧️", "Moderate rain"),
    65: ("⛈️", "Heavy rain"),
    71: ("🌨️", "Slight snow"),
    73: ("❄️", "Moderate snow"),
    75: ("❄️", "Heavy snow"),
    80: ("🌦️", "Rain showers"),
    81: ("🌧️", "Moderate showers"),
    82: ("⛈️", "Violent showers"),
    95: ("⛈️", "Thunderstorm"),
    96: ("⛈️", "Thunderstorm with hail"),
    99: ("⛈️", "Thunderstorm with heavy hail"),
}


def main() -> None:
    with open("weather_bundle.json", encoding="utf-8") as f:
        bundle = json.load(f)

    loc = os.environ.get("SEARCH_LOCATION", "")
    cw = bundle.get("weather", {}).get("current_weather") or {}
    code = cw.get("weathercode")
    if code is None:
        emoji, label = "🌡️", "Weather"
    else:
        emoji, label = WMO.get(int(code), ("🌡️", f"Weather code {code}"))

    place = (bundle.get("reference") or {}).get("place") or {}
    is_day = cw.get("is_day")
    hero = (
        "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b?auto=format&fit=crop&w=1600&q=80"
        if is_day == 0
        else "https://images.unsplash.com/photo-1598328665670-13a27a50716a?auto=format&fit=crop&w=1600&q=80"
    )

    postcodes = place.get("postcodes") or []
    postcodes_short = ", ".join(postcodes[:36])
    if len(postcodes) > 36:
        postcodes_short += ", …"

    out = dict(bundle)
    out["search_location"] = loc
    out["wmo_emoji"] = emoji
    out["wmo_label"] = label
    out["hero_image_url"] = hero
    out["postcodes_short"] = postcodes_short
    out["json_pretty"] = json.dumps(bundle, indent=2)
    print(json.dumps(out))


if __name__ == "__main__":
    try:
        main()
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as e:
        print(json.dumps({"error": "build_context_failed", "detail": str(e)}), file=sys.stderr)
        sys.exit(1)
