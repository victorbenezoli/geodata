"""
Point-in-polygon localisation utilities for the ibge-geodata package.

This module provides the :class:`GeoLocator`, a class for determining which IBGE
administrative divisions contain a given geographic coordinate (latitude and longitude).

Key features
------------
- **Multi-level localisation** — locate the municipality, state, region, intermediate region,
    and immediate region containing the point in a single query.
- **Cached polygon layers** — administrative boundary layers are loaded and cached on
    first use to optimise subsequent lookups.
- **Graceful handling of missing data** — if a point does not fall within any polygon
    at a given level, the corresponding attribute in the result will be set to None.

Typical usage
-------------
>>> from geodata.core import GeoLocator
>>> from geodata.utils.geocoords import GeoCoords
>>> locator = GeoLocator()
>>> coords = GeoCoords(lat=-15.7801, lon=-47.9292)
>>> location = locator.locate(coords)
>>> location.municipality
'Brasília'
>>> location.state
'Distrito Federal'
>>> location.region
'Centro-Oeste'
>>> location.intermediate_region
'Brasília'
>>> location.immediate_region
'Brasília'
"""

from __future__ import annotations

from dataclasses import dataclass

import geopandas as gpd

from geodata.core.base import GeoDataBase
from geodata.core.geolevel import GeoLevel
from geodata.core.quality import Quality
from geodata.utils.geocoords import GeoCoords


@dataclass
class GeoLocation:
    """
    Data class representing the administrative divisions containing a geographic point.

    Attributes
    ----------
    municipality : str | None
        The name of the municipality containing the point, or None if not found.
    state : str | None
        The name of the state containing the point, or None if not found.
    region : str | None
        The name of the region containing the point, or None if not found.
    intermediate_region : str | None
        The name of the intermediate region containing the point, or None if not found.
    immediate_region : str | None
        The name of the immediate region containing the point, or None if not found.

    """

    municipality: str | None
    state: str | None
    region: str | None
    intermediate_region: str | None
    immediate_region: str | None

    def to_dict(self) -> dict[str, str | None]:
        """
        Convert the GeoLocation to a dictionary.

        Returns
        -------
        dict[str, str | None]
            A dictionary representation of the GeoLocation.

        """
        return {
            "municipality": self.municipality,
            "state": self.state,
            "immediate_region": self.immediate_region,
            "intermediate_region": self.intermediate_region,
            "region": self.region,
        }


class GeoLocator:
    """
    Point-in-polygon locator for IBGE administrative boundaries.

    Parameters
    ----------
    quality : Quality, optional
        Desired quality level of the result (default: ``Quality.LOW``).

    Methods
    -------
    locate(coords: GeoCoords) -> GeoLocation
        Locate the administrative divisions containing the given geographic coordinates.

    Notes
    -----
    - The locator uses cached GeoDataFrames of the administrative boundaries for efficient lookups.
    - If a point does not fall within any polygon at a given level, the corresponding attribute
      in the result will be set to None.
    - Use lower quality levels for faster lookups with less detailed boundaries, and higher quality
      levels for more accurate results at the cost of performance.

    """

    def __init__(self, quality: Quality = Quality.LOW) -> None:
        """
        Initialize the GeoLocator with the specified quality level.

        Parameters
        ----------
        quality : Quality, optional
            Desired quality level of the result (default: ``Quality.LOW``).

        """
        self.quality = quality
        self._cache: dict[GeoLevel, gpd.GeoDataFrame] = self._load_layers()

    def _load_layers(self) -> dict[GeoLevel, gpd.GeoDataFrame]:
        """
        Load and cache the necessary polygon layers for point-in-polygon queries.

        Returns
        -------
        dict[GeoLevel, gpd.GeoDataFrame]
            A dictionary mapping GeoLevel to the corresponding GeoDataFrame.

        """
        return {
            GeoLevel.MUNICIPALITY: GeoDataBase(
                GeoLevel.MUNICIPALITY,
                self.quality,
            ).polygons,
            GeoLevel.STATE: GeoDataBase(
                GeoLevel.STATE,
                self.quality,
            ).polygons,
            GeoLevel.IMMEDIATE_REGION: GeoDataBase(
                GeoLevel.IMMEDIATE_REGION,
                self.quality,
            ).polygons,
            GeoLevel.INTERMEDIATE_REGION: GeoDataBase(
                GeoLevel.INTERMEDIATE_REGION,
                self.quality,
            ).polygons,
            GeoLevel.REGION: GeoDataBase(
                GeoLevel.REGION,
                self.quality,
            ).polygons,
        }

    def locate(self, coords: GeoCoords) -> GeoLocation:
        """
        Locate the administrative divisions containing the given geographic coordinates.

        Parameters
        ----------
        coords : GeoCoords
            Geographic coordinates (latitude and longitude) to locate.

        Returns
        -------
        GeoLocation
            A GeoLocation object containing the names of the located administrative divisions.

        """
        point = coords.to_shapely_point()
        geolocation = GeoLocation(
            municipality=None,
            state=None,
            region=None,
            intermediate_region=None,
            immediate_region=None,
        )

        for level in GeoLevel:
            layer = self._cache[level]
            match = layer[layer.geometry.contains(point)]
            if not match.empty:
                geolocation.__setattr__(level.value, match.iloc[0][level.value])

        return geolocation
