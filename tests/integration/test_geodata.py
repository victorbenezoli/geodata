"""Integration tests for GeoData class."""

import unittest

from geodata import GeoData, GeoLevel, Quality


class TestGeoData(unittest.TestCase):
    """Integration tests for GeoData initialization and data fetching."""

    def test_geodata_initialization(self):
        """Test that GeoData can be initialized with valid parameters."""
        geolevel = GeoLevel.REGION
        quality = Quality.HIGH
        geodata = GeoData(geolevel, quality)
        self.assertIsNotNone(geodata)
        self.assertEqual(geodata.geolevel.spatial.value, "regiao")
        self.assertEqual(geodata.quality.value, "maxima")

    def test_geodata_metadata(self):
        """Test that GeoData can fetch metadata from IBGE API."""
        geolevel = GeoLevel.REGION
        quality = Quality.HIGH
        geodata = GeoData(geolevel, quality)
        metadata = geodata.metadata["nome"].to_list()
        self.assertIn("Nordeste", metadata)


if __name__ == "__main__":
    unittest.main()
