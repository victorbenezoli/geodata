# GeoLocator

Locates the administrative divisions that contain a geographic point.

```python
from geodata import GeoLocator, Quality
from geodata.utils.geocoords import GeoCoords
```

---

## GeoLocator

### Constructor

```python
GeoLocator(quality: Quality = Quality.LOW)
```

| Parameter | Type      | Default       | Description                           |
| --------- | --------- | ------------- | ------------------------------------- |
| `quality` | `Quality` | `Quality.LOW` | Resolution of the downloaded polygons |

Polygon layers for all administrative levels are loaded and cached on construction, so repeated calls to `locate()` reuse the same in-memory data.

---

### Attributes

| Attribute | Type      | Description                                          |
| --------- | --------- | ---------------------------------------------------- |
| `quality` | `Quality` | Polygon resolution used when loading boundary layers |

---

### Methods

#### `locate`

```python
def locate(self, coords: GeoCoords) -> GeoLocation
```

Performs a point-in-polygon test for all administrative levels and returns a `GeoLocation` with the results.

| Parameter | Type        | Description                |
| --------- | ----------- | -------------------------- |
| `coords`  | `GeoCoords` | Geographic point to locate |

**Returns:** [`GeoLocation`](#geolocation)

```python
locator  = GeoLocator()
coords   = GeoCoords(lat=-15.7801, lon=-47.9292)  # Brasília
location = locator.locate(coords)

print(location.municipality)         # 'Brasília'
print(location.state)                # 'Distrito Federal'
print(location.region)               # 'Centro-Oeste'
print(location.intermediate_region)  # 'Brasília'
print(location.immediate_region)     # 'Brasília'
```

---

## GeoLocation

Data class returned by `GeoLocator.locate()`.

### Attributes

| Attribute             | Type          | Description                                                 |
| --------------------- | ------------- | ----------------------------------------------------------- |
| `municipality`        | `str \| None` | Municipality name, or `None` if the point is outside Brazil |
| `state`               | `str \| None` | State full name (e.g. `'São Paulo'`, `'Distrito Federal'`)  |
| `region`              | `str \| None` | Macro-region name (e.g. `'Sudeste'`, `'Centro-Oeste'`)      |
| `intermediate_region` | `str \| None` | Intermediate region name                                    |
| `immediate_region`    | `str \| None` | Immediate region name                                       |

`None` is returned for any level where the point falls outside all polygons (e.g. at sea or near a border gap).

---

### Methods

#### `to_dict`

```python
def to_dict(self) -> dict[str, str | None]
```

Serialises the `GeoLocation` to a plain dictionary.

```python
location.to_dict()
# {
#     "municipality":        "Brasília",
#     "state":               "Distrito Federal",
#     "immediate_region":    "Brasília",
#     "intermediate_region": "Brasília",
#     "region":              "Centro-Oeste",
# }
```

---

## Full example

```python
from geodata import GeoLocator, Quality
from geodata.utils.geocoords import GeoCoords

coords   = GeoCoords(lat=-23.5505, lon=-46.6333)  # São Paulo
locator  = GeoLocator(quality=Quality.LOW)
location = locator.locate(coords)

print(location.state)                # 'São Paulo'
print(location.municipality)         # 'São Paulo'
print(location.region)               # 'Sudeste'
print(location.intermediate_region)
print(location.immediate_region)

# Serialise to dict
print(location.to_dict())
```

!!! warning "Point near a border"
For points very close to state borders, use `Quality.HIGH` to ensure the
low-resolution geometry does not exclude the point.
