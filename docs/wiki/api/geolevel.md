<div style="width:40%;margin:0 auto 1rem;aspect-ratio:4/1;overflow:hidden;background:url('../../assets/wiki/wiki_api_reference.png') center/100% auto no-repeat;"></div>

# GeoLevel

Enum representing the geographic level of a territorial division.

```python
from geodata import GeoLevel
```

---

## Values

| Member                | `spatial`         | `metadata`                 | Description            |
| --------------------- | ----------------- | -------------------------- | ---------------------- |
| `COUNTRY`             | `"paises"`        | `"paises"`                 | Brazil (country level) |
| `REGION`              | `"regiao"`        | `"regioes"`                | Macro-regions          |
| `INTERMEDIATE_REGION` | `"intermediaria"` | `"regioes-intermediarias"` | Intermediate regions   |
| `IMMEDIATE_REGION`    | `"imediata"`      | `"regioes-imediatas"`      | Immediate regions      |
| `STATE`               | `"UF"`            | `"estados"`                | Federative units       |
| `MUNICIPALITY`        | `"municipio"`     | `"municipios"`             | Municipalities         |

---

## Member attributes

Each `GeoLevel` member exposes two sub-attributes used internally:

| Attribute   | Type           | Usage                                    |
| ----------- | -------------- | ---------------------------------------- |
| `.spatial`  | `SpatialLevel` | `intrarregiao` parameter of the mesh API |
| `.metadata` | `Metadata`     | URL segment of the localities API        |

---

## Usage

```python
from geodata import GeoData, GeoLevel, Quality

geodata = GeoData(GeoLevel.MUNICIPALITY, Quality.LOW)
print(geodata.polygons.head())
```

Iterate over all levels:

```python
for level in GeoLevel:
    print(level.name, level.spatial)
```
