import unittest
from NDSTile import NDSTile
from NDSCoordinate import NDSCoordinate
from WGS84Coordinate import WGS84Coordinate
import logging

# Configure logging for tests, switch to logging.DEBUG for more detailed output
logging.basicConfig(level=logging.INFO)

class TestNDSTile(unittest.TestCase):
    """Test cases for the NDSTile class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Common test values
        self.level0_packed_id = 65536  # Level 0, tile 0 (East hemisphere)
        self.level0_packed_id_west = 65537  # Level 0, tile 1 (West hemisphere)
        self.level1_packed_id = 131072  # Level 1, tile 0
        self.level2_packed_id = 262144  # Level 2, tile 0
        
        # Test coordinates
        self.east_coord = NDSCoordinate(90.0, 45.0)  # East hemisphere
        self.west_coord = NDSCoordinate(-90.0, 45.0)  # West hemisphere
        self.wgs_east_coord = WGS84Coordinate(90.0, 45.0)  # East hemisphere
        self.wgs_west_coord = WGS84Coordinate(-90.0, 45.0)  # West hemisphere
    
    def test_constructor_packed_id(self):
        """Test constructor with packed ID."""
        # Test level 0 tiles
        tile = NDSTile(self.level0_packed_id)
        self.assertEqual(tile.level, 0)
        self.assertEqual(tile.tile_number, 0)
        
        tile = NDSTile(self.level0_packed_id_west)
        self.assertEqual(tile.level, 0)
        self.assertEqual(tile.tile_number, 1)
        
        # Test level 1 tile
        tile = NDSTile(self.level1_packed_id)
        self.assertEqual(tile.level, 1)
        self.assertEqual(tile.tile_number, 0)
        
        # Test level 2 tile
        tile = NDSTile(self.level2_packed_id)
        self.assertEqual(tile.level, 2)
        self.assertEqual(tile.tile_number, 0)
    
    def test_constructor_level_and_tile_number(self):
        """Test constructor with level and tile number."""
        # Test level 0 tiles
        tile = NDSTile(0, 0)  # East hemisphere
        self.assertEqual(tile.level, 0)
        self.assertEqual(tile.tile_number, 0)
        
        tile = NDSTile(0, 1)  # West hemisphere
        self.assertEqual(tile.level, 0)
        self.assertEqual(tile.tile_number, 1)
        
        # Test level 1 tile
        tile = NDSTile(1, 0)
        self.assertEqual(tile.level, 1)
        self.assertEqual(tile.tile_number, 0)
        
        # Test level 2 tile
        tile = NDSTile(2, 0)
        self.assertEqual(tile.level, 2)
        self.assertEqual(tile.tile_number, 0)
    
    def test_constructor_level_and_nds_coordinate(self):
        """Test constructor with level and NDSCoordinate."""
        # Test with East hemisphere coordinate
        tile = NDSTile(0, self.east_coord)
        self.assertEqual(tile.level, 0)
        self.assertEqual(tile.tile_number, 0)  # Should be in East hemisphere
        
        # Test with West hemisphere coordinate
        tile = NDSTile(0, self.west_coord)
        self.assertEqual(tile.level, 0)
        self.assertEqual(tile.tile_number, 1)  # Should be in West hemisphere
        
        # Test with higher level
        tile = NDSTile(2, self.east_coord)
        self.assertEqual(tile.level, 2)
        # Tile number depends on the coordinate's position in the grid
    
    def test_constructor_level_and_wgs84_coordinate(self):
        """Test constructor with level and WGS84Coordinate."""
        # Test with East hemisphere coordinate
        tile = NDSTile(0, self.wgs_east_coord)
        self.assertEqual(tile.level, 0)
        self.assertEqual(tile.tile_number, 0)  # Should be in East hemisphere
        
        # Test with West hemisphere coordinate
        tile = NDSTile(0, self.wgs_west_coord)
        self.assertEqual(tile.level, 0)
        self.assertEqual(tile.tile_number, 1)  # Should be in West hemisphere
        
        # Test with higher level
        tile = NDSTile(2, self.wgs_east_coord)
        self.assertEqual(tile.level, 2)
        # Tile number depends on the coordinate's position in the grid
    
    def test_constructor_invalid_inputs(self):
        """Test constructor with invalid inputs."""
        # Test invalid level (negative)
        with self.assertRaises(ValueError):
            NDSTile(-1, 0)
        
        # Test invalid level (too high)
        with self.assertRaises(ValueError):
            NDSTile(NDSTile.MAX_LEVEL + 1, 0)
        
        # Test invalid tile number (negative)
        with self.assertRaises(ValueError):
            NDSTile(0, -1)
        
        # Test invalid tile number (too high for level)
        with self.assertRaises(ValueError):
            NDSTile(1, 8)  # Level 1 only allows tile numbers 0-7
        
        # Test invalid packed ID
        with self.assertRaises(ValueError):
            NDSTile(1)  # No level bit present
    
    def test_packed_id(self):
        """Test packed_id() method."""
        # Test level 0 tiles
        tile = NDSTile(0, 0)
        self.assertEqual(tile.packed_id(), self.level0_packed_id)
        
        tile = NDSTile(0, 1)
        self.assertEqual(tile.packed_id(), self.level0_packed_id_west)
        
        # Test level 1 tile
        tile = NDSTile(1, 0)
        self.assertEqual(tile.packed_id(), self.level1_packed_id)
        
        # Test level 2 tile
        tile = NDSTile(2, 0)
        self.assertEqual(tile.packed_id(), self.level2_packed_id)
        
        # Test round-trip conversion
        original_packed_id = 262154  # Level 2 in southern hemisphere
        tile = NDSTile(original_packed_id)
        self.assertEqual(tile.packed_id(), original_packed_id)
    
    def test_contains(self):
        """Test contains() method."""
        # Test level 0 East hemisphere tile
        east_tile = NDSTile(0, 0)
        self.assertTrue(east_tile.contains(self.east_coord))
        self.assertFalse(east_tile.contains(self.west_coord))
        
        # Test level 0 West hemisphere tile
        west_tile = NDSTile(0, 1)
        self.assertTrue(west_tile.contains(self.west_coord))
        self.assertFalse(west_tile.contains(self.east_coord))
        
        # Test with higher level tile
        high_level_tile = NDSTile(5, self.east_coord)
        self.assertTrue(high_level_tile.contains(self.east_coord))
        
        # Test with a coordinate just outside the tile
        # Create a coordinate that's slightly offset from the original
        slightly_offset = NDSCoordinate(90.1, 45.1)
        self.assertFalse(high_level_tile.contains(slightly_offset))
    
    def test_get_center(self):
        """Test get_center() method."""
        # Test level 0 East hemisphere tile
        east_tile = NDSTile(0, 0)
        center = east_tile.get_center()
        self.assertIsInstance(center, NDSCoordinate)
        self.assertEqual(center.longitude, NDSCoordinate.MAX_LONGITUDE // 2)
        self.assertEqual(center.latitude, 0)
        
        # Test level 0 West hemisphere tile
        west_tile = NDSTile(0, 1)
        center = west_tile.get_center()
        self.assertIsInstance(center, NDSCoordinate)
        self.assertEqual(center.longitude, NDSCoordinate.MIN_LONGITUDE // 2)
        self.assertEqual(center.latitude, 0)
        
        # Test with higher level tile
        high_level_tile = NDSTile(2, 0)
        center = high_level_tile.get_center()
        self.assertIsInstance(center, NDSCoordinate)
    
    def test_get_bbox(self):
        """Test get_bbox() method."""
        # Test level 0 East hemisphere tile
        east_tile = NDSTile(0, 0)
        bbox = east_tile.get_bbox()
        self.assertEqual(bbox.north, NDSCoordinate.MAX_LATITUDE)
        self.assertEqual(bbox.east, NDSCoordinate.MAX_LONGITUDE)
        self.assertEqual(bbox.south, NDSCoordinate.MIN_LATITUDE)
        self.assertEqual(bbox.west, 0)
        
        # Test level 0 West hemisphere tile
        west_tile = NDSTile(0, 1)
        bbox = west_tile.get_bbox()
        self.assertEqual(bbox.north, NDSCoordinate.MAX_LATITUDE)
        self.assertEqual(bbox.east, 0)
        self.assertEqual(bbox.south, NDSCoordinate.MIN_LATITUDE)
        self.assertEqual(bbox.west, NDSCoordinate.MIN_LONGITUDE)
        
        # Test with higher level tile
        high_level_tile = NDSTile(2, 0)
        bbox = high_level_tile.get_bbox()
        # The exact values depend on the tile's position, but we can check the type
        self.assertIsNotNone(bbox)
    
    def test_get_tile_grid_coordinates(self):
        """Test get_tile_grid_coordinates() method."""
        # Test level 0 East hemisphere tile
        east_tile = NDSTile(0, 0)
        coords = east_tile.get_tile_grid_coordinates()
        self.assertEqual(coords, [0, 0])
        
        # Test level 0 West hemisphere tile
        west_tile = NDSTile(0, 1)
        coords = west_tile.get_tile_grid_coordinates()
        self.assertEqual(coords, [-1, 0])
        
        # Test level 1 tiles
        for i in range(4):
            tile = NDSTile(1, i)
            coords = tile.get_tile_grid_coordinates()
            logging.debug(f"Tile {i}: {coords}")
            # Check that coordinates are within expected range for level 1
            self.assertTrue(-2 <= coords[0] <= 1)
            self.assertTrue(-1 <= coords[1] <= 0)
        
        # Test level 2 tiles
        for i in range(8):
            tile = NDSTile(2, i)
            coords = tile.get_tile_grid_coordinates()
            # Check that coordinates are within expected range for level 2
            self.assertTrue(-4 <= coords[0] <= 3)
            self.assertTrue(-2 <= coords[1] <= 1)
    
    def test_to_geojson(self):
        """Test to_geojson() method."""
        # Test that the method returns a string
        tile = NDSTile(0, 0)
        geojson = tile.to_geojson()
        self.assertIsInstance(geojson, str)
        
        # Check that the string contains expected GeoJSON elements
        self.assertIn('"type": "Feature"', geojson)
        self.assertIn('"type": "Polygon"', geojson)
        self.assertIn('"coordinates"', geojson)
    
    def test_south_west_as_morton(self):
        """Test south_west_as_morton() method."""
        # Test level 0 East hemisphere tile
        east_tile = NDSTile(0, 0)
        morton = east_tile.south_west_as_morton()
        self.assertIsInstance(morton, int)
        
        # Test level 0 West hemisphere tile
        west_tile = NDSTile(0, 1)
        morton = west_tile.south_west_as_morton()
        self.assertIsInstance(morton, int)
        
        # Test that the morton code shifts correctly with level
        level1_tile = NDSTile(1, 0)
        level2_tile = NDSTile(2, 0)
        self.assertEqual(level1_tile.south_west_as_morton() >> 2, level2_tile.south_west_as_morton() >> 4)
    
    def test_extract_level(self):
        """Test extract_level() method."""
        # Test level 0
        tile = NDSTile(0, 0)
        self.assertEqual(tile.extract_level(self.level0_packed_id), 0)
        
        # Test level 1
        self.assertEqual(tile.extract_level(self.level1_packed_id), 1)
        
        # Test level 2
        self.assertEqual(tile.extract_level(self.level2_packed_id), 2)
        
        # Test invalid packed ID
        self.assertEqual(tile.extract_level(1), -1)  # No level bit present
        
        # Test negative packed ID (should return MAX_LEVEL)
        self.assertEqual(tile.extract_level(-1), NDSTile.MAX_LEVEL)
    
    def test_level_15_tile(self):
        """Test functionality with level 15 tiles (maximum level)."""
        # Test constructor with level and tile number
        max_level = NDSTile.MAX_LEVEL
        self.assertEqual(max_level, 15, "MAX_LEVEL should be 15")
        
        # Calculate a valid tile number for level 15
        # Level 15 allows tile numbers 0 to (2^31)-1
        max_tile_number = (1 << (2 * max_level + 1)) - 1
        
        # Test with a valid tile number
        tile = NDSTile(max_level, 0)  # Simplest tile number
        self.assertEqual(tile.level, max_level)
        self.assertEqual(tile.tile_number, 0)
        
        # Test with a larger valid tile number
        sample_tile_number = 1000000  # Some arbitrary large number within range
        tile = NDSTile(max_level, sample_tile_number)
        self.assertEqual(tile.level, max_level)
        self.assertEqual(tile.tile_number, sample_tile_number)
        
        # Test packed_id method
        level_bit = 1 << (16 + max_level)
        self.assertEqual(tile.packed_id(), sample_tile_number + level_bit)
        
        # Test constructor with packed ID
        packed_id = sample_tile_number + level_bit
        logging.debug(f"Packed ID: {packed_id}")
        tile_from_packed = NDSTile(packed_id)
        self.assertEqual(tile_from_packed.level, max_level)
        self.assertEqual(tile_from_packed.tile_number, sample_tile_number)
        
        # Test with coordinates
        coord = NDSCoordinate(90.0, 45.0)  # East hemisphere
        tile = NDSTile(max_level, coord)
        logging.debug(f"Packed ID: {tile.packed_id()}")
        self.assertEqual(tile.level, max_level)
        self.assertTrue(tile.contains(coord))
        
        # Test get_bbox method
        bbox = tile.get_bbox()
        self.assertIsNotNone(bbox)
        
        # Test get_center method
        center = tile.get_center()
        self.assertIsInstance(center, NDSCoordinate)
        
        # Test south_west_as_morton method
        morton = tile.south_west_as_morton()
        self.assertIsInstance(morton, int)
        
        # Test that the tile grid coordinates are within expected range for level 15
        coords = tile.get_tile_grid_coordinates()
        # For level 15, the range would be much larger than lower levels
        self.assertTrue(-(1 << max_level) <= coords[0] < (1 << max_level))
        self.assertTrue(-(1 << (max_level - 1)) <= coords[1] < (1 << (max_level - 1)))

if __name__ == '__main__':
    unittest.main()