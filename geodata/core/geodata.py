"""
This module provides the GeoData class for handling geospatial data.
"""

from pathlib import Path

import geopandas as gpd
import pandas as pd

from geodata.core.client import HTTPClient
from geodata.core.enums import GeoLevel, Quality
from geodata.storage import CacheManager


class GeoData:
    """
    GeoData class to handle geospatial data.

    Attributes
    ----------
    geolevel : GeoLevel
        The geographical level of the spatial data.
    quality : Quality
        The quality level of the spatial data.

    Properties
    ----------
    metadata : pd.DataFrame
        The metadata of the spatial data.
    polygons : gpd.GeoDataFrame
        The polygons of the spatial data.

    """

    def __init__(self, geolevel: GeoLevel, quality: Quality):
        self.geolevel = geolevel
        self.quality = quality
        self._client = HTTPClient(
            geolevel=geolevel,
            quality=quality,
            cache_path=self._cache_path(),
        )

    def __repr__(self):
        """Return a string representation of the GeoData instance."""
        return f"GeoData(geolevel={self.geolevel}, quality={self.quality})"

    def __str__(self):
        """Return a string representation of the GeoData instance."""
        return f"GeoData: {self.geolevel.spatial} - {self.quality.value}"

    def _cache_path(self) -> Path:
        """
        Get the cache path for the spatial data.

        Returns
        -------
        Path
            The cache path for the spatial data.
        """
        return CacheManager.get_cache_path(
            geolevel_value=self.geolevel.spatial.value,
            quality_value=self.quality.value,
        )

    def _fetch_polygons(self) -> gpd.GeoDataFrame:
        """
        Get the polygons of the spatial data.

        Returns
        -------
        gpd.GeoDataFrame
            The polygons of the spatial data.
        """
        return self._client.fetch_polygons()

    def _fetch_metadata(self) -> pd.DataFrame:
        """
        Get the metadata of the spatial data.

        Returns
        -------
        pd.DataFrame
            The metadata of the spatial data.
        """
        return self._client.fetch_metadata()

    @property
    def metadata(self) -> pd.DataFrame:
        """
        Get the metadata of the spatial data.

        Returns
        -------
        pd.DataFrame
            The metadata of the spatial data.
        """
        meta = (
            self._fetch_metadata()
            .pipe(
                lambda df: df.drop(
                    columns=[
                        x
                        for x in df.columns
                        if x.endswith("id") and not x.startswith(self.geolevel.spatial.value)
                    ]
                )
            )
            .pipe(
                lambda df: df.set_axis(
                    [
                        (
                            x.split("-")[-1]
                            if x.startswith(self.geolevel.spatial.value)
                            else x.replace("-nome", "")
                        )
                        for x in df.columns
                    ],
                    axis=1,
                )
            )
            .astype({"id": int})
        )
        return meta

    @property
    def polygons(self) -> gpd.GeoDataFrame:
        """
        Get the polygons of the spatial data.

        Returns
        -------
        gpd.GeoDataFrame
            The polygons of the spatial data.
        """
        polygons = self._fetch_polygons()
        if self.geolevel.spatial.value == "paises":
            return polygons.set_crs("EPSG:4674")
        metadata = self.metadata
        crs = polygons.crs if polygons.crs is not None else "EPSG:4674"
        return gpd.GeoDataFrame(metadata.merge(polygons, on="id")).set_crs(crs)

    def plot(self, **kwargs) -> None:
        """
        Plot the polygons of the spatial data.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments for the plot method.
        """
        self.polygons.plot(**kwargs)
