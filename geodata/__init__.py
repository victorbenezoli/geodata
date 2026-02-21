"""
This module initializes the geodata package.
"""

import logging
import sys

import numpy as np
import pandas as pd

from .core import GeoData, GeoLevel, GeoLocator, Quality

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for required dependencies
REQUIRED_PACKAGES = ["numpy", "pandas", "geopandas"]

for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        logger.error("Required package '%s' is not installed.", package)
        sys.exit(1)

__all__ = ["GeoData", "GeoLevel", "Quality", "GeoLocator"]

__doc__ = """
geodata

This package provides classes for handling geospatial data.

Subpackages
-----------
core
    Core module for handling geospatial data.

Modules
-------
GeoData
    Class for handling geospatial data.
GeoLevel
    Enum for geographical levels of spatial data.
Quality
    Enum for quality levels of spatial data.
GeoLocator
    Point-in-polygon locator for IBGE administrative boundaries.

Examples
--------
>>> import geodata as gd
>>> geolevel = gd.GeoLevel("region")
>>> quality = gd.Quality("high")
>>> geodata = gd.GeoData(geolevel, quality)
>>> geodata.polygon
>>> geodata.metadata
>>> geodata.plot()
"""


# Validate package versions (optional)
def validate_package_versions():
    """
    Validate the versions of the required packages.
    """
    if np.__version__ < "1.18.0":
        logger.warning(
            "Numpy version is lower than 1.18.0. "
            "Some features may not work as expected."
        )
    if pd.__version__ < "1.0.0":
        logger.warning(
            "Pandas version is lower than 1.0.0. "
            "Some features may not work as expected."
        )


validate_package_versions()
