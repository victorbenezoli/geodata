"""
HTTP client for fetching geospatial data from IBGE APIs.

This module provides the HTTPClient class for handling API requests,
caching, and response processing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import geopandas as gpd
import httpx
import pandas as pd
from bs4 import BeautifulSoup
from hishel import SyncSqliteStorage
from hishel.httpx import SyncCacheClient

from geodata.core.enums import GeoLevel, Quality
from geodata.utils.constants import (
    DEFAULT_CACHE_TTL,
    GEOJSON_FORMAT,
    METADATA_VIEW,
)


@dataclass(frozen=True)
class ApiVersion:
    """
    Represents an API version for a specific IBGE API.

    Attributes
    ----------
    name : str
        The name of the API (e.g., "malhas" or "localidades").
    version : int
        The version number of the API.
    """

    name: str
    version: int

    @property
    def base_url(self) -> str:
        return f"https://servicodados.ibge.gov.br/api/v{self.version}/{self.name}"

    @staticmethod
    def find_latest_version(api_service_name: str) -> ApiVersion:
        with httpx.Client() as client:
            response = client.get("https://servicodados.ibge.gov.br/api/docs/")
            response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        api_link = next(
            (
                link
                for link in soup.select("a.headline")
                if link.get("id") == api_service_name
            ),
            None,
        )
        href = api_link.get("href") if api_link is not None else None
        if not isinstance(href, str) or not href:
            raise RuntimeError(
                f"Não foi possível descobrir a versão da API '{api_service_name}'."
            )

        version = parse_qs(urlparse(href).query).get("versao", ["1"])[0]
        try:
            latest = int(version)
        except ValueError as exc:
            raise RuntimeError(
                f"Não foi possível descobrir a versão da API '{api_service_name}'."
            ) from exc

        return ApiVersion(name=api_service_name, version=latest)


class HTTPClient:
    """HTTP client for fetching geospatial data from IBGE APIs."""

    def __init__(self, geolevel: GeoLevel, quality: Quality, cache_path: Path):
        """
        Initialize the HTTP client.

        Parameters
        ----------
        geolevel : GeoLevel
            The geographical level of the spatial data.
        quality : Quality
            The quality level of the spatial data.
        cache_path : Path
            Path to the cache database file.
        """
        self.geolevel = geolevel
        self.quality = quality
        self.cache_path = cache_path

    def fetch_polygons(self) -> gpd.GeoDataFrame:
        """
        Fetch polygon data from IBGE Spatial API with caching.

        Returns
        -------
        gpd.GeoDataFrame
            GeoDataFrame containing polygon geometries and IDs.

        Raises
        ------
        APIError
            If the API request fails.
        """
        url_base = ApiVersion.find_latest_version("malhas").base_url
        url = f"{url_base}/paises/BR"
        params = {
            "intrarregiao": self.geolevel.spatial.value,
            "qualidade": self.quality.value,
            "formato": GEOJSON_FORMAT,
        }
        if self.geolevel.spatial.value == "paises":
            params.pop("intrarregiao")

        cache_path_str = str(self.cache_path)
        with SyncCacheClient(
            storage=SyncSqliteStorage(
                database_path=cache_path_str,
                default_ttl=DEFAULT_CACHE_TTL,
            ),
        ) as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            data = (
                gpd.GeoDataFrame.from_features(response.json())
                .set_axis(["geometry", "id"], axis=1)
                .reindex(columns=["id", "geometry"])
                .assign(
                    id=lambda df: (
                        1 if self.geolevel.spatial.value == "paises" else df.id
                    )
                )
                .astype({"id": int})
            )
        return data

    def fetch_metadata(self) -> pd.DataFrame:
        """
        Fetch metadata from IBGE Metadata API.

        Returns
        -------
        pd.DataFrame
            DataFrame containing metadata for the given geographical level.

        Raises
        ------
        APIError
            If the API request fails.
        """
        url_base = ApiVersion.find_latest_version("localidades").base_url
        url = f"{url_base}/{self.geolevel.metadata.value}"
        params = {"view": METADATA_VIEW}
        with httpx.Client() as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        return pd.DataFrame.from_dict(data)
