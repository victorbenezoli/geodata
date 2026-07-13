"""
Global constants for the ibge-geodata package.
"""

# Cache Configuration
DEFAULT_CACHE_TTL: int = 86400  # 1 day in seconds
CACHE_DIR_NAME: str = "geodata_cache"
CACHE_DB_SUFFIX: str = ".sqlite"

# GeoJSON Response Format
GEOJSON_FORMAT: str = "application/vnd.geo+json"
METADATA_VIEW: str = "nivelado"
