# geodata
`geodata` is a Python package designed to simplify the process of working with geographical data from the IBGE (Brazilian Geography and Statistic Institute) API.

# Features
- Loads vector data of Brazil's geographical divisions without the need to download files;
- Allows intuitive selection of the geographical division level and data resolution;
- Export the vector data to the desired format without the need for third-party software.

# Usage
```python
import geodata as gd

# Initialize the geodata object
geolevel = gd.GeoLevel.STATE
quality = gd.Quality.MEDIUM
geo = gd.GeoData(geolevel=level, quality=quality)

# Load the polygons data to a variable
data_pol = geo.polygons

# Load only metadata
data_meta = geo.metadata
```