# Installation

## Requirements

- Python 3.11 or newer
- Network access to IBGE APIs
- A working geospatial stack supported by GeoPandas on your platform

ibge-geodata targets Linux, macOS, and Windows.

## Install From PyPI

```bash
pip install ibge-geodata
```

## Install With Poetry

```bash
poetry add ibge-geodata
```

## Development Setup

```bash
git clone https://github.com/victorbenezoli/geodata.git
cd geodata
poetry install
```

If you plan to build the documentation locally, also install the docs dependency group.

```bash
poetry install --with docs
```

## Runtime Dependencies

| Package     | Purpose                                                     |
| ----------- | ----------------------------------------------------------- |
| `geopandas` | Polygon loading, CRS handling, plotting, and spatial tables |
| `requests`  | HTTP access to IBGE endpoints                               |
| `numpy`     | Numeric utilities used by the package                       |
| `pandas`    | Metadata tables                                             |
| `pyproj`    | Coordinate transformations used by `GeoCoords`              |
| `shapely`   | Point geometry and polygon containment                      |

## Verify The Installation

```python
from geodata import GeoData, GeoLevel, Quality

states = GeoData(GeoLevel.STATE, Quality.LOW)
print(states.metadata.head())
```

If this succeeds, the package, its dependencies, and IBGE connectivity are all working.
