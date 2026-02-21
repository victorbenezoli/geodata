"""
Geographic coordinate utilities for the ibge-geodata package.

This module provides the :class:`GeoCoords` dataclass, a lightweight, validated
representation of a WGS-84 geographic coordinate (latitude / longitude pair).

Key features
------------
- **Validation & coercion** — values are cast to ``float`` on construction and
  checked against the valid WGS-84 ranges (±90° lat, ±180° lon).
- **Multiple constructors** — create instances from tuples (:meth:`~GeoCoords.from_tuple`),
  dictionaries (:meth:`~GeoCoords.from_dict`), or projected UTM coordinates
  (:meth:`~GeoCoords.from_utm`).
- **Serialisation** — convert back to tuple (:meth:`~GeoCoords.to_tuple`) or
  dict (:meth:`~GeoCoords.to_dict`) for JSON-friendly output.
- **Geodesic computations** — great-circle distance in km (:meth:`~GeoCoords.distance_to`)
  and initial bearing in degrees (:meth:`~GeoCoords.bearing_to`).
- **UTM projection** — round-trip conversion to/from any projected CRS supported
  by ``pyproj`` (:meth:`~GeoCoords.to_utm`, :meth:`~GeoCoords.from_utm`),
  with transformers cached via :func:`functools.lru_cache` to minimise overhead.

Typical usage
-------------
>>> from geodata.utils.geocoords import GeoCoords
>>> brasilia = GeoCoords(lat=-15.7801, lon=-47.9292)
>>> manaus   = GeoCoords(lat=-3.1190, lon=-60.0217)
>>> round(brasilia.distance_to(manaus), 1)
2689.6
>>> round(brasilia.bearing_to(manaus), 1)
322.0
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import lru_cache

from pyproj import Transformer
from pyproj.exceptions import CRSError
from shapely.geometry import Point

_EARTH_RADIUS_KM: float = 6_371.0


@lru_cache(maxsize=32)
def _get_transformer(source_crs: str, target_crs: str) -> Transformer:
    """
    Return a cached Transformer to avoid repeated initialisation overhead.

    Parameters
    ----------
    source_crs : str
        The source coordinate reference system (e.g., ``'EPSG:4326'``).
    target_crs : str
        The target coordinate reference system (e.g., ``'EPSG:32722'``).

    Returns
    -------
    Transformer
        A pyproj Transformer object for the specified source and target CRS.

    Raises
    ------
    CRSError
        If either the source or target CRS is invalid.

    """
    return Transformer.from_crs(source_crs, target_crs, always_xy=True)


@dataclass(slots=True)
class GeoCoords:
    """
    A class to represent geographic coordinates with validation.

    Parameters
    ----------
    lat : float
        Latitude in degrees, must be between -90 and 90.
    lon : float
        Longitude in degrees, must be between -180 and 180.

    Raises
    ------
    TypeError
        If latitude or longitude are not numeric.
    ValueError
        If latitude is not between -90 and 90 degrees.
        If longitude is not between -180 and 180 degrees.

    """

    lat: float
    lon: float

    def __post_init__(self) -> None:
        try:
            self.lat = float(self.lat)
            self.lon = float(self.lon)
        except (TypeError, ValueError) as e:
            raise TypeError(
                f"Latitude and longitude must be numeric. Got: {self.lat!r}, {self.lon!r}"
            ) from e
        if not (-90 <= self.lat <= 90):
            raise ValueError(
                f"Latitude must be between -90 and 90 degrees. Got: {self.lat}"
            )
        if not (-180 <= self.lon <= 180):
            raise ValueError(
                f"Longitude must be between -180 and 180 degrees. Got: {self.lon}"
            )

    def __str__(self) -> str:
        ns = "N" if self.lat >= 0 else "S"
        ew = "E" if self.lon >= 0 else "W"
        return f"{abs(self.lat):.6f}°{ns}, {abs(self.lon):.6f}°{ew}"

    @staticmethod
    def from_tuple(coords: tuple[float, float]) -> GeoCoords:
        """
        Create a GeoCoords instance from a tuple of (latitude, longitude).

        Parameters
        ----------
        coords : tuple[float, float]
            A tuple containing (latitude, longitude).

        Returns
        -------
        GeoCoords
            An instance of GeoCoords created from the provided tuple.

        Raises
        ------
        ValueError
            If the input is not a tuple of length 2.
            If latitude or longitude values are out of valid ranges.
        """
        if not isinstance(coords, tuple) or len(coords) != 2:
            msg = f"Input must be a tuple of (latitude, longitude). Got: {coords!r}"
            raise ValueError(msg)
        return GeoCoords(lat=coords[0], lon=coords[1])

    @staticmethod
    def from_dict(data: dict[str, float]) -> GeoCoords:
        """
        Create a GeoCoords instance from a dictionary with ``'lat'`` and ``'lon'`` keys.

        Parameters
        ----------
        data : dict[str, float]
            A dictionary containing ``'lat'`` and ``'lon'`` keys.

        Returns
        -------
        GeoCoords
            An instance of GeoCoords.

        Raises
        ------
        KeyError
            If the ``'lat'`` or ``'lon'`` key is missing.
        ValueError
            If latitude or longitude values are out of valid ranges.
        """
        try:
            return GeoCoords(lat=data["lat"], lon=data["lon"])
        except KeyError as e:
            msg = f"Missing required key in coordinate dict: {e}"
            raise KeyError(msg) from e

    def to_tuple(self) -> tuple[float, float]:
        """
        Convert the GeoCoords instance to a tuple of (latitude, longitude).

        Returns
        -------
        tuple[float, float]
            A tuple containing (latitude, longitude).
        """
        return self.lat, self.lon

    def to_dict(self) -> dict[str, float]:
        """
        Convert the GeoCoords instance to a dictionary.

        Returns
        -------
        dict[str, float]
            A dictionary with ``'lat'`` and ``'lon'`` keys.
        """
        return {"lat": self.lat, "lon": self.lon}

    def distance_to(self, other: GeoCoords) -> float:
        """
        Compute the great-circle distance to another point (haversine formula).

        Parameters
        ----------
        other : GeoCoords
            The target coordinate.

        Returns
        -------
        float
            Distance in kilometres.
        """
        lat1, lon1 = math.radians(self.lat), math.radians(self.lon)
        lat2, lon2 = math.radians(other.lat), math.radians(other.lon)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        )
        return 2 * _EARTH_RADIUS_KM * math.asin(math.sqrt(a))

    def bearing_to(self, other: GeoCoords) -> float:
        """
        Compute the initial bearing (azimuth) to another point.

        Parameters
        ----------
        other : GeoCoords
            The target coordinate.

        Returns
        -------
        float
            Bearing in degrees (0–360), measured clockwise from north.
        """
        lat1 = math.radians(self.lat)
        lat2 = math.radians(other.lat)
        dlon = math.radians(other.lon - self.lon)
        x = math.sin(dlon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(
            lat2
        ) * math.cos(dlon)
        return (math.degrees(math.atan2(x, y)) + 360) % 360

    @staticmethod
    def from_utm(easting: float, northing: float, source_crs: str) -> GeoCoords:
        """
        Create a GeoCoords instance from UTM coordinates.

        Parameters
        ----------
        easting : float
            The easting value in UTM coordinates.
        northing : float
            The northing value in UTM coordinates.
        source_crs : str
            The coordinate reference system of the input UTM coordinates (e.g., ``'EPSG:32722'``).

        Returns
        -------
        GeoCoords
            An instance of GeoCoords created from the provided UTM coordinates.

        Raises
        ------
        ValueError
            If ``source_crs`` is invalid or the transformation fails.
        """
        try:
            transformer = _get_transformer(source_crs, "EPSG:4326")
            lon, lat = transformer.transform(easting, northing)
            return GeoCoords(lat=lat, lon=lon)
        except CRSError as e:
            msg = f"Invalid source CRS '{source_crs}': {e}"
            raise ValueError(msg) from e
        except Exception as e:
            msg = f"Error transforming UTM to geographic coordinates: {e}"
            raise ValueError(msg) from e

    def to_utm(self, target_crs: str) -> tuple[float, float]:
        """
        Convert the GeoCoords instance to UTM coordinates.

        Parameters
        ----------
        target_crs : str
            The coordinate reference system to convert to (e.g., ``'EPSG:32722'``).

        Returns
        -------
        tuple[float, float]
            A tuple containing (easting, northing) in UTM coordinates.

        Raises
        ------
        ValueError
            If ``target_crs`` is invalid or the transformation fails.
        """
        try:
            transformer = _get_transformer("EPSG:4326", target_crs)
            easting, northing = transformer.transform(self.lon, self.lat)
            return easting, northing
        except CRSError as e:
            msg = f"Invalid target CRS '{target_crs}': {e}"
            raise ValueError(msg) from e
        except Exception as e:
            msg = f"Error transforming geographic coordinates to UTM: {e}"
            raise ValueError(msg) from e

    def to_shapely_point(self) -> Point:
        """
        Convert the GeoCoords instance to a Shapely Point object.

        Returns
        -------
        shapely.geometry.Point
            A Point object representing the geographic coordinates.

        """
        return Point(self.lon, self.lat)
