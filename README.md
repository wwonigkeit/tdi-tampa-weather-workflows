# Tampa weather — Direktiv bundle

This directory is what you sync to a Direktiv namespace:

- **`gateways/`** — `tampa-weather.yaml` exposes `GET /weather/tampa`.
- **`workflows/`** — `tampa-weather.yaml` orchestrates `http-request` + `python` states.
- **`code/`** — Python helpers referenced by the workflow (`pick_tampa_place.py`, `assemble_tampa_response.py`).

Full documentation, dependency list, and local test commands: **[../README.md](../README.md)**.
