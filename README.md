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

- Typed API for all IBGE territorial levels
- Geometry as `GeoDataFrame` with metadata aligned by `id`
- Point-in-polygon localisation with `GeoLocator`
- Validated geographic coordinates with `GeoCoords`
- Geodesic distance and bearing calculations
- WGS-84 ↔ UTM coordinate conversion
- Quick plotting with `plot()`

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

# Polygons + metadata for all states
estados = GeoData(GeoLevel.STATE, Quality.LOW)
estados.plot()

# Locate a point
brasilia = GeoCoords(lat=-15.7801, lon=-47.9292)
loc = GeoLocator(brasilia)

print(loc.state)         # 'DF'
print(loc.municipality)  # 'Brasília'
print(loc.region)        # 'Centro-Oeste'

# Geodesic calculations
manaus = GeoCoords(lat=-3.1190, lon=-60.0217)
print(brasilia.distance_to(manaus))  # ~2689.6 km
print(brasilia.bearing_to(manaus))   # ~322.0°
```

---

## API (core)

| Class        | Description                                                                                   |
| ------------ | --------------------------------------------------------------------------------------------- |
| `GeoData`    | Main entry point — downloads polygons and metadata                                            |
| `GeoLocator` | Point-in-polygon locator for administrative divisions                                         |
| `GeoCoords`  | Validated WGS-84 coordinate with geodesic utilities                                           |
| `GeoLevel`   | Enum: `COUNTRY`, `REGION`, `INTERMEDIATE_REGION`, `IMMEDIATE_REGION`, `STATE`, `MUNICIPALITY` |
| `Quality`    | Enum: `LOW`, `MEDIUM`, `HIGH`                                                                 |

---

## Documentation

Full documentation at **[victorbenezoli.github.io/geodata](https://victorbenezoli.github.io/geodata)**.

---

## Requirements

- Python 3.11+

# Initialize the geodata object
geolevel = gd.GeoLevel.STATE
quality = gd.Quality.MEDIUM
geo = gd.GeoData(geolevel=geolevel, quality=quality)

## License

GPL. See [LICENSE.md](LICENSE.md).
