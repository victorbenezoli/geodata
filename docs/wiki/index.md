<p align="center">
  <img src="assets/logo/horizontal/ibge-geodata-logo-horizontal.svg" alt="IBGE GeoData" style="max-width: 760px; width: 100%;" />
</p>

# ibge-geodata

[![PyPI](https://img.shields.io/pypi/v/ibge-geodata)](https://pypi.org/project/ibge-geodata/)
[![Python](https://img.shields.io/pypi/pyversions/ibge-geodata)](https://pypi.org/project/ibge-geodata/)
[![License](https://img.shields.io/badge/license-GPL-blue)](license.md)

ibge-geodata is a Python package for consuming Brazilian territorial data from IBGE with a workflow oriented around GeoPandas, validated coordinates, and reproducible administrative lookups.

## What Changed In 2.0

<div class="grid cards" markdown>

- :material-map-search-outline: **Unified territorial access**

  Load country, region, intermediate region, immediate region, state, or municipality layers from the same `GeoData` API.

- :material-database-sync-outline: **Merged metadata and geometry**

  Use `metadata` for plain tabular data or `polygons` for a merged `GeoDataFrame` keyed by `id`.

- :material-crosshairs-gps: **Reusable point locator**

  `GeoLocator` caches boundary layers and returns a structured `GeoLocation` object for repeated queries.

- :material-axis-arrow: **Coordinate utilities**

  `GeoCoords` validates latitude and longitude, computes distance and bearing, and converts between WGS-84 and projected CRS values.

</div>

## Install

```bash
pip install ibge-geodata
```

Requires Python 3.11 or newer.

## First Look

```python
from geodata import GeoData, GeoLevel, GeoLocator, Quality
from geodata.utils.geocoords import GeoCoords

states = GeoData(GeoLevel.STATE, Quality.LOW)
print(states.polygons[["id", "nome", "sigla"]].head())

locator = GeoLocator()
point = GeoCoords(lat=-15.7801, lon=-47.9292)
location = locator.locate(point)

print(location.state)
print(location.municipality)
print(location.to_dict())
```

## Main Concepts

| Object                            | Description                                                               |
| --------------------------------- | ------------------------------------------------------------------------- |
| [`GeoData`](api/geodata.md)       | Entry point for polygon download, metadata retrieval, and direct plotting |
| [`GeoLocator`](api/geolocator.md) | Point-in-polygon lookup across IBGE administrative layers                 |
| [`GeoCoords`](api/geocoords.md)   | Validated WGS-84 coordinate object with geodesic and CRS helpers          |
| [`GeoLevel`](api/geolevel.md)     | Enumeration of supported territorial levels                               |
| [`Quality`](api/quality.md)       | Resolution strategy for boundary downloads                                |

## Documentation Map

| Page                            | Use it for                                                     |
| ------------------------------- | -------------------------------------------------------------- |
| [Installation](install.md)      | Environment requirements and local setup                       |
| [Quickstart](quickstart.md)     | Core workflows with copy-paste examples                        |
| [Examples](examples.md)         | End-to-end snippets for maps, localisation, and CRS conversion |
| [FAQ](faq.md)                   | Performance, border cases, and export guidance                 |
| [Contributing](contributing.md) | Development workflow and project contribution                  |

## Why Use It

- It removes most of the boilerplate around IBGE mesh and locality endpoints.
- It keeps geometry and metadata aligned in a predictable tabular shape.
- It gives you a single coordinate model for validation, distance, bearing, and projection transforms.
- It makes repeated localisation practical by caching polygon layers inside the locator.
