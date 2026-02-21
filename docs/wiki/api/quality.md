
# Quality

Enum that controls the resolution of polygons downloaded from the IBGE mesh API.

```python
from geodata import Quality
```

---

## Values

| Member   | API value         | Description                                          |
| -------- | ----------------- | ---------------------------------------------------- |
| `LOW`    | `"minima"`        | Lowest resolution — smallest files, fastest download |
| `MEDIUM` | `"intermediaria"` | Intermediate resolution                              |
| `HIGH`   | `"maxima"`        | Highest resolution — most accurate boundaries        |

---

## When to use each level

| Situation                           | Recommended quality |
| ----------------------------------- | ------------------- |
| General visualisations / dashboards | `LOW`               |
| Regional analyses                   | `MEDIUM`            |
| Points near borders                 | `HIGH`              |
| Cartographic publications           | `HIGH`              |

---

## Usage

```python
from geodata import GeoData, GeoLevel, Quality

# Fast download for exploration
states = GeoData(GeoLevel.STATE, Quality.LOW)

# High-accuracy download for analysis
states_hq = GeoData(GeoLevel.STATE, Quality.HIGH)
```
