# Quickstart

## Imports

```python
from geodata import GeoData, GeoLevel, Quality, GeoLocator
from geodata.utils.geocoords import GeoCoords
```

---

## 1. Download polygons and metadata

`GeoData` is the main entry point. Combine a `GeoLevel` with a `Quality`:

```python
# All Brazilian states at maximum quality
states = GeoData(GeoLevel.STATE, Quality.HIGH)

# GeoDataFrame with geometries + aligned metadata
print(states.polygons)

# Metadata only (id, nome, sigla, etc.)
print(states.metadata)
```

### Available levels

| `GeoLevel`            | Description                   |
| --------------------- | ----------------------------- |
| `COUNTRY`             | Country (Brazil)              |
| `REGION`              | Macro-regions (North, South…) |
| `INTERMEDIATE_REGION` | Intermediate regions          |
| `IMMEDIATE_REGION`    | Immediate regions             |
| `STATE`               | Federative units              |
| `MUNICIPALITY`        | Municipalities                |

### Available qualities

| `Quality` | Resolution                                 |
| --------- | ------------------------------------------ |
| `LOW`     | Minimum — smallest files, fastest download |
| `MEDIUM`  | Intermediate                               |
| `HIGH`    | Maximum — most accurate boundaries         |

---

## 2. Visualise

```python
import matplotlib.pyplot as plt

states.plot(column="nome", legend=False, figsize=(10, 8))
plt.title("Brazilian States")
plt.axis("off")
plt.show()
```

---

## 3. Work with coordinates

`GeoCoords` represents a validated WGS-84 coordinate pair:

```python
brasilia = GeoCoords(lat=-15.7801, lon=-47.9292)
manaus   = GeoCoords(lat=-3.1190,  lon=-60.0217)

# Distance in km (haversine)
print(brasilia.distance_to(manaus))   # ~2689.6 km

# Initial bearing in degrees
print(brasilia.bearing_to(manaus))    # ~322.0°

# Convert to UTM
easting, northing = brasilia.to_utm("EPSG:32722")
```

---

## 4. Locate a point

`GeoLocator` finds which administrative division a point belongs to:

```python
locator  = GeoLocator()
coords   = GeoCoords(lat=-15.7801, lon=-47.9292)
location = locator.locate(coords)

print(location.state)                # 'Distrito Federal'
print(location.municipality)         # 'Brasília'
print(location.region)               # 'Centro-Oeste'
print(location.intermediate_region)  # 'Brasília'
print(location.immediate_region)     # 'Brasília'

# Serialise to dict
print(location.to_dict())
```

!!! tip "Quality vs speed"
By default `GeoLocator` uses `Quality.LOW` to minimise download time.
For points near state borders, use `Quality.HIGH` to avoid false negatives.
