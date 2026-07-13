"""
Cache management for geospatial data.

This module provides the CacheManager class for handling cache directory
creation, path management, and cleanup operations.
"""

import os
from pathlib import Path

from geodata.utils.constants import CACHE_DB_SUFFIX, CACHE_DIR_NAME


class CacheManager:
    """Manages cache paths and directory operations."""

    @staticmethod
    def get_cache_dir() -> Path:
        """
        Get the platform-specific cache directory.

        Returns
        -------
        Path
            The cache directory path.
        """
        if os.name == "nt":
            cache_dir = Path.home().joinpath("AppData", "Local", CACHE_DIR_NAME)
        else:
            cache_dir = Path.home().joinpath(".cache", CACHE_DIR_NAME)
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    @staticmethod
    def get_cache_path(geolevel_value: str, quality_value: str) -> Path:
        """
        Get the cache file path for a specific geolevel and quality combination.

        Parameters
        ----------
        geolevel_value : str
            The spatial level value.
        quality_value : str
            The quality value.

        Returns
        -------
        Path
            The cache file path.
        """
        cache_dir = CacheManager.get_cache_dir()
        filename = f"{geolevel_value}_{quality_value}{CACHE_DB_SUFFIX}"
        return cache_dir / filename

    @staticmethod
    def clear_cache(
        geolevel_value: str | None = None, quality_value: str | None = None
    ) -> int:
        """
        Clear cache files.

        If no parameters are provided, clears all cache files.
        If only geolevel_value is provided, clears caches for that level.
        If both parameters are provided, clears the specific cache file.

        Parameters
        ----------
        geolevel_value : str, optional
            The spatial level value to filter by.
        quality_value : str, optional
            The quality value to filter by.

        Returns
        -------
        int
            Number of cache files deleted.
        """
        cache_dir = CacheManager.get_cache_dir()
        if not cache_dir.exists():
            return 0

        deleted_count = 0
        for cache_file in cache_dir.glob(f"*{CACHE_DB_SUFFIX}"):
            if geolevel_value and quality_value:
                if f"{geolevel_value}_{quality_value}" in cache_file.name:
                    cache_file.unlink()
                    deleted_count += 1
            elif geolevel_value:
                if geolevel_value in cache_file.name:
                    cache_file.unlink()
                    deleted_count += 1
            else:
                cache_file.unlink()
                deleted_count += 1

        return deleted_count
