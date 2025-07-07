"""
This module contains data classes for representing the quality and
geographical level of spatial data.
"""

from enum import StrEnum, Enum


class Quality(StrEnum):
    """
    Quality class to represent the quality of the spatial data.

    Attributes
    ----------
    LOW : str
        The low quality level of the spatial data.
    MEDIUM : str
        The medium quality level of the spatial data.
    HIGH : str
        The high quality level of the spatial data.
    """
    LOW = "minima"
    MEDIUM = "intermediaria"
    HIGH = "maxima"


class SpatialLevel(StrEnum):
    """
    SpatialLevel class to represent the spatial level of the data.

    Attributes
    ----------
    COUNTRY : str
        The country level of the spatial data.
    REGION : str
        The region level of the spatial data.
    STATE : str
        The state level of the spatial data.
    MUNICIPALITY : str
        The municipality level of the spatial data.
    """
    COUNTRY = "paises"
    REGION = "regiao"
    STATE = "UF"
    MUNICIPALITY = "municipio"

    def __repr__(self) -> str:
        return f"SpatialLevel.{self.name}"
    
    def __str__(self) -> str:
        return self.__repr__()


class Metadata(StrEnum):
    """
    Metadata class to represent the metadata level of the data.

    Attributes
    ----------
    COUNTRY : str
        The country level of the metadata.
    REGION : str
        The region level of the metadata.
    STATE : str
        The state level of the metadata.
    MUNICIPALITY : str
        The municipality level of the metadata.
    """
    COUNTRY = "paises"
    REGION = "regioes"
    STATE = "estados"
    MUNICIPALITY = "municipios"

    def __repr__(self) -> str:
        return f"Metadata.{self.name}"
    
    def __str__(self) -> str:
        return self.__repr__()


class GeoLevel(Enum):
    """
    GeoLevel class to represent the geographical level of the data.

    Attributes
    ----------
    COUNTRY : tuple
        The country level of the spatial data.
    REGION : tuple
        The region level of the spatial data.
    STATE : tuple
        The state level of the spatial data.
    MUNICIPALITY : tuple
        The municipality level of the spatial data.
    """
    COUNTRY = (SpatialLevel.COUNTRY, Metadata.COUNTRY)
    REGION = (SpatialLevel.REGION, Metadata.REGION)
    STATE = (SpatialLevel.STATE, Metadata.STATE)
    MUNICIPALITY = (SpatialLevel.MUNICIPALITY, Metadata.MUNICIPALITY)

    def __init__(self, spatial: str, metadata: str):
        self.spatial = spatial
        self.metadata = metadata

    def __repr__(self):
        return f"GeoLevel.{self.name}"
    
    def __str__(self):
        return self.__repr__()
