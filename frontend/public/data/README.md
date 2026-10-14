# Data

## provinsi.json

Indonesia's 38 province boundaries, used in the browser to turn the user's location into a province name (`src/features/triage/location.ts`). Coordinates stay on the device.

- Source: "Indonesia GeoJSON & TopoJSON Maps (38 Provinces)" by Deny Herianto,
  https://github.com/denyherianto/indonesia-geojson-topojson-maps-with-38-provinces
  (`GeoJSON/indonesia-38-provinces.geojson`, version 1.0.0)
- License: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
- Changes: kept only the province name (`PROVINSI`) and polygons, rounded coordinates to 3 decimals (about 100 m), stored rings as flat `[lon, lat, …]` lists. Format: `[{ "n": name, "p": [[ring, …], …] }]`.

The boundaries are simplified. `location.ts` counts a point within 25 km of a province's edge as that province, so coastal towns are still found.
