import json
from typing import Union

VALID_MESH_CODE_LENGTH = (4, 6, 8, 9, 10, 11)


def normalize_meshcode(meshcode):
    return ''.join(filter(lambda x: x.isdigit(), meshcode))

def mc2geojson(meshcode: Union[str, int]) -> str:

    if isinstance(meshcode, str):
        meshcode = normalize_meshcode(meshcode)

    # Convert meshcode to string if it's an integer
    if isinstance(meshcode, int):
        meshcode = str(meshcode)

    # Check the length of the meshcode to determine the mesh level
    mesh_level = len(meshcode)

    if mesh_level not in VALID_MESH_CODE_LENGTH:
        raise ValueError(f"meshcode length error length:{mesh_level} meshcode length must be within {VALID_MESH_CODE_LENGTH}")

    # Extract base latitude and longitude from the meshcode
    south_latitude = int(meshcode[:2]) / 1.5
    west_longitude = 100 + int(meshcode[2:4])
    
    # Initial latitude and longitude intervals for the first order mesh
    delta_latitude = 2/3  # 40 minutes in degrees
    delta_longitude = 1  # 1 degree
    
    if mesh_level >= 6:  # Apply adjustments for second order mesh
        delta_latitude = 1/12
        delta_longitude = 1/8
        south_latitude += int(meshcode[4]) * delta_latitude
        west_longitude += int(meshcode[5]) * delta_longitude
        
    if mesh_level >= 8:  # Apply adjustments for third order mesh
        delta_latitude = 1/120
        delta_longitude = 3/240
        south_latitude += int(meshcode[6]) * delta_latitude
        west_longitude += int(meshcode[7]) * delta_longitude
        
    if mesh_level >= 9:  # Apply adjustments for fourth order mesh
        if not int(meshcode[8]) in [1, 2, 3, 4]:
            raise ValueError(f"meshcode number error last number:The range of numbers in last number of forth meshcode must be from 1 to 4")
        
        delta_latitude = 15/3600
        delta_longitude = 22.5/3600
        south_latitude += [None, 0, 0, delta_latitude, delta_latitude][int(meshcode[8])]
        west_longitude += [None, 0, delta_longitude, 0, delta_longitude][int(meshcode[8])]

    if mesh_level >= 10:  # Apply adjustments for fifth order mesh
        if not int(meshcode[8]) in [1, 2, 3, 4]:
            raise ValueError(f"meshcode number error last number:The range of numbers in last number of forth meshcode must be from 1 to 4")
       
        delta_latitude = 7.5/3600  # 7.5 seconds in degrees
        delta_longitude = 11.25/3600  # 11.25 seconds in degrees
        south_latitude += [None, 0, 0, delta_latitude, delta_latitude][int(meshcode[9])]
        west_longitude += [None, 0, delta_longitude, 0, delta_longitude][int(meshcode[9])]
        
    if mesh_level == 11:  # Apply adjustments for sixth order mesh
        if not int(meshcode[8]) in [1, 2, 3, 4]:
            raise ValueError(f"meshcode number errorh last number:The range of numbers in last number of forth meshcode must be from 1 to 4")
       
        delta_latitude = 3.75/3600  # 3.75 seconds in degrees
        delta_longitude = 5.625/3600  # 5.625 seconds in degrees
        south_latitude += [None, 0, 0, delta_latitude, delta_latitude][int(meshcode[10])]
        west_longitude += [None, 0, delta_longitude, 0, delta_longitude][int(meshcode[10])]
        
    # Calculate the coordinates for the bounding box of the mesh
    coordinates = [
        [
            [west_longitude, south_latitude],  # Bottom left
            [west_longitude + delta_longitude, south_latitude],  # Bottom right
            [west_longitude + delta_longitude, south_latitude + delta_latitude],  # Top right
            [west_longitude, south_latitude + delta_latitude],  # Top left
            [west_longitude, south_latitude]  # Close the loop
        ]
    ]
    
    # Construct the GeoJSON
    geojson = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": coordinates
        },
        "properties": {
            "meshcode": meshcode
        }
    }
    
    return json.dumps(geojson)