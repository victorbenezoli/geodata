
# Examples

## Choropleth map of states

```python
import matplotlib.pyplot as plt
from geodata import GeoData, GeoLevel, Quality

states = GeoData(GeoLevel.STATE, Quality.LOW)

ax = states.polygons.plot(
    column="nome",
    cmap="tab20",
    figsize=(14, 10),
    legend=False,
    edgecolor="white",
    linewidth=0.4,
)
ax.set_title("Brazilian States", fontsize=16)
ax.axis("off")
plt.tight_layout()
plt.show()
```

---

## Locate multiple points

```python
from geodata import GeoLocator
from geodata.utils.geocoords import GeoCoords

points = {
    "Brasília":     GeoCoords(lat=-15.7801, lon=-47.9292),
    "São Paulo":   GeoCoords(lat=-23.5505, lon=-46.6333),
    "Manaus":       GeoCoords(lat=-3.1190,  lon=-60.0217),
    "Porto Alegre": GeoCoords(lat=-30.0346, lon=-51.2177),
}

locator = GeoLocator()
for city, coords in points.items():
    location = locator.locate(coords)
    print(f"{city}: {location.state} — {location.municipality} ({location.region})")
```

---

## Calculate distances between cities

```python
from geodata.utils.geocoords import GeoCoords

capitals = {
    "Brasília":     GeoCoords(lat=-15.7801, lon=-47.9292),
    "Recife":        GeoCoords(lat=-8.0539,  lon=-34.8811),
    "Porto Alegre": GeoCoords(lat=-30.0346, lon=-51.2177),
    "Belém":        GeoCoords(lat=-1.4558,  lon=-48.5044),
}

origin = capitals["Brasília"]
for dest, coords in capitals.items():
    if dest == "Brasília":
        continue
    dist = origin.distance_to(coords)
    bearing = origin.bearing_to(coords)
    print(f"Brasília → {dest}: {dist:.0f} km, bearing {bearing:.1f}°")
```

---

## Convert between geographic and UTM coordinates

```python
from geodata.utils.geocoords import GeoCoords

p = GeoCoords(lat=-15.7801, lon=-47.9292)

# WGS-84 → UTM zone 22S
easting, northing = p.to_utm("EPSG:32722")
print(f"E={easting:.0f}  N={northing:.0f}")

# UTM → WGS-84
q = GeoCoords.from_utm(easting, northing, "EPSG:32722")
print(q)  # ~15.780100°S, 47.929200°W
```

---

## Serialisation and JSON integration

```python
import json
from geodata.utils.geocoords import GeoCoords

p = GeoCoords(lat=-15.7801, lon=-47.9292)

# Export
payload = json.dumps(p.to_dict())

# Import
q = GeoCoords.from_dict(json.loads(payload))
assert p == q
```
