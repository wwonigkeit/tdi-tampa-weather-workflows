# Tampa weather (Direktiv demo)

Demo namespace bundle: a **GET** API gateway runs a workflow that returns **Tampa, Florida** current weather as JSON. Geocoding and forecast calls use the **`http-request`** system service; short **Python** steps pick the correct city from geocode results and assemble the final payload (including a latitude/longitude check against the forecast document).

## Layout

| Path | Purpose |
|------|---------|
| `tdi-tampa-weather-workflows/gateways/tampa-weather.yaml` | API gateway: `GET` → workflow |
| `tdi-tampa-weather-workflows/workflows/tampa-weather.yaml` | Workflow definition |
| `tdi-tampa-weather-workflows/code/pick_tampa_place.py` | Choose Tampa (US/FL) from geocode JSON |
| `tdi-tampa-weather-workflows/code/assemble_tampa_response.py` | Merge + verify coords + output JSON |

## Workflow (high level)

1. **fetch-geocode** — `GET` [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api) for `name=Tampa`.
2. **pick-tampa-place** — Python reads the geocode response and emits coordinates and place metadata.
3. **fetch-forecast** — `GET` [Open-Meteo Forecast API](https://open-meteo.com/en/docs) with `current_weather=true` for those coordinates.
4. **assemble-response** — Python compares geocoded coordinates to the forecast document’s echoed coordinates (grid snap tolerated) and returns `{ reference, verification, weather }`.

## Gateway

- **Path:** `/weather/tampa` (see `gateways/tampa-weather.yaml` for full OpenAPI fragment).
- **Method:** `GET`
- **Auth:** `allow_anonymous: true` in the sample (tighten in production).

Full URL: `https://<your-direktiv-host>/ns/<namespace>/weather/tampa` (exact prefix depends on your Direktiv ingress and namespace routing).

## Dependencies (namespace)

The workflow expects these **system** services (same pattern as other demos in `tdi-demo-project`):

- `/services/http-request.yaml`
- `/services/python.yaml`

Ensure the Python and http-request images your cluster uses are available and scaled as needed.

## External APIs

No API keys: [Open-Meteo](https://open-meteo.com/) public endpoints only. Respect their fair-use guidance for production.

## Local checks (scripts only)

From `tdi-tampa-weather-workflows/code/`:

```bash
curl -sS 'https://geocoding-api.open-meteo.com/v1/search?name=Tampa&count=10&language=en&format=json' -o geocode.json
python3 pick_tampa_place.py > tampa.json
# build forecast URL from lat/lon in tampa.json, then:
curl -sS 'https://api.open-meteo.com/v1/forecast?latitude=...&longitude=...&current_weather=true' -o forecast.json
python3 assemble_tampa_response.py
```

## Deploy

Sync this tree into your Direktiv namespace (same process you use for other `tdi-*-workflows` folders in this repo): gateways and workflows must land at the paths referenced in the YAML (`/workflows/tampa-weather.yaml`, etc.).

## Static HTML preview

`../static/tampa-weather.html` is a single-file dashboard: paste workflow JSON into the `<script type="application/json" id="snapshot-data">` block and open the file in a browser (hero image, weather card, Leaflet map, expandable raw JSON). Requires network access for fonts, Unsplash hero image, Leaflet, and OSM tiles.
