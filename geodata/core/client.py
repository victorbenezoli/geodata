"""
HTTP client for fetching geospatial data from IBGE APIs.

This module provides the HTTPClient class for handling API requests,
caching, and response processing.
"""

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import geopandas as gpd
import httpx
import pandas as pd
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
        return f"https://servicodados.ibge.gov.br/api/" f"v{self.version}/{self.name}"


@contextmanager
def _silence_httpx_logging():
    """Silencia temporariamente os logs INFO do httpx durante a sondagem de versões."""
    httpx_logger = logging.getLogger("httpx")
    previous_level = httpx_logger.level
    httpx_logger.setLevel(logging.WARNING)
    try:
        yield
    finally:
        httpx_logger.setLevel(previous_level)


class IBGEApiVersions:
    """
    Class to find the latest available versions of IBGE APIs.

    Attributes
    ----------
    meshes : ApiVersion
        The latest version of the "malhas" (meshes) API.
    metadata : ApiVersion
        The latest version of the "localidades" (metadata) API.
    """

    BASE_URL = "https://servicodados.ibge.gov.br/api"
    MAX_VERSION = 20

    def __init__(
        self,
        *,
        timeout: float = 10.0,
        client: httpx.Client | None = None,
    ):
        self._client = client or httpx.Client(timeout=timeout)

    def _exists(self, api: str, version: int) -> bool:
        """
        Check if a specific version of an IBGE API exists.

        Parameters
        ----------
        api : str
            The name of the API (e.g., "malhas" or "localidades").
        version : int
            The version number to check.

        Returns
        -------
        bool
            True if the API version exists, False otherwise.
        """
        url = f"{self.BASE_URL}/docs/{api}"

        try:
            response = self._client.get(
                url,
                params={"versao": version},
                follow_redirects=True,
            )
        except httpx.HTTPError:
            return False

        return response.status_code != 500

    def latest_version(self, api: str) -> ApiVersion:
        """
        Get the latest available version of a specific IBGE API.

        Parameters
        ----------
        api : str
            The name of the API (e.g., "malhas" or "localidades").

        Returns
        -------
        ApiVersion
            The latest available version of the specified API.
        Raises
        ------
        RuntimeError
            If the latest version of the API cannot be determined.
        """
        latest: int | None = None
        with _silence_httpx_logging():
            for version in range(1, self.MAX_VERSION + 1):
                if not self._exists(api, version):
                    break
                latest = version

        if latest is None:
            raise RuntimeError(f"Não foi possível descobrir a versão da API '{api}'.")

        return ApiVersion(name=api, version=latest)

    @cached_property
    def meshes(self) -> ApiVersion:
        """
        Get the latest available version of the "malhas" (meshes) API.
        """
        return self.latest_version("malhas")

    @cached_property
    def metadata(self) -> ApiVersion:
        """
        Get the latest available version of the "localidades" (metadata) API.
        """
        return self.latest_version("localidades")


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
        url_base = IBGEApiVersions().meshes.base_url
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
        url_base = IBGEApiVersions().metadata.base_url
        url = f"{url_base}/{self.geolevel.metadata.value}"
        params = {"view": METADATA_VIEW}
        with httpx.Client() as client:
            response = client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        return pd.DataFrame.from_dict(data)
