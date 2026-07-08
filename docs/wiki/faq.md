# FAQ

## Downloads are slow. How can I reduce startup time?

Use `Quality.LOW` whenever you do not need detailed borders. This matters most for municipality and regional layers.

```python
from geodata import GeoData, GeoLevel, Quality

municipalities = GeoData(GeoLevel.MUNICIPALITY, Quality.LOW)
```

## `GeoLocator` returned `None` for a point that should be inside Brazil

The most common cause is a coarse polygon layer near a border. Retry with `Quality.HIGH`.

```python
from geodata import GeoLocator, Quality

locator = GeoLocator(quality=Quality.HIGH)
location = locator.locate(coords)
```

## Does `GeoLocator` cache anything?

Yes. It loads all required polygon layers during construction and keeps them in memory for later `locate()` calls. If you need to resolve many points, reuse the same `GeoLocator` instance.

## Can I access metadata without downloading the merged polygon layer?

Yes. Use the `metadata` property.

```python
states = GeoData(GeoLevel.STATE, Quality.LOW)
print(states.metadata.head())
```

## Can I export the geometry to a local file?

Yes. `polygons` is a standard GeoPandas `GeoDataFrame`, so you can use GeoPandas writers directly.

```python
states.polygons.to_file("states.gpkg", driver="GPKG")
states.polygons.to_file("states.geojson", driver="GeoJSON")
```

## Can I use coordinates from another CRS?

Yes. Convert them to WGS-84 with `GeoCoords.from_utm()` when the source CRS is projected.

```python
from geodata.utils.geocoords import GeoCoords

coords = GeoCoords.from_utm(197055.0, 8254536.0, "EPSG:32722")
```

## Can I still work with degree-minute-second coordinates?

Yes, but convert them to decimal degrees before constructing `GeoCoords`.

```python
def dms_to_dd(degrees, minutes, seconds, direction):
    decimal = degrees + minutes / 60 + seconds / 3600
    return -decimal if direction in ("S", "W") else decimal
```

## What happens if the IBGE API is unavailable?

The request layer raises an HTTP exception from `requests`. Handle it in your application if you need retry or fallback logic.

```python
import requests
from geodata import GeoData, GeoLevel, Quality

try:
    states = GeoData(GeoLevel.STATE, Quality.LOW)
    polygons = states.polygons
except requests.HTTPError as exc:
    print(f"IBGE API error: {exc}")
```
