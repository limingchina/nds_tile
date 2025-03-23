class WGS84Coordinate:
    """
    A simple class containing coordinates in WGS84 format.
    
    @see https://en.wikipedia.org/wiki/World_Geodetic_System
    @see https://earth-info.nga.mil/GandG/update/index.php?dir=wgs84&action=wgs84
    
    @author Daniel Wirtz
    @since 20.02.2020
    """

    def __init__(self, longitude, latitude):
        """
        Instantiates a new WGS84 coordinate.
        
        :param longitude: The longitude value within [-180, 180]
        :param latitude: The latitude value within [-90, 90]
        """
        if longitude < -180 or longitude > 180:
            raise ValueError(f"The longitude value {longitude} exceeds the valid range of [-180, 180].")
        if latitude < -90 or latitude > 90:
            raise ValueError(f"The latitude value {latitude} exceeds the valid range of [-90, 90].")
        self.longitude = longitude
        self.latitude = latitude

    def to_geojson(self):
        """
        Creates a GeoJSON "Point" feature representation of this coordinate.
        
        :return: A string representing the GeoJSON "Point" feature.
        """
        return (
            "{\n"
            '  "type": "Feature",\n'
            '  "properties": {},\n'
            '  "geometry": {\n'
            '    "type": "Point",\n'
            '    "coordinates": [\n'
            f'      {self.longitude}, {self.latitude}\n'
            "    ]\n"
            "  }\n"
            "}"
        )