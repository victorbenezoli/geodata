<p align="center">
  <img src="../assets/banner/readme_banner.png" alt="IBGE GeoData" style="max-width:700px;" />
</p>

# ibge-geodata

[![PyPI](https://img.shields.io/pypi/v/ibge-geodata)](https://pypi.org/project/ibge-geodata/)
[![Python](https://img.shields.io/pypi/pyversions/ibge-geodata)](https://pypi.org/project/ibge-geodata/)
[![License](https://img.shields.io/badge/license-GPL-blue)](license.md)

**ibge-geodata** is a Python package to access and manipulate Brazilian IBGE territorial geospatial data directly in DataFrames and GeoDataFrames.

---

## What you can do

<div class="grid cards" markdown>

- :material-map-outline: **Territorial polygons**

  Download geometries for countries, regions, states, municipalities, and intermediate/immediate regions.

- :material-table: **Aligned metadata**

  IBGE localities API metadata automatically joined to geometries by `id`.

- :material-crosshairs-gps: **Point localisation**

  Find the state, municipality, and region that contain any geographic point.

- :material-chart-scatter-plot: **Quick visualisation**

  Generate maps in one line with `geodata.plot()`.

</div>

---

## Quick install

```bash
pip install ibge-geodata
```

---

## Minimal example

```python
from geodata import GeoData, GeoLevel, Quality, GeoLocator
from geodata.utils.geocoords import GeoCoords

# Polygons and metadata for all states
states = GeoData(GeoLevel.STATE, Quality.LOW)
states.plot()

# Locate a point
brasilia = GeoCoords(lat=-15.7801, lon=-47.9292)
loc = GeoLocator(brasilia)
print(loc.state)         # 'DF'
print(loc.municipality)  # 'Brasília'
```

---

## Navigation

| Page                            | Description                             |
| ------------------------------- | --------------------------------------- |
| [Installation](install.md)      | Requirements and setup instructions     |
| [Quickstart](quickstart.md)     | Practical guide with annotated examples |
| [API Reference](api/geodata.md) | Full documentation for all classes      |
| [Examples](examples.md)         | Real-world use cases                    |
| [FAQ](faq.md)                   | Frequently asked questions              |
| [Contributing](contributing.md) | How to contribute to the project        |

---

## API Reference

| Class                             | Description                                                               |
| --------------------------------- | ------------------------------------------------------------------------- |
| [`GeoData`](api/geodata.md)       | Downloads territorial polygons and metadata for a given level and quality |
| [`GeoLocator`](api/geolocator.md) | Finds the administrative divisions that contain a geographic point        |
| [`GeoCoords`](api/geocoords.md)   | Validated WGS-84 coordinate pair with geodesic utilities                  |
| [`GeoLevel`](api/geolevel.md)     | Enum of available geographic levels (country, state, municipality…)       |
| [`Quality`](api/quality.md)       | Enum controlling polygon resolution (low, medium, high)                   |
