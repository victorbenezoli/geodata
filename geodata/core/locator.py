"""
Point-in-polygon localisation utilities for the ibge-geodata package.

This module provides :class:`GeoLocator`, which determines the administrative
division (state, municipality, region, etc.) that contains a given geographic
point by performing a spatial join against IBGE polygon data.

All results are resolved eagerly during construction (``__post_init__``) and
stored as plain instance attributes, with internal polygon layers cached to
avoid redundant API calls.

Typical usage
-------------
>>> from geodata.core.locator import GeoLocator
>>> from geodata.core.quality import Quality
>>> from geodata.utils.geocoords import GeoCoords
>>>
>>> brasilia = GeoCoords(lat=-15.7801, lon=-47.9292)
>>> locator  = GeoLocator(brasilia, quality=Quality.LOW)
>>>
>>> locator.state
'DF'
>>> locator.municipality
'Brasília'
"""

from __future__ import annotations

from dataclasses import dataclass, field

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

from geodata.core.base import GeoDataBase
from geodata.core.geolevel import GeoLevel
from geodata.core.quality import Quality
from geodata.utils.geocoords import GeoCoords


@dataclass(repr=False)
class GeoLocator:
    """
    Locate the administrative divisions that contain a geographic point.

    All results are resolved eagerly in ``__post_init__`` and stored as plain
    instance attributes.  Polygon layers are fetched from the IBGE API during
    construction and cached internally to avoid redundant requests.

    Parameters
    ----------
    coords : GeoCoords
        The geographic point to locate.
    quality : Quality, optional
        Polygon resolution used when downloading IBGE boundaries.
        Lower quality means faster downloads; higher quality means more
        accurate boundaries near complex coastlines / state borders.
        Defaults to :attr:`Quality.LOW`.

    Attributes
    ----------
    coords : GeoCoords
        The geographic point supplied at construction time.
    quality : Quality
        The polygon resolution used for boundary data.
    state : str or None
        Abbreviation (sigla) of the matching state (UF), or ``None`` if the
        point is outside Brazil.
    municipality : str or None
        Name of the matching municipality, or ``None``.
    region : str or None
        Name of the matching macro-region, or ``None``.
    intermediate_region : str or None
        Name of the matching intermediate region, or ``None``.
    immediate_region : str or None
        Name of the matching immediate region, or ``None``.

    Examples
    --------
    >>> locator = GeoLocator(GeoCoords(lat=-15.7801, lon=-47.9292))
    >>> locator.state
    'DF'
    >>> locator.municipality
    'Brasília'
    >>> locator.region
    'Centro-Oeste'
    """

    coords: GeoCoords = field(repr=False)
    quality: Quality = field(default=Quality.LOW, repr=False)

    _cache: dict[GeoLevel, gpd.GeoDataFrame] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )
    _point: Point = field(
        default=None,  # type: ignore[assignment]
        init=False,
        repr=False,
    )
    municipality: str | None = field(
        default=None,
        init=False,
        repr=True,
    )
    state: str | None = field(
        default=None,
        init=False,
        repr=True,
    )
    region: str | None = field(
        default=None,
        init=False,
        repr=True,
    )
    intermediate_region: str | None = field(
        default=None,
        init=False,
        repr=True,
    )
    immediate_region: str | None = field(
        default=None,
        init=False,
        repr=True,
    )

    def __post_init__(self) -> None:
        """Resolve all administrative levels eagerly on construction."""
        self._point = self.coords.to_shapely_point()
        self.state = self._abbreviation(GeoLevel.STATE)
        self.municipality = self._name(GeoLevel.MUNICIPALITY)
        self.region = self._name(GeoLevel.REGION)
        self.intermediate_region = self._name(GeoLevel.INTERMEDIATE_REGION)
        self.immediate_region = self._name(GeoLevel.IMMEDIATE_REGION)

    def __str__(self) -> str:
        return (
            f"GeoLocator(coords={self.coords}, "
            f"state={self.state}, municipality={self.municipality}, "
            f"region={self.region}, intermediate_region={self.intermediate_region}, "
            f"immediate_region={self.immediate_region})"
        )

    def __repr__(self) -> str:
        return self.__str__()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _polygons(self, geolevel: GeoLevel) -> gpd.GeoDataFrame:
        """
        Return the polygon layer for *geolevel*, downloading it if necessary.

        Parameters
        ----------
        geolevel : GeoLevel
            The administrative level whose boundaries are required.

        Returns
        -------
        geopandas.GeoDataFrame
            Polygon layer with metadata columns merged in.
        """
        if geolevel not in self._cache:
            self._cache[geolevel] = GeoDataBase(geolevel, self.quality).polygons
        return self._cache[geolevel]

    def _name(self, geolevel: GeoLevel) -> str | None:
        """
        Return the ``'nome'`` field of the matching polygon row.

        Parameters
        ----------
        geolevel : GeoLevel
            The administrative level to query.

        Returns
        -------
        str or None
            The name string, or ``None`` if no polygon contains the point.
        """
        row = self.locate(geolevel)
        return str(row["nome"]) if row is not None else None

    def _abbreviation(self, geolevel: GeoLevel) -> str | None:
        """
        Return the ``'sigla'`` field of the matching polygon row.

        Parameters
        ----------
        geolevel : GeoLevel
            The administrative level to query.

        Returns
        -------
        str or None
            The abbreviation string, or ``None`` if no polygon contains the point.
        """
        row = self.locate(geolevel)
        return str(row["sigla"]) if row is not None else None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def locate(self, geolevel: GeoLevel) -> pd.Series | None:
        """
        Find the administrative unit at *geolevel* that contains this point.

        Parameters
        ----------
        geolevel : GeoLevel
            The administrative level to query (e.g. ``GeoLevel.STATE``).

        Returns
        -------
        pandas.Series or None
            A Series with the metadata columns of the matching polygon
            (e.g. ``id``, ``nome``, ``sigla``), or ``None`` if no polygon
            contains the point (e.g. the point is offshore).

        Examples
        --------
        >>> locator = GeoLocator(GeoCoords(lat=-15.7801, lon=-47.9292))
        >>> locator.locate(GeoLevel.STATE)['nome']
        'Distrito Federal'
        """
        polygons = self._polygons(geolevel)

        candidates = polygons.sindex.query(self._point, predicate="within")
        if len(candidates) == 0:
            return None

        row: pd.Series = polygons.iloc[candidates[0]].drop(labels="geometry")  # type: ignore[assignment]
        return row
