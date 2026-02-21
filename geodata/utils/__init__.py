from .geocoords import GeoCoords

__doc__ = """
geodata.utils
=============

Utility classes and functions for geospatial data handling.

Classes
-------
GeoCoords
    Lightweight, validated representation of WGS-84 geographic
    coordinates (latitude/longitude pairs).

Examples
--------
>>> from geodata.utils import GeoCoords
>>> coords = GeoCoords(latitude=-23.5505, longitude=-46.6333)
>>> coords
GeoCoords(latitude=-23.5505, longitude=-46.6333)
"""

__all__ = ["GeoCoords"]
