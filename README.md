<p align="center">
  <img src="docs/assets/banner/readme_banner.png" alt="IBGE GeoData" width="600" />
</p>

# ibge-geodata

[![PyPI](https://img.shields.io/pypi/v/ibge-geodata)](https://pypi.org/project/ibge-geodata/)
[![Python](https://img.shields.io/pypi/pyversions/ibge-geodata)](https://pypi.org/project/ibge-geodata/)
[![License](https://img.shields.io/badge/license-GPL-blue)](LICENSE.md)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-teal)](https://victorbenezoli.github.io/geodata)

Python package to access and manipulate **Brazilian IBGE territorial geospatial data**.

---

## Highlights

- Typed API for all IBGE territorial levels (`COUNTRY` → `MUNICIPALITY`)
- Geometry as `GeoDataFrame` with metadata aligned by `id`
- Point-in-polygon localisation across all administrative levels with `GeoLocator`
- Validated WGS-84 coordinates with `GeoCoords`
- Geodesic distance and bearing calculations (haversine)
- WGS-84 ↔ UTM coordinate conversion via `pyproj`
- Quick plotting with `GeoDataFrame.plot()`

---

## Installation

```bash
pip install ibge-geodata
```

---

## Quickstart

```python
from geodata import GeoData, GeoLevel, Quality, GeoLocator
from geodata.utils.geocoords import GeoCoords

# Download polygons + metadata for all states
states = GeoData(GeoLevel.STATE, Quality.LOW)
states.plot()

# Locate a point across all administrative levels
locator  = GeoLocator()
brasilia = GeoCoords(lat=-15.7801, lon=-47.9292)
location = locator.locate(brasilia)

print(location.state)                # 'Distrito Federal'
print(location.municipality)         # 'Brasília'
print(location.region)               # 'Centro-Oeste'
print(location.intermediate_region)  # 'Brasília'
print(location.immediate_region)     # 'Brasília'

# Reuse the same locator for multiple points efficiently
manaus = GeoCoords(lat=-3.1190, lon=-60.0217)
print(locator.locate(manaus).state)  # 'Amazonas'

# Geodesic calculations
print(brasilia.distance_to(manaus))  # ~2689.6 km
print(brasilia.bearing_to(manaus))   # ~322.0°
```

---

## API

| Class        | Description                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------------- |
| `GeoData`    | Main entry point — downloads polygons and aligned metadata for a given level and quality       |
| `GeoLocator` | Point-in-polygon locator — returns a `GeoLocation` with all administrative divisions           |
| `GeoCoords`  | Validated WGS-84 coordinate pair with geodesic distance, bearing, and UTM conversion utilities |
| `GeoLevel`   | Enum: `COUNTRY`, `REGION`, `INTERMEDIATE_REGION`, `IMMEDIATE_REGION`, `STATE`, `MUNICIPALITY`  |
| `Quality`    | Enum: `LOW`, `MEDIUM`, `HIGH` — controls boundary resolution and download size                 |

---

## Documentation

Full documentation at **[victorbenezoli.github.io/geodata](https://victorbenezoli.github.io/geodata)**.

---

## Requirements

- Python 3.11+
- `geopandas`, `pyproj`, `shapely`, `requests`

---

## License

GPL. See [LICENSE.md](LICENSE.md).
