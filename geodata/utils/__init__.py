from .constants import (
    CACHE_DB_SUFFIX,
    CACHE_DIR_NAME,
    DEFAULT_CACHE_TTL,
    GEOJSON_FORMAT,
    METADATA_VIEW,
)
from .exceptions import APIError, CacheError, FetchError, GeoDataError, ValidationError
from .geocoords import GeoCoords

__all__ = [
    "GeoCoords",
    # Constants
    "DEFAULT_CACHE_TTL",
    "CACHE_DIR_NAME",
    "CACHE_DB_SUFFIX",
    "GEOJSON_FORMAT",
    "METADATA_VIEW",
    # Exceptions
    "GeoDataError",
    "CacheError",
    "FetchError",
    "ValidationError",
    "APIError",
]

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
