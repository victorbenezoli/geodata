import unittest
from geodata import GeoData, types


class TestGeoData(unittest.TestCase):
    def test_geodata_initialization(self):
        geolevel = types.GeoLevel("region")
        quality = types.Quality("high")
        geodata = GeoData(geolevel, quality)
        self.assertIsNotNone(geodata)
        self.assertEqual(geodata.geolevel.spatial, "regiao")
        self.assertEqual(geodata.quality.level, "high")

    def test_geodata_metadata(self):
        geolevel = types.GeoLevel("region")
        quality = types.Quality("high")
        geodata = GeoData(geolevel, quality)
        metadata = geodata.metadata["nome"].to_list()
        self.assertIn("Nordeste", metadata)

if __name__ == '__main__':
    unittest.main()
