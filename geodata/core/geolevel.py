from enum import Enum, StrEnum


class SpatialLevel(StrEnum):
    """
    SpatialLevel class to represent the spatial level of the data.

    Attributes
    ----------
    COUNTRY : str
        The country level of the spatial data.
    REGION : str
        The region level of the spatial data.
    INTERMEDIATE_REGION : str
        The intermediate region level of the spatial data.
    IMMEDIATE_REGION : str
        The immediate region level of the spatial data.
    STATE : str
        The state level of the spatial data.
    MUNICIPALITY : str
        The municipality level of the spatial data.
    """

    COUNTRY = "paises"
    REGION = "regiao"
    INTERMEDIATE_REGION = "intermediaria"
    IMMEDIATE_REGION = "imediata"
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
    INTERMEDIATE_REGION : str
        The intermediate region level of the metadata.
    IMMEDIATE_REGION : str
        The immediate region level of the metadata.
    STATE : str
        The state level of the metadata.
    MUNICIPALITY : str
        The municipality level of the metadata.
    """

    COUNTRY = "paises"
    REGION = "regioes"
    INTERMEDIATE_REGION = "regioes-intermediarias"
    IMMEDIATE_REGION = "regioes-imediatas"
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
    INTERMEDIATE_REGION : tuple
        The intermediate region level of the spatial data.
    IMMEDIATE_REGION : tuple
        The immediate region level of the spatial data.
    STATE : tuple
        The state level of the spatial data.
    MUNICIPALITY : tuple
        The municipality level of the spatial data.
    """

    COUNTRY = (
        SpatialLevel.COUNTRY,
        Metadata.COUNTRY,
    )
    REGION = (
        SpatialLevel.REGION,
        Metadata.REGION,
    )
    INTERMEDIATE_REGION = (
        SpatialLevel.INTERMEDIATE_REGION,
        Metadata.INTERMEDIATE_REGION,
    )
    IMMEDIATE_REGION = (
        SpatialLevel.IMMEDIATE_REGION,
        Metadata.IMMEDIATE_REGION,
    )
    STATE = (
        SpatialLevel.STATE,
        Metadata.STATE,
    )
    MUNICIPALITY = (
        SpatialLevel.MUNICIPALITY,
        Metadata.MUNICIPALITY,
    )

    def __init__(self, spatial: SpatialLevel, metadata: Metadata):
        self.spatial = spatial
        self.metadata = metadata

    def __repr__(self):
        return f"GeoLevel.{self.name}"

    def __str__(self):
        return self.__repr__()
