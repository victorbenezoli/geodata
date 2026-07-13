"""
Data models and type hints for the ibge-geodata package.

This module defines TypedDicts and other type definitions used for
type checking and documentation purposes.
"""

from typing import Any, TypedDict


class GeoJSONFeature(TypedDict, total=False):
    """GeoJSON Feature object."""

    type: str
    properties: dict[str, Any]
    geometry: dict[str, Any]


class GeoJSONFeatureCollection(TypedDict):
    """GeoJSON FeatureCollection object."""

    type: str
    features: list[GeoJSONFeature]


class MetadataRecord(TypedDict, total=False):
    """Metadata record from IBGE API."""

    id: int
    nome: str
    sigla: str
    regiao: dict[str, Any]
    UF: dict[str, Any]
