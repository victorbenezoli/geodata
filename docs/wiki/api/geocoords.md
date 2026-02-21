
# GeoCoords

Represents a validated WGS-84 geographic coordinate pair.

```python
from geodata.utils.geocoords import GeoCoords
```

---

## Constructor

```python
GeoCoords(lat: float, lon: float)
```

| Parameter | Valid range   | Description                  |
| --------- | ------------- | ---------------------------- |
| `lat`     | `[-90, 90]`   | Latitude in decimal degrees  |
| `lon`     | `[-180, 180]` | Longitude in decimal degrees |

Values are coerced to `float` automatically. Exceptions are raised for invalid inputs.

---

## Attributes

| Attribute | Type    | Description |
| --------- | ------- | ----------- |
| `lat`     | `float` | Latitude    |
| `lon`     | `float` | Longitude   |

---

## Alternative constructors

### `from_tuple`

```python
@staticmethod
def from_tuple(coords: tuple[float, float]) -> GeoCoords
```

```python
p = GeoCoords.from_tuple((-15.7801, -47.9292))
```

---

### `from_dict`

```python
@staticmethod
def from_dict(data: dict[str, float]) -> GeoCoords
```

```python
p = GeoCoords.from_dict({"lat": -15.7801, "lon": -47.9292})
```

---

### `from_utm`

```python
@staticmethod
def from_utm(easting: float, northing: float, source_crs: str) -> GeoCoords
```

```python
p = GeoCoords.from_utm(197055.0, 8254536.0, "EPSG:32722")
```

---

## Serialisation

### `to_tuple`

```python
(-15.7801, -47.9292) == GeoCoords(lat=-15.7801, lon=-47.9292).to_tuple()
```

### `to_dict`

```python
{"lat": -15.7801, "lon": -47.9292} == GeoCoords(lat=-15.7801, lon=-47.9292).to_dict()
```

### `to_utm`

```python
easting, northing = GeoCoords(lat=-15.7801, lon=-47.9292).to_utm("EPSG:32722")
```

### `to_shapely_point`

```python
point = GeoCoords(lat=-15.7801, lon=-47.9292).to_shapely_point()
# POINT (-47.9292 -15.7801)
```

---

## Geodesic calculations

### `distance_to`

Great-circle distance in km using the Haversine formula.

```python
brasilia = GeoCoords(lat=-15.7801, lon=-47.9292)
manaus   = GeoCoords(lat=-3.1190,  lon=-60.0217)

print(brasilia.distance_to(manaus))  # ~2689.6 km
```

### `bearing_to`

Initial bearing in degrees (0–360°), measured clockwise from true north.

```python
print(brasilia.bearing_to(manaus))  # ~322.0°
```

---

## String representation

```python
str(GeoCoords(lat=-15.7801, lon=-47.9292))
# '15.780100°S, 47.929200°W'
```
