<div style="width:40%;margin:0 auto 1rem;aspect-ratio:19/8;overflow:hidden;background:url('../assets/wiki/wiki_install.png') center/100% auto no-repeat;"></div>

# Installation

## Requirements

- Python **3.11** or higher
- Operating system: Linux, macOS, or Windows

## Via pip

```bash
pip install ibge-geodata
```

## Via Poetry

```bash
poetry add ibge-geodata
```

## Development installation

Clone the repository and install all development dependencies:

```bash
git clone https://github.com/victorbenezoli/geodata.git
cd geodata
poetry install
```

## Dependencies

| Package      | Minimum version | Purpose                                 |
| ------------ | --------------- | --------------------------------------- |
| `geopandas`  | 1.0             | GeoDataFrames and spatial operations    |
| `pyproj`     | —               | Coordinate reference system conversions |
| `shapely`    | —               | Geometries and point-in-polygon         |
| `requests`   | 2.32            | IBGE API calls                          |
| `numpy`      | 2.0             | Numerical operations                    |
| `pandas`     | —               | Metadata DataFrames                     |
| `matplotlib` | 3.10            | Map visualisation                       |

## Verification

```python
import geodata
print(geodata.__version__)
```
