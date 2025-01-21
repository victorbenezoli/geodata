"""
This module initializes the geodata package.
"""

import logging
import sys

import numpy as np
import pandas as pd

from .src.base import GeoDataBase as GeoData
from .src.core import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for required dependencies
REQUIRED_PACKAGES = ["numpy", "pandas"]

for package in REQUIRED_PACKAGES:
    try:
        __import__(package)
    except ImportError:
        logger.error("Required package '%s' is not installed.", package)
        sys.exit(1)

__all__ = ["GeoData", "types"]

__doc__ = """
geodata

This package provides classes for handling geospatial data.

Subpackages
-----------
core
    Core module for handling geospatial data.
base
    Base module for handling geospatial data.

Modules
-------
types
    Data classes for representing the quality and geographical level of spatial data.
GeoDataBase
    Class for handling geospatial data.

Examples
--------
>>> from geodata import GeoData, types
>>> geolevel = types.GeoLevel("region")
>>> quality = types.Quality("high")
>>> geodata = GeoData(geolevel, quality)
>>> geodata.metadata()
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
