"""
Core module initialization.
"""

from .base import GeoDataBase as GeoData
from .geolevel import GeoLevel
from .quality import Quality

__all__ = ["Quality", "GeoLevel", "GeoData"]
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

"""
