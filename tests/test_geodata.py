import unittest
from geodata import GeoData, Quality, GeoLevel


class TestGeoData(unittest.TestCase):
    def test_geodata_initialization(self):
        geolevel = GeoLevel.REGION
        quality = Quality.HIGH
        geodata = GeoData(geolevel, quality)
        self.assertIsNotNone(geodata)
        self.assertEqual(geodata.geolevel.spatial, "regiao")
        self.assertEqual(geodata.quality.value, "maxima")

    def test_geodata_metadata(self):
        geolevel = GeoLevel.REGION
        quality = Quality.HIGH
        geodata = GeoData(geolevel, quality)
        metadata = geodata.metadata["nome"].to_list()
        self.assertIn("Nordeste", metadata)

if __name__ == '__main__':
    unittest.main()
