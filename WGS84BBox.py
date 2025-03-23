class WGS84BBox:
    """
    A simple WGS84-format bounding box.
    
    @author Daniel Wirtz
    @since 20.02.2020
    """

    def __init__(self, north, east, south, west):
        """
        Initializes a new WGS84BBox instance.
        
        :param north: Northern boundary (latitude)
        :param east: Eastern boundary (longitude)
        :param south: Southern boundary (latitude)
        :param west: Western boundary (longitude)
        """
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def to_geojson(self):
        """
        Creates a GeoJSON representation of this bounding box as a "Polygon" feature.
        
        :return: A string representing the GeoJSON "Polygon" feature.
        """
        return (
            "{\n"
            '  "type": "Feature",\n'
            '  "properties": {},\n'
            '  "geometry": {\n'
            '    "type": "Polygon",\n'
            '    "coordinates": [\n'
            "      [\n"
            f"        [{self.west}, {self.south}],\n"
            f"        [{self.east}, {self.south}],\n"
            f"        [{self.east}, {self.north}],\n"
            f"        [{self.west}, {self.north}],\n"
            f"        [{self.west}, {self.south}]\n"
            "      ]\n"
            "    ]\n"
            "  }\n"
            "}"
        )