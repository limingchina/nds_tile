from WGS84Coordinate import WGS84Coordinate
from PrintBinary import print_binary_representation
import logging

logger = logging.getLogger(__name__)

def to_signed_32bit(value):
    """
    Convert an integer to a signed 32-bit integer with proper overflow behavior.
    This emulates Java's 32-bit integer behavior in Python.
    """
    # Perform 32-bit masking and sign extension
    mask = 0xFFFFFFFF  # 32 bits of 1's
    value = value & mask  # Apply mask to get lowest 32 bits
    
    # If the highest bit is set (negative in two's complement)
    if value & 0x80000000:
        # Extend the sign by setting all the bits above bit 31 to 1
        value = value | ~mask
    
    return value

class NDSCoordinate:
    """
    Implementation of a NDS coordinate, according to the NDS Format Specification, Version 2.5.4, §7.2.1.
    
    The NDS coordinate encoding divides the 360° range into 2^32 steps.
    Consequently, each coordinate is represented by a pair of signed integers, where
    a coordinate unit corresponds to 360/2^32 = 90/2^30 degrees longitude/latitude
    (with their respective longitude [-180°,180°] and latitude [-90°,90°] ranges).
    
    Note: The integer range is not fully used encoding latitude values due to the half degree range.
    But this is done in favor of equally sized coordinate units along longitude/latitude.
    
    No warranties for correctness, use at own risk.
    """
    MAX_LONGITUDE = 2**31 - 1  # Integer.MAX_VALUE
    MIN_LONGITUDE = -(2**31)   # Integer.MIN_VALUE
    MAX_LATITUDE = MAX_LONGITUDE // 2
    MIN_LATITUDE = MIN_LONGITUDE // 2

    LONGITUDE_RANGE = MAX_LONGITUDE - MIN_LONGITUDE
    LATITUDE_RANGE = MAX_LATITUDE - MIN_LATITUDE

    def __init__(self, *args):
        """
        Constructor supports multiple signatures:
        1. NDSCoordinate(int longitude, int latitude)
        2. NDSCoordinate(double lon, double lat) - WGS84 coordinates
        3. NDSCoordinate(long ndsMortonCoordinates)
        """

        if len(args) == 2:
            if isinstance(args[0], int) and isinstance(args[1], int):  # (longitude, latitude)
                longitude, latitude = args
                latitude = to_signed_32bit(latitude)
                longitude = to_signed_32bit(longitude)
                longitude = min(longitude, self.MAX_LONGITUDE)
                latitude = min(latitude, self.MAX_LATITUDE)
                self.verify(longitude, latitude)
                self.longitude = longitude
                self.latitude = latitude
            elif isinstance(args[0], float) and isinstance(args[1], float):  # (lon, lat) in WGS84
                lon, lat = args
                if lon < -180 or lon > 180:
                    raise ValueError(f"The longitude value {lon} exceeds the valid range of [-180, 180].")
                if lat < -90 or lat > 90:
                    raise ValueError(f"The latitude value {lat} exceeds the valid range of [-90, 90].")
                self.latitude = int(lat / 180.0 * self.LATITUDE_RANGE)
                self.longitude = int(lon / 360.0 * self.LONGITUDE_RANGE)

        elif len(args) == 1:  # Morton code
            nds_morton_coordinates = args[0]
            lat = 0
            lon = 0
            for pos in range(32):
                if pos < 31 and (nds_morton_coordinates & (1 << (pos * 2 + 1))):
                    lat |= 1 << pos
                if nds_morton_coordinates & (1 << (pos * 2)):
                    lon |= 1 << pos

            # with NDS, the latitude value is considered a 31-bit signed integer.
            # hence, if the 31st bit is 1, this means we have a negative integer, requiring
            # to set the 32st bit to 1 for native java 32bit signed integers.
            if lat & (1 << 30):  # Handle negative latitude
                lat |= 1 << 31
            print_binary_representation(lat, "lat binary")
            print_binary_representation(lon, "lon binary")
            logger.debug("lat: %d, lon: %d", lat, lon)
            lat = to_signed_32bit(lat)
            lon = to_signed_32bit(lon)
            lon = min(lon, self.MAX_LONGITUDE)
            lat = min(lat, self.MAX_LATITUDE)
            self.verify(lon, lat)
            self.longitude = lon
            self.latitude = lat

    def verify(self, lon, lat):
        """
        Verifies that the given latitude and longitude are within valid ranges.
        """
        if lon < self.MIN_LONGITUDE or lon > self.MAX_LONGITUDE:
            raise ValueError(f"Longitude value {lon} exceeds allowed range [{self.MIN_LONGITUDE}, {self.MAX_LONGITUDE}].")
        if lat < self.MIN_LATITUDE or lat > self.MAX_LATITUDE:
            raise ValueError(f"Latitude value {lat} exceeds allowed range [{self.MIN_LATITUDE}, {self.MAX_LATITUDE}].")

    def add(self, delta_longitude, delta_latitude):
        """
        Adds an offset specified by two int values to the coordinate.
        Useful for NDS coordinate decoding using tile offsets.
        """
        return NDSCoordinate(self.longitude + delta_longitude, self.latitude + delta_latitude)

    def get_morton_code(self):
        """
        Returns the unique Morton code for this NDSCoordinate.
        """
        res = 0
        for pos in range(31):
            if self.longitude & (1 << pos):
                res |= 1 << (2 * pos)
            if pos < 31 and (self.latitude & (1 << pos)):
                res |= 1 << (2 * pos + 1)
        if self.longitude < 0:
            res |= 1 << 62
        if self.latitude < 0:
            res |= 1 << 61
        return res

    def to_wgs84(self):
        """
        Converts this coordinate to a WGS84 coordinate (using the "usual" longitude/latitude degree ranges).
        """
        lon = (self.longitude / self.MAX_LONGITUDE) * 180.0 if self.longitude >= 0 else (self.longitude / self.MIN_LONGITUDE) * -180.0
        lat = (self.latitude / self.MAX_LATITUDE) * 90.0 if (int)(self.latitude) >= 0 else ((int)(self.latitude) / self.MIN_LATITUDE) * -90.0
        return WGS84Coordinate(lon, lat)

    def to_geojson(self):
        """
        Creates a GeoJSON "Point" feature representation of this coordinate.
        """
        return self.to_wgs84().to_geojson()
