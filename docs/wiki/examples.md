# Examples

These examples focus on the workflows added or clarified in the current release: merged IBGE layers, reusable localisation, and coordinate transformations.

## Compare territorial levels

```python
from geodata import GeoData, GeoLevel, Quality

for level in [GeoLevel.REGION, GeoLevel.STATE, GeoLevel.MUNICIPALITY]:
    layer = GeoData(level, Quality.LOW)
    print(level.name, len(layer.metadata), len(layer.polygons))
```

## Build a state map

```python
import matplotlib.pyplot as plt
from geodata import GeoData, GeoLevel, Quality

states = GeoData(GeoLevel.STATE, Quality.LOW)

ax = states.polygons.plot(
    column="sigla",
    cmap="tab20",
    figsize=(14, 10),
    legend=False,
    edgecolor="white",
    linewidth=0.4,
)
ax.set_title("Brazilian states", fontsize=16)
ax.axis("off")
plt.tight_layout()
plt.show()
```

## Export a layer to GeoPackage

```python
from geodata import GeoData, GeoLevel, Quality

states = GeoData(GeoLevel.STATE, Quality.MEDIUM)
states.polygons.to_file("states.gpkg", driver="GPKG")
```

## Locate multiple cities with one cached locator

```python
from geodata import GeoLocator
from geodata.utils.geocoords import GeoCoords

points = {
    "Brasília": GeoCoords(lat=-15.7801, lon=-47.9292),
    "São Paulo": GeoCoords(lat=-23.5505, lon=-46.6333),
    "Manaus": GeoCoords(lat=-3.1190, lon=-60.0217),
    "Porto Alegre": GeoCoords(lat=-30.0346, lon=-51.2177),
}

locator = GeoLocator()

for city, coords in points.items():
    location = locator.locate(coords)
    print(f"{city}: {location.municipality} / {location.state} / {location.region}")
```

## Serialize localisation output

```python
import json
from geodata import GeoLocator
from geodata.utils.geocoords import GeoCoords

locator = GeoLocator()
location = locator.locate(GeoCoords(lat=-15.7801, lon=-47.9292))

payload = json.dumps(location.to_dict(), ensure_ascii=False)
print(payload)
```

## Calculate distances and bearings between capitals

```python
from geodata.utils.geocoords import GeoCoords

capitals = {
    "Brasília": GeoCoords(lat=-15.7801, lon=-47.9292),
    "Recife": GeoCoords(lat=-8.0539, lon=-34.8811),
    "Porto Alegre": GeoCoords(lat=-30.0346, lon=-51.2177),
    "Belém": GeoCoords(lat=-1.4558, lon=-48.5044),
}

origin = capitals["Brasília"]

for city, coords in capitals.items():
    if city == "Brasília":
        continue
    print(city, round(origin.distance_to(coords), 1), round(origin.bearing_to(coords), 1))
```

## Convert between WGS-84 and projected CRS

```python
from geodata.utils.geocoords import GeoCoords

point = GeoCoords(lat=-15.7801, lon=-47.9292)
easting, northing = point.to_utm("EPSG:32722")
restored = GeoCoords.from_utm(easting, northing, "EPSG:32722")

print((easting, northing))
print(restored)
```

## Create coordinates from external payloads

```python
from geodata.utils.geocoords import GeoCoords

from_tuple = GeoCoords.from_tuple((-15.7801, -47.9292))
from_dict = GeoCoords.from_dict({"lat": -15.7801, "lon": -47.9292})

assert from_tuple == from_dict
```
