<div style="width:40%;margin:0 auto 1rem;aspect-ratio:19/8;overflow:hidden;background:url('../assets/wiki/wiki_quickstart.png') center/100% auto no-repeat;"></div>

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
loc = GeoLocator(GeoCoords(lat=-15.7801, lon=-47.9292))

print(loc.state)               # 'DF'
print(loc.municipality)        # 'Brasília'
print(loc.region)              # 'Centro-Oeste'
print(loc.intermediate_region)
print(loc.immediate_region)

# Full metadata row for any level
print(loc.locate(GeoLevel.STATE))

# All levels at once
print(loc.all_levels())
```

!!! tip "Quality vs speed"
By default `GeoLocator` uses `Quality.LOW` to minimise download time.
For points near state borders, use `Quality.HIGH` to avoid false negatives.
