# GeoData

`GeoData` is the main entry point for loading IBGE territorial meshes and aligned locality metadata.

```python
from geodata import GeoData, GeoLevel, Quality
```

## Constructor

```python
GeoData(geolevel: GeoLevel, quality: Quality)
```

| Parameter  | Type       | Description                                    |
| ---------- | ---------- | ---------------------------------------------- |
| `geolevel` | `GeoLevel` | Territorial level to fetch                     |
| `quality`  | `Quality`  | Polygon resolution requested from the mesh API |

## Properties

### `metadata`

```python
@property
def metadata(self) -> pd.DataFrame
```

Returns a plain `DataFrame` from the IBGE localities endpoint. Columns are normalised so the requested level is exposed with a predictable shape such as `id`, `nome`, `sigla`, and parent administrative fields when available.

```python
states = GeoData(GeoLevel.STATE, Quality.LOW)
print(states.metadata[["id", "nome", "sigla"]].head())
```

### `polygons`

```python
@property
def polygons(self) -> gpd.GeoDataFrame
```

Returns a merged `GeoDataFrame` containing geometry plus metadata aligned by `id`.

```python
states = GeoData(GeoLevel.STATE, Quality.LOW)
gdf = states.polygons
print(gdf.columns)
```

For `GeoLevel.COUNTRY`, the result is a single polygon in `EPSG:4674`.

## Methods

### `plot`

```python
def plot(self, **kwargs) -> None
```

Convenience wrapper around `self.polygons.plot(**kwargs)`.

```python
states.plot(column="sigla", figsize=(12, 8), edgecolor="white")
```

## Notes

- Data is requested lazily when `metadata` or `polygons` is accessed.
- `polygons` triggers both geometry and metadata retrieval for non-country levels.
- CRS is preserved from the geometry payload when available, otherwise it falls back to `EPSG:4674`.

## Example

```python
from geodata import GeoData, GeoLevel, Quality

municipalities = GeoData(GeoLevel.MUNICIPALITY, Quality.MEDIUM)
print(len(municipalities.metadata))
print(municipalities.polygons.head())
```
