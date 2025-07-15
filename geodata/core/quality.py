from enum import StrEnum


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

    def __repr__(self) -> str:
        return f"Quality.{self.name}"
    
    def __str__(self) -> str:
        return self.__repr__()