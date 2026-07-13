"""
Custom exceptions for the ibge-geodata package.
"""


class GeoDataError(Exception):
    """Base exception for all geospatial data errors."""

    pass


class CacheError(GeoDataError):
    """Raised when cache operations fail."""

    pass


class FetchError(GeoDataError):
    """Raised when data fetching fails."""

    pass


class ValidationError(GeoDataError):
    """Raised when data validation fails."""

    pass


class APIError(GeoDataError):
    """Raised when API calls fail."""

    pass
