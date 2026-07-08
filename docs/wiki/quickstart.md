# Quickstart

This page covers the main workflows introduced in the current API: downloading IBGE layers, working with merged metadata, locating points, and using coordinate helpers.

## Imports

```python
from geodata import GeoData, GeoLevel, GeoLocator, Quality
from geodata.utils.geocoords import GeoCoords
```

## 1. Choose A Territorial Level

Every data request starts with a `GeoLevel` and a `Quality`.

```python
states = GeoData(GeoLevel.STATE, Quality.LOW)
municipalities = GeoData(GeoLevel.MUNICIPALITY, Quality.MEDIUM)
country = GeoData(GeoLevel.COUNTRY, Quality.HIGH)
```

| `GeoLevel`            | Meaning                                          |
| --------------------- | ------------------------------------------------ |
| `COUNTRY`             | Brazil as a single polygon                       |
| `REGION`              | North, Northeast, Central-West, Southeast, South |
| `INTERMEDIATE_REGION` | IBGE intermediate regions                        |
| `IMMEDIATE_REGION`    | IBGE immediate regions                           |
| `STATE`               | Federative units                                 |
| `MUNICIPALITY`        | Municipalities                                   |

| `Quality` | Trade-off                                   |
| --------- | ------------------------------------------- |
| `LOW`     | Fastest download and lowest geometry weight |
| `MEDIUM`  | Balanced option for analysis                |
| `HIGH`    | Highest fidelity, slower and heavier        |

## 2. Load Metadata Or Polygons

`GeoData` exposes two main views over the same IBGE source.

```python
states = GeoData(GeoLevel.STATE, Quality.LOW)

# Tabular metadata only
metadata = states.metadata
print(metadata[["id", "nome", "sigla"]].head())

# Merged metadata plus geometry
polygons = states.polygons
print(polygons[["id", "nome", "sigla", "geometry"]].head())
```

The `polygons` property returns a `GeoDataFrame` already aligned by `id`, so no extra merge step is needed.

## 3. Plot Directly

`GeoData.plot()` forwards keyword arguments to GeoPandas.

```python
import matplotlib.pyplot as plt

states.plot(
	column="sigla",
	figsize=(11, 8),
	edgecolor="white",
	linewidth=0.4,
	legend=False,
)
plt.title("Brazilian states")
plt.axis("off")
plt.show()
```

## 4. Validate Coordinates

`GeoCoords` keeps latitude and longitude in decimal degrees and validates them on construction.

```python
brasilia = GeoCoords(lat=-15.7801, lon=-47.9292)
print(brasilia.to_tuple())
print(brasilia.to_dict())
print(brasilia.to_shapely_point())
```

Alternative constructors are available when your input is not already a pair of named arguments.

```python
GeoCoords.from_tuple((-15.7801, -47.9292))
GeoCoords.from_dict({"lat": -15.7801, "lon": -47.9292})
```

## 5. Compute Distance, Bearing, And CRS Transforms

```python
manaus = GeoCoords(lat=-3.1190, lon=-60.0217)

print(round(brasilia.distance_to(manaus), 1))
print(round(brasilia.bearing_to(manaus), 1))

easting, northing = brasilia.to_utm("EPSG:32722")
restored = GeoCoords.from_utm(easting, northing, "EPSG:32722")
print(restored)
```

## 6. Locate Administrative Divisions

`GeoLocator` loads and caches boundary layers once, then reuses them for repeated point lookups.

```python
locator = GeoLocator(quality=Quality.LOW)
location = locator.locate(brasilia)

print(location.municipality)
print(location.state)
print(location.region)
print(location.intermediate_region)
print(location.immediate_region)
print(location.to_dict())
```

## 7. Reuse The Same Locator For Batch Queries

```python
locator = GeoLocator()

points = [
	GeoCoords(lat=-23.5505, lon=-46.6333),
	GeoCoords(lat=-30.0346, lon=-51.2177),
	GeoCoords(lat=-1.4558, lon=-48.5044),
]

for point in points:
	print(locator.locate(point).state)
```

!!! tip "Quality vs speed"
Use `Quality.LOW` for exploratory work and repeated lookups. If a point lies close to a border, retry with `Quality.HIGH`.
