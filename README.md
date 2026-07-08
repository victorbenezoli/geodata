<p align="center">
  <img src="docs/wiki/assets/logo/horizontal/ibge-geodata-logo-horizontal.svg" alt="IBGE GeoData" width="760" />
</p>

# ibge-geodata

[![PyPI](https://img.shields.io/pypi/v/ibge-geodata)](https://pypi.org/project/ibge-geodata/)
[![Python](https://img.shields.io/pypi/pyversions/ibge-geodata)](https://pypi.org/project/ibge-geodata/)
[![License](https://img.shields.io/badge/license-GPL-blue)](LICENSE.md)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-teal)](https://victorbenezoli.github.io/geodata)

Python package for downloading, organising, and querying Brazilian territorial data published by IBGE.

It combines administrative meshes, tabular metadata, point localisation, and coordinate utilities behind a small typed API.

## What Is Included

- Administrative polygons for country, region, intermediate region, immediate region, state, and municipality
- Metadata aligned by `id` in ready-to-use `DataFrame` and `GeoDataFrame` objects
- Point-in-polygon localisation across multiple IBGE levels with a reusable cached locator
- Validated WGS-84 coordinates with distance, bearing, shapely conversion, and UTM transforms
- One-line plotting through GeoPandas for quick exploratory maps

## Installation

```bash
pip install ibge-geodata
```

Python 3.11 or newer is required.

## Quick Example

```python
from geodata import GeoData, GeoLevel, GeoLocator, Quality
from geodata.utils.geocoords import GeoCoords

# Download polygons plus aligned metadata
states = GeoData(GeoLevel.STATE, Quality.LOW)
print(states.polygons[["id", "nome", "sigla"]].head())

# Plot directly with GeoPandas
states.plot(figsize=(10, 8), edgecolor="white", linewidth=0.4)

# Locate a point across administrative levels
locator = GeoLocator(quality=Quality.LOW)
brasilia = GeoCoords(lat=-15.7801, lon=-47.9292)
location = locator.locate(brasilia)

print(location.to_dict())
# {
#     'municipality': 'Brasília',
#     'state': 'Distrito Federal',
#     'immediate_region': 'Brasília',
#     'intermediate_region': 'Brasília',
#     'region': 'Centro-Oeste'
# }

# Geodesic utilities
manaus = GeoCoords(lat=-3.1190, lon=-60.0217)
print(round(brasilia.distance_to(manaus), 1))
print(round(brasilia.bearing_to(manaus), 1))

# CRS conversion
easting, northing = brasilia.to_utm("EPSG:32722")
restored = GeoCoords.from_utm(easting, northing, "EPSG:32722")
print(restored)
```

## Core API

| Object       | Purpose                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------ |
| `GeoData`    | Downloads IBGE meshes and returns metadata or merged polygon layers                        |
| `GeoLocator` | Resolves the municipality, state, region, and IBGE regional divisions that contain a point |
| `GeoCoords`  | Validates coordinates and provides geodesic and CRS conversion helpers                     |
| `GeoLevel`   | Enumerates supported territorial levels                                                    |
| `Quality`    | Controls mesh resolution and download weight                                               |

## Typical Workflows

### Download a territorial layer

```python
municipalities = GeoData(GeoLevel.MUNICIPALITY, Quality.MEDIUM)
gdf = municipalities.polygons
```

### Inspect metadata only

```python
states = GeoData(GeoLevel.STATE, Quality.LOW)
print(states.metadata.columns)
```

### Reuse a locator for many points

```python
locator = GeoLocator()

for coords in [
    GeoCoords(lat=-23.5505, lon=-46.6333),
    GeoCoords(lat=-30.0346, lon=-51.2177),
]:
    print(locator.locate(coords).state)
```

## Documentation

Full documentation: [victorbenezoli.github.io/geodata](https://victorbenezoli.github.io/geodata)

- Quickstart: practical usage patterns
- API reference: classes, enums, and return types
- Examples: mapping, localisation, and coordinate conversion
- FAQ: quality, performance, and persistence tips

## Data Sources

- IBGE Mesh API for polygons
- IBGE Localities API for administrative metadata

## License

GPL. See [LICENSE.md](LICENSE.md).
