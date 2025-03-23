
from NDSCoordinate import NDSCoordinate
from WGS84BBox import WGS84BBox

class NDSBBox:
    """
    Utility class for bounding boxes in NDS coordinates.
    
    For efficiency, this is implemented as a separate class instead of including this into NDSTile.
    """

    # Static constants for hemispheres
    WEST_HEMISPHERE = None  # Placeholder, initialized after NDSCoordinate is defined
    EAST_HEMISPHERE = None  # Placeholder, initialized after NDSCoordinate is defined

    def __init__(self, north, east, south, west):
        """
        Initializes a new NDSBBox instance.
        
        :param north: Northern boundary (latitude)
        :param east: Eastern boundary (longitude)
        :param south: Southern boundary (latitude)
        :param west: Western boundary (longitude)
        """
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def south_west(self):
        """
        Gets the south-west corner of the bounding box.
        
        :return: NDSCoordinate
        """
        return NDSCoordinate(self.west, self.south)

    def south_east(self):
        """
        Gets the south-east corner of the bounding box.
        
        :return: NDSCoordinate
        """
        return NDSCoordinate(self.east, self.south)

    def north_west(self):
        """
        Gets the north-west corner of the bounding box.
        
        :return: NDSCoordinate
        """
        return NDSCoordinate(self.west, self.north)

    def north_east(self):
        """
        Gets the north-east corner of the bounding box.
        
        :return: NDSCoordinate
        """
        return NDSCoordinate(self.east, self.north)

    def center(self):
        """
        Returns the center of the bounding box.
        
        :return: NDSCoordinate
        """
        return NDSCoordinate((self.east + self.west) // 2, (self.north + self.south) // 2)

    def to_wgs84(self):
        """
        Converts this bounding box to a WGS84-coordinate-based bounding box.
        
        :return: WGS84BBox
        """
        ne = self.north_east().to_wgs84()
        sw = self.south_west().to_wgs84()
        return WGS84BBox(ne.latitude, ne.longitude, sw.latitude, sw.longitude)

    def to_geojson(self):
        """
        Creates a GeoJSON representation of this bounding box as a "Polygon" feature.
        
        :return: String
        """
        return self.to_wgs84().to_geojson()


# Initialize static constants for hemispheres
NDSBBox.WEST_HEMISPHERE = NDSBBox(
    NDSCoordinate.MAX_LATITUDE, 0, NDSCoordinate.MIN_LATITUDE, NDSCoordinate.MIN_LONGITUDE
)
NDSBBox.EAST_HEMISPHERE = NDSBBox(
    NDSCoordinate.MAX_LATITUDE, NDSCoordinate.MAX_LONGITUDE, NDSCoordinate.MIN_LATITUDE, 0
)
