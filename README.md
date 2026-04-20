# Tampa weather (Direktiv demo)

Weather data from [Open-Meteo](https://open-meteo.com/) (geocode + forecast) using the **`http-request`** service, **Python** for place selection and JSON assembly, and optionally **`gcr.io/direktiv/functions/mustache`** for a **dynamic HTML** page (same pattern as Dell formrequest: workflow → `{ result: html }` → `js-outbound`).

## Layout

| Path | Purpose |
|------|---------|
| `gateways/tampa-weather.yaml` | `GET /weather/tampa` → JSON (fixed Tampa via subflow) |
| `gateways/tampa-weather-page.yaml` | `GET /weather/page?location=…` → **HTML** dashboard |
| `workflows/get-weather-json.yaml` | Subflow: geocode + pick + forecast + assemble `{ reference, verification, weather }` |
| `workflows/tampa-weather.yaml` | Calls `get-weather-json` with `location_query: Tampa` |
| `workflows/weather-page.yaml` | Query param `location` → subflow → `build_html_context.py` → Mustache |
| `code/pick_place.py` | First geocode hit (API relevance order) |
| `code/assemble_weather_response.py` | Merge place + forecast; verify coordinates |
| `code/build_html_context.py` | WMO labels, hero URL, Mustache extras |
| `code/weather-page.mustache` | HTML template for the dynamic page |

## Gateways

| Path | Response |
|------|----------|
| `/weather/tampa` | JSON (backward-compatible default location) |
| `/weather/page` | `text/html` — form submits `location` (default **Tampa**) |

Example: `…/weather/page?location=Miami`

## Workflows (high level)

**`get-weather-json`** (input: `{ "location_query": "Berlin" }`):

1. Geocode `name=` + URL-encoded query  
2. Python picks **`results[0]`**  
3. Forecast `current_weather=true`  
4. Python verifies grid vs geocode and returns JSON  

**`weather-page`**: reads `query_params.location[0]`, runs the subflow, expands context for Mustache, renders **`weather-page.mustache`**, returns `{ "result": "<html>…" }`. The gateway **`js-outbound`** unwraps `result` and sets `Content-Type: text/html; charset=utf-8`.

## Dependencies

- `/services/http-request.yaml`
- `/services/python.yaml`
- **`gcr.io/direktiv/functions/mustache:1.0`** (for `/weather/page` only) — ensure the cluster can pull this image (mirror if you use a private registry).

## External APIs

No API keys. Respect Open-Meteo fair-use limits in production.

## Local checks (scripts)

From `code/`:

```bash
curl -sS 'https://geocoding-api.open-meteo.com/v1/search?name=Tampa&count=10&language=en&format=json' -o geocode.json
export GEOCODE_REQUEST_URL='https://geocoding-api.open-meteo.com/v1/search?name=Tampa&count=10&language=en&format=json'
python3 pick_place.py > place.json
# forecast from lat/lon in place.json
curl -sS 'https://api.open-meteo.com/v1/forecast?latitude=...&longitude=...&current_weather=true' -o forecast.json
python3 assemble_weather_response.py > bundle.json
cp bundle.json weather_bundle.json
export SEARCH_LOCATION=Tampa
python3 build_html_context.py
```

## Static offline preview

`../static/tampa-weather.html` — paste JSON into the embedded script block; no Direktiv required.

## Deploy

Sync this tree into your Direktiv namespace so workflows and gateways resolve (`/workflows/get-weather-json.yaml`, `/code/*.py`, `/code/weather-page.mustache`, etc.).
