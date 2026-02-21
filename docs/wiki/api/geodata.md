<div style="width:40%;margin:0 auto 1rem;aspect-ratio:4/1;overflow:hidden;background:url('../../assets/wiki/wiki_api_reference.png') center/100% auto no-repeat;"></div>

# GeoData

Main class for accessing IBGE territorial polygons and metadata.

```python
from geodata import GeoData, GeoLevel, Quality
```

---

## Constructor

```python
GeoData(geolevel: GeoLevel, quality: Quality)
```

| Parameter  | Type       | Description              |
| ---------- | ---------- | ------------------------ |
| `geolevel` | `GeoLevel` | Desired geographic level |
| `quality`  | `Quality`  | Polygon resolution       |

---

## Properties

### `polygons`

```python
@property
def polygons(self) -> gpd.GeoDataFrame
```

Returns a `GeoDataFrame` with geometries and all metadata joined by `id`.

```python
states = GeoData(GeoLevel.STATE, Quality.LOW)
gdf = states.polygons
print(gdf.columns)  # ['id', 'nome', 'sigla', ..., 'geometry']
```

---

### `metadata`

```python
@property
def metadata(self) -> pd.DataFrame
```

Returns metadata only (no geometry) from the IBGE localities API.

```python
meta = states.metadata
print(meta[["id", "nome", "sigla"]])
```

---

## Methods

### `plot`

```python
def plot(self, **kwargs) -> None
```

Shortcut for `self.polygons.plot(...)`. Accepts all GeoPandas/Matplotlib `plot` arguments.

```python
states.plot(column="nome", figsize=(12, 8))
```

---

## Representation

```python
repr(GeoData(GeoLevel.STATE, Quality.LOW))
# "GeoData(geolevel=GeoLevel.STATE, quality=Quality.LOW)"
```

```python
repr(GeoData(GeoLevel.STATE, Quality.LOW))
# "GeoData(geolevel=GeoLevel.STATE, quality=Quality.LOW)"
```
