"""
Conftest for pytest - shared fixtures and configuration.
"""

import pytest


@pytest.fixture
def sample_geolevel():
    """Provide a sample GeoLevel for testing."""
    from geodata import GeoLevel

    return GeoLevel.REGION


@pytest.fixture
def sample_quality():
    """Provide a sample Quality for testing."""
    from geodata import Quality

    return Quality.HIGH


@pytest.fixture
def sample_geodata(sample_geolevel, sample_quality):
    """Provide a sample GeoData instance for testing."""
    from geodata import GeoData

    return GeoData(sample_geolevel, sample_quality)
