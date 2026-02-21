<div style="width:40%;margin:0 auto 1rem;aspect-ratio:4/1;overflow:hidden;background:url('../../assets/wiki/wiki_api_reference.png') center/100% auto no-repeat;"></div>

# GeoLocator

Locates the administrative divisions that contain a geographic point.

```python
from geodata import GeoLocator, GeoLevel, Quality
from geodata.utils.geocoords import GeoCoords
```

---

## Constructor

```python
GeoLocator(coords: GeoCoords, quality: Quality = Quality.LOW)
```

| Parameter | Type        | Default       | Description                           |
| --------- | ----------- | ------------- | ------------------------------------- |
| `coords`  | `GeoCoords` | —             | Point to locate                       |
| `quality` | `Quality`   | `Quality.LOW` | Resolution of the downloaded polygons |

All attributes are resolved **eagerly** in `__post_init__`: polygons for every level are downloaded and the point-in-polygon test is performed immediately on construction.

---

## Attributes

| Attribute             | Type          | Description                              |
| --------------------- | ------------- | ---------------------------------------- |
| `coords`              | `GeoCoords`   | The point provided at construction time  |
| `quality`             | `Quality`     | Polygon resolution                       |
| `state`               | `str \| None` | State abbreviation (e.g. `'SP'`, `'DF'`) |
| `municipality`        | `str \| None` | Municipality name                        |
| `region`              | `str \| None` | Macro-region name                        |
| `intermediate_region` | `str \| None` | Intermediate region name                 |
| `immediate_region`    | `str \| None` | Immediate region name                    |

`None` is returned when the point falls outside Brazilian territory (e.g. at sea).

---

## Methods

### `locate`

```python
def locate(self, geolevel: GeoLevel) -> pd.Series | None
```

Returns the full metadata row of the polygon that contains the point at the given level.

```python
loc = GeoLocator(GeoCoords(lat=-15.7801, lon=-47.9292))
row = loc.locate(GeoLevel.STATE)
print(row["nome"])   # 'Distrito Federal'
print(row["sigla"])  # 'DF'
print(row["id"])     # 53
```

---

### `all_levels`

```python
def all_levels(self) -> dict[GeoLevel, pd.Series | None]
```

Returns a dictionary with results for all administrative levels.

```python
result = loc.all_levels()
for level, row in result.items():
    name = row["nome"] if row is not None else "—"
    print(f"{level.name}: {name}")
```

---

## Full example

```python
from geodata import GeoLocator, Quality
from geodata.utils.geocoords import GeoCoords

coords = GeoCoords(lat=-23.5505, lon=-46.6333)  # São Paulo
loc = GeoLocator(coords, quality=Quality.LOW)

print(loc.state)               # 'SP'
print(loc.municipality)        # 'São Paulo'
print(loc.region)              # 'Sudeste'
print(loc.intermediate_region)
print(loc.immediate_region)
```

!!! warning "Point near a border"
For points very close to state borders, use `Quality.HIGH` to ensure the
low-resolution geometry does not exclude the point.
