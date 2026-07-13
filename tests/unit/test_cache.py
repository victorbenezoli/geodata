"""Tests for cache functionality."""

import os
import unittest
from pathlib import Path

from geodata import GeoData, GeoLevel, Quality


class TestCachePath(unittest.TestCase):
    """Tests for cache path generation and validation."""

    def test_cache_path_format(self):
        """Test that cache path has the correct format."""
        geolevel = GeoLevel.REGION
        quality = Quality.HIGH

        geodata = GeoData(geolevel, quality)
        cache_path = geodata._cache_path()

        # Check if path contains both geolevel and quality
        path_str = cache_path.as_posix()
        self.assertIn("regiao", path_str)
        self.assertIn("maxima", path_str)
        self.assertIn("geodata_cache", path_str)
        self.assertTrue(path_str.endswith(".sqlite"))

    def test_cache_directory_created(self):
        """Test that cache directory is created when _cache_path is called."""
        geolevel = GeoLevel.REGION
        quality = Quality.HIGH
        geodata = GeoData(geolevel, quality)

        cache_path = geodata._cache_path()

        # Verify directory was created
        self.assertTrue(cache_path.parent.exists())
        self.assertTrue(cache_path.parent.is_dir())

    def test_cache_path_different_levels(self):
        """Test that different geolevel/quality combinations produce different cache paths."""
        geodata1 = GeoData(GeoLevel.REGION, Quality.HIGH)
        geodata2 = GeoData(GeoLevel.STATE, Quality.HIGH)
        geodata3 = GeoData(GeoLevel.REGION, Quality.LOW)

        path1 = geodata1._cache_path().as_posix()
        path2 = geodata2._cache_path().as_posix()
        path3 = geodata3._cache_path().as_posix()

        # All paths should be different
        self.assertNotEqual(path1, path2)
        self.assertNotEqual(path1, path3)
        self.assertNotEqual(path2, path3)

        # Check that they contain the right geolevel names
        self.assertIn("regiao", path1)
        self.assertIn("UF", path2)
        self.assertIn("regiao", path3)

    def test_cache_path_uses_home_directory(self):
        """Test that cache path uses the home directory."""
        geolevel = GeoLevel.REGION
        quality = Quality.HIGH
        geodata = GeoData(geolevel, quality)

        cache_path = geodata._cache_path()
        home_dir = Path.home()

        # The cache path should be under the home directory
        self.assertTrue(str(cache_path).startswith(str(home_dir)))

    def test_cache_subdirectory_structure(self):
        """Test that cache uses the correct subdirectory structure."""
        geolevel = GeoLevel.REGION
        quality = Quality.HIGH
        geodata = GeoData(geolevel, quality)

        cache_path = geodata._cache_path()

        # Check the directory structure
        if os.name == "nt":  # Windows
            self.assertIn("AppData", str(cache_path))
            self.assertIn("Local", str(cache_path))
        else:  # Linux/Mac
            self.assertIn(".cache", str(cache_path))

    def test_cache_file_naming_convention(self):
        """Test that cache files follow the naming convention."""
        test_cases = [
            (GeoLevel.COUNTRY, Quality.HIGH),
            (GeoLevel.REGION, Quality.MEDIUM),
            (GeoLevel.STATE, Quality.LOW),
        ]

        for geolevel, quality in test_cases:
            geodata = GeoData(geolevel, quality)
            cache_path = geodata._cache_path()
            filename = cache_path.name

            # Filename should be: {spatial}_{quality}.sqlite
            self.assertIn(geolevel.spatial.value, filename)
            self.assertIn(quality.value, filename)
            self.assertTrue(filename.endswith(".sqlite"))


if __name__ == "__main__":
    unittest.main()
