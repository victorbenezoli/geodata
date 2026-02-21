<div style="width:40%;margin:0 auto 1rem;aspect-ratio:19/8;overflow:hidden;background:url('../assets/wiki/wiki_faq.png') center/100% auto no-repeat;"></div>

# FAQ

## Downloads are slow. How can I speed things up?

Use `Quality.LOW`. Municipality polygons at maximum quality can be several MB each.

```python
municipalities = GeoData(GeoLevel.MUNICIPALITY, Quality.LOW)
```

---

## `GeoLocator` returns `None` for a point inside Brazil

This usually happens for points very close to state borders when polygon quality is low. Use `Quality.HIGH`:

```python
loc = GeoLocator(coords, quality=Quality.HIGH)
```

---

## Can I use degree/minute/second coordinates?

`GeoCoords` expects decimal degrees. Convert first:

```python
def dms_to_dd(degrees, minutes, seconds, direction):
    dd = degrees + minutes / 60 + seconds / 3600
    return -dd if direction in ("S", "W") else dd

lat = dms_to_dd(15, 46, 47.9, "S")   # -15.7800
lon = dms_to_dd(47, 55, 45.1, "W")   # -47.9292
```

---

## The IBGE API is down. What happens?

`GeoDataBase` raises `requests.HTTPError`. You can catch and handle it:

```python
import requests
try:
    geodata = GeoData(GeoLevel.STATE, Quality.LOW)
    gdf = geodata.polygons
except requests.HTTPError as e:
    print(f"IBGE API error: {e}")
```

---

## How do I save polygons locally?

Use native GeoPandas methods:

```python
# GeoPackage (recommended)
states.polygons.to_file("states.gpkg", driver="GPKG")

# GeoJSON
states.polygons.to_file("states.geojson", driver="GeoJSON")

# Shapefile
states.polygons.to_file("states.shp")
```

---

## Can I reproject to SIRGAS 2000?

Yes, use GeoPandas `to_crs`. SIRGAS 2000 is `EPSG:4674`:

```python
gdf_sirgas = states.polygons.to_crs("EPSG:4674")
```
