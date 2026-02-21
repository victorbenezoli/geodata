"""
Core module initialization.
"""

from .base import GeoDataBase as GeoData
from .geolevel import GeoLevel
from .locator import GeoLocator
from .quality import Quality

__all__ = ["Quality", "GeoLevel", "GeoData", "GeoLocator"]
__doc__ = """
geodata.core

This module provides core classes for handling geospatial data.

Classes
-------
GeoData
    Class for handling geospatial data.
GeoLevel
    Enum for geographical levels of spatial data.
Quality
    Enum for quality levels of spatial data.
GeoLocator
    Point-in-polygon locator for IBGE administrative boundaries.

"""
