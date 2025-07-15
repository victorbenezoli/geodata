"""
This module provides the GeoDataBase class for handling geospatial data.
"""

import geopandas as gpd
import pandas as pd
import requests

from geodata.core.geolevel import GeoLevel
from geodata.core.quality import Quality

URL_SPATIAL: str = "https://servicodados.ibge.gov.br/api/v3/malhas"
URL_METADATA: str = "https://servicodados.ibge.gov.br/api/v1/localidades"


class GeoDataBase:
    """
    GeoDataBase class to handle geospatial data.

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

    def __repr__(self):
        """Return a string representation of the GeoData instance."""
        return f"GeoData(geolevel={self.geolevel}, quality={self.quality})"

    def __str__(self):
        """Return a string representation of the GeoData instance."""
        return f"GeoData: {self.geolevel.spatial} - {self.quality.value}"

    def _fetch_polygons(self) -> gpd.GeoDataFrame:
        """
        Get the polygons of the spatial data.

        Returns
        -------
        gpd.GeoDataFrame
            The polygons of the spatial data.
        """
        url = f"{URL_SPATIAL}/paises/BR"
        params = {
            "intrarregiao": self.geolevel.spatial.value,
            "qualidade": self.quality.value,
            "formato": "application/vnd.geo+json",
        }
        if self.geolevel.spatial == "paises":
            params.pop("intrarregiao")
        with requests.Session() as session:
            response = session.get(url, params=params)
            response.raise_for_status()
            data = (
                gpd.GeoDataFrame.from_features(response.json())
                .set_axis(["geometry", "id"], axis=1)
                .reindex(columns=["id", "geometry"])
                .assign(
                    id=lambda df: 1
                    if self.geolevel.spatial.value == "paises"
                    else df.id
                )
                .astype({"id": int})
            )
        return data

    def _fetch_metadata(self) -> pd.DataFrame:
        """
        Get the metadata of the spatial data.

        Returns
        -------
        pd.DataFrame
            The metadata of the spatial data.
        """
        url = f"{URL_METADATA}/{self.geolevel.metadata.value}"
        params = {"view": "nivelado"}
        with requests.Session() as session:
            response = session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        return pd.DataFrame.from_dict(data)

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
                        if x.endswith("id") and not x.startswith(self.geolevel.spatial)
                    ]
                )
            )
            .pipe(
                lambda df: df.set_axis(
                    [
                        (
                            x.split("-")[-1]
                            if x.startswith(self.geolevel.spatial)
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
        if self.geolevel.spatial == "paises":
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
