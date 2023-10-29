# jismeshcode

## About this Library

- This library is for handling regional mesh codes.
- Currently, it provides a function to convert mesh codes into rectangles as geodata (GeoJSON).

## Installation

- Environment
  - Python 3.8 or higher

```shell
pip install jismeshcode
```

## How to use

### mc2geojson

- Input
  - JIS mesh code (4, 6, 8, 9, 10, 11 digits)
- Output
  - Returns GeoJSON representing a polygon enclosing the area denoted by the mesh code.

```Python
>>> from jismeshcode.jismeshcode import mc2geojson
>>> mc2geojson(5439)
'{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[139, 36.0], [140, 36.0], [140, 36.666666666666664], [139, 36.666666666666664], [139, 36.0]]]}, "properties": {"meshcode": "5439"}}'
```
