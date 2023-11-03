import json
import math
from typing import Union, Optional

VALID_MESH_CODE_LENGTH = (4, 6, 7, 8, 9, 10, 11)


def normalize_meshcode(meshcode):
    return ''.join(filter(lambda x: x.isdigit(), meshcode))

def mc2coordinates(meshcode: Union[str, int]) -> str:
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
        if not (0 <= int(meshcode[4]) <= 7) or not (0 <= int(meshcode[5]) <= 7):
            raise ValueError(f"meshcode number error number:Fourth and fifth number of meshcode must be from 0 to 7")
    
        delta_latitude = 1/12 # 5 minutes in degrees
        delta_longitude = 1/8 # 7.5 minutes in degrees
        south_latitude += int(meshcode[4]) * delta_latitude
        west_longitude += int(meshcode[5]) * delta_longitude

    if mesh_level == 7:  # Apply adjustments for five times regional mesh
        if not 1 <= int(meshcode[6]) <= 4:
            raise ValueError(f"meshcode number error number:The range of number in last number of forth meshcode must be from 1 to 4")
        
        delta_latitude = 1/24 # 2.5 minutes in degrees
        delta_longitude = 1/16 # 3.75 minutes in degrees
        south_latitude += [None, 0, 0, delta_latitude, delta_latitude][int(meshcode[6])]
        west_longitude += [None, 0, delta_longitude, 0, delta_longitude][int(meshcode[6])]

    if mesh_level >= 8:  # Apply adjustments for third order mesh
        delta_latitude = 1/120 # 30 seconds in degrees
        delta_longitude = 3/240 # 45 seconds in degrees
        south_latitude += int(meshcode[6]) * delta_latitude
        west_longitude += int(meshcode[7]) * delta_longitude
        
    if mesh_level == 9:  # Apply adjustments for fourth order or two times mesh
        if not 1 <= int(meshcode[8]) <= 5:
            raise ValueError(f"meshcode number error last number:The range of number in last number of forth meshcode must be from 1 to 5")
        
        if not int(meshcode[8]) == 5: # Apply adjustments for fourth order mesh
            delta_latitude = 15/3600 # 15 seconds in degrees
            delta_longitude = 22.5/3600 # 22.5 seconds in degrees
            south_latitude += [None, 0, 0, delta_latitude, delta_latitude][int(meshcode[8])]
            west_longitude += [None, 0, delta_longitude, 0, delta_longitude][int(meshcode[8])]
        elif int(meshcode[6])%2 == 1 or int(meshcode[7])%2 == 1:
            raise ValueError(f"meshcode number error number:Sevens and eighth number of meshcode must be even")
        elif len(meshcode) == 9: # Apply adjustments for two times mesh
            delta_latitude = 1/60 # 1 minutes in degrees
            delta_longitude = 1/40 # 1.41 minutes in degrees
            south_latitude += int(meshcode[6]) * delta_latitude
            west_longitude += int(meshcode[7]) * delta_longitude

    if mesh_level >= 10:  # Apply adjustments for fifth order mesh
        if not int(meshcode[9]) in [1, 2, 3, 4]:
            raise ValueError(f"meshcode number error last number:The range of number in last number of forth meshcode must be from 1 to 4")
       
        delta_latitude = 7.5/3600  # 7.5 seconds in degrees
        delta_longitude = 11.25/3600  # 11.25 seconds in degrees
        south_latitude += [None, 0, 0, delta_latitude, delta_latitude][int(meshcode[9])]
        west_longitude += [None, 0, delta_longitude, 0, delta_longitude][int(meshcode[9])]
        
    if mesh_level == 11:  # Apply adjustments for sixth order mesh
        if not int(meshcode[10]) in [1, 2, 3, 4]:
            raise ValueError(f"meshcode number errorh last number:The range of number in last number of forth meshcode must be from 1 to 4")
       
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
    return coordinates

def mc2geojson(meshcode: Union[str, int], properties: Optional[dict] = None) -> str:
    # Construct the properties dictionary
    properties_data = {"meshcode": meshcode}
    if properties:
        properties_data.update(properties)

    # Construct the GeoJSON
    geojson = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": mc2coordinates(meshcode)
        },
        "properties": properties_data
    }
    
    return json.dumps(geojson)

def latlon2mc(lat: float, lon: float, mesh_level: int = 8):
    if(not(mesh_level in VALID_MESH_CODE_LENGTH)):
        raise ValueError(f"meshcode type error:{mesh_level} meshcode type must be within {VALID_MESH_CODE_LENGTH}")

    remain_lat = lat * 3 / 2
    remain_lon = lon - 100
    flat = math.floor(remain_lat)
    flon = math.floor(remain_lon)
    mc = str(flat)[0:2] + str(flon)[0:2]

    if mesh_level >= 6:
        remain_lat = 8*(remain_lat - flat)
        remain_lon = 8*(remain_lon - flon)
        flat = math.floor(remain_lat)
        flon = math.floor(remain_lon)
        mc = mc[0:4] + str(flat)[-1] + str(flon)[-1]

    if mesh_level >= 8:
        remain_lat = 10*(remain_lat - flat)
        remain_lon = 10*(remain_lon - flon)
        flat = math.floor(remain_lat)
        flon = math.floor(remain_lon)
        mc = mc[0:6] + str(flat)[-1] + str(flon)[-1]
 
    if mesh_level >= 9:
        remain_lat = 2*(remain_lat - flat)
        remain_lon = 2*(remain_lon - flon)
        flat = math.floor(remain_lat)
        flon = math.floor(remain_lon)
        mc = mc[0:8] + str(flat*2 + 1 + flon)
 
    if mesh_level >= 10:
        remain_lat = 2*(remain_lat - flat)
        remain_lon = 2*(remain_lon - flon)
        flat = math.floor(remain_lat)
        flon = math.floor(remain_lon)
        mc = mc[0:9] + str(flat*2 + 1 + flon)
 
    if mesh_level >= 11:
        remain_lat = 2*(remain_lat - flat)
        remain_lon = 2*(remain_lon - flon)
        flat = math.floor(remain_lat)
        flon = math.floor(remain_lon)
        mc = mc[0:10] + str(flat*2 + 1 + flon)
 
    return mc