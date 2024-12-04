"""
This module contains data classes for representing the quality and
geographical level of spatial data.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Quality:
    """
    Quality class to represent the quality the spatial data.

    Attributes
    ----------
    level : Literal["low", "medium", "high"]
        The quality level of the spatial data.
    value : str
        The value of the quality level.
    """
    level: Literal["low", "medium", "high"]

    def __post_init__(self) -> None:
        if self.level not in ["low", "medium", "high"]:
            raise ValueError("Invalid quality name")

    def __repr__(self) -> str:
        return f"Quality: {self.level}"

    def __str__(self) -> str:
        return f"Quality: {self.level}"

    @property
    def value(self) -> str:
        """
        Return the value of the quality level.
        """
        match self.level:
            case "low":
                return "minima"
            case "medium":
                return "intermediaria"
            case "high":
                return "maxima"


@dataclass
class GeoLevel:
    """
    GeoLevel class to represent the geographical level of the spatial data.

    Attributes
    ----------
    geolevel : Literal["country", "region", "state", "municipality"]
        The geographical level of the spatial data.
    value : str
        The value of the geographical level.
    """
    geolevel: Literal["country", "region", "state", "municipality"]

    def __post_init__(self) -> None:
        if self.geolevel not in ["country", "region", "state", "municipality"]:
            raise ValueError("Invalid geolevel name")

    def __repr__(self) -> str:
        return f"GeoLevel: {self.geolevel}"

    def __str__(self) -> str:
        return f"GeoLevel: {self.geolevel}"

    @property
    def spatial(self) -> str:
        """
        Return the value of the geographical level for spatial data.
        """
        match self.geolevel:
            case "country":
                return "paises"
            case "region":
                return "regiao"
            case "state":
                return "UF"
            case "municipality":
                return "municipio"

    @property
    def metadata(self) -> str:
        """
        Return the value of the geographical level for metadata.
        """
        match self.geolevel:
            case "country":
                return "paises"
            case "region":
                return "regioes"
            case "state":
                return "estados"
            case "municipality":
                return "municipios"
