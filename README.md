# nds_tile

## Description

`nds_tile` is a Python implementation of the NDS Tile scheme, which follows the NDS Format Specification, Version 2.5.4, §7.3.1. This library provides functionality to create, manipulate, and query NDS tiles, which are a way of dividing the Earth's surface into hierarchical geographic regions.

## Features

- **Tile Initialization**: Create tiles using packed tile IDs, level and tile number, or coordinates.
- **Containment Check**: Check if a tile contains a given coordinate.
- **Packed ID Generation**: Generate packed tile IDs for tiles.
- **Center Calculation**: Calculate the center of a tile in NDSCoordinates.
- **Bounding Box Creation**: Create bounding boxes for tiles.
- **GeoJSON Conversion**: Convert tile data to GeoJSON format.

## Usage

Here is a basic example of how to use the class NDSTile:

```python
from NDSTile import NDSTile

# Create a tile using a packed ID
tile = NDSTile(65536)

# Get the packed ID of the tile
print(f"Tile ID: {tile.packed_id()}")

# Get the center of the tile in NDSCoordinates
center = tile.get_center()
print(f"Center in NDSCoordinates: {center.longitude}, {center.latitude}")

# Convert the center to GeoJSON, which will show the WGS84 coordinates
print(f"Center: {center.to_geojson()}")

# Get the bounding box of the tile in GeoJSON
print(f"Bounding Box: {tile.get_bbox().to_geojson()}")
```

If you want to use it as a command-line tool, the following command can be used:
```bash
python NDSTile.py 545666601 33801982
```
They are the tiles containing Berlin and Sydney, repsectively.
One can also add "--log_level debug" in the command line to see some log messages for debugging.

## Development

`nds_tile` is developed based on the Java implementation of NDS tiles available at [rondiplomatico/nds-tiles](https://github.com/rondiplomatico/nds-tiles). The goal of the Python port is to provide a similar set of functionalities in a language that is widely used for data science and geographic information systems.

https://oxidase.github.io/nds/# is useful to browse the NDS tiles on a map. One can also register an account on https://www.nds.live and
download packages from https://artifactory.nds-association.org/ui/repos/tree/General/tooling-pypi/ndsmath, which also contains python utilities for NDS tiles.

## Contributing

Contributions to `nds_tile` are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure that all code is well-documented and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open(https://github.com/limingchina/nds_tile/issues) an issue.

---

This README file provides an overview of the `NDSTile.py` project, its features, usage, and development guidelines. It serves as a starting point for users looking to integrate NDS tiles into their Python projects.