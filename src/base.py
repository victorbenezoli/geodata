"""
This module provides the GeoDataBase class for handling geospatial data.
"""

import geopandas as gpd
import pandas as pd
import requests
from src.core.types import GeoLevel, Quality

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

    Methods
    -------
    metadata()
        Get the metadata of the spatial data.
    polygons()
        Get the polygons of the spatial data.
    """
    def __init__(self, geolevel: GeoLevel, quality: Quality):
        self.geolevel = geolevel
        self.quality = quality

    def __polygons(self) -> gpd.GeoDataFrame:
        """
        Get the polygons of the spatial data.

        Returns
        -------
        gpd.GeoDataFrame
            The polygons of the spatial data.
        """
        url = f"{URL_SPATIAL}/paises/BR"
        params = {
            "intrarregiao": self.geolevel.spatial,
            "qualidade": self.quality.value,
            "formato": "application/vnd.geo+json",
        }
        with requests.Session() as session:
            response = session.get(url, params=params)
            response.raise_for_status()
            data = (
                gpd.GeoDataFrame.from_features(response.json())
                .set_axis(["geometry", "id"], axis=1)
                .reindex(columns=["id", "geometry"])
                .astype({"id": int})
            )
        return data

    @property
    def metadata(self) -> pd.DataFrame:
        """
        Get the metadata of the spatial data.

        Returns
        -------
        pd.DataFrame
            The metadata of the spatial data.
        """
        url = f"{URL_METADATA}/{self.geolevel.metadata}"
        params = {"view": "nivelado"}
        with requests.Session() as session:
            response = session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        meta = (
            pd.DataFrame.from_dict(data)
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
        polygons = self.__polygons()
        metadata = self.metadata()
        return metadata.merge(polygons, on="id")

    def plot(self, **kwargs) -> None:
        """
        Plot the polygons of the spatial data.

        Parameters
        ----------
        **kwargs
            Arbitrary keyword arguments for the plot method.
        """
        self.polygons.plot(**kwargs)
