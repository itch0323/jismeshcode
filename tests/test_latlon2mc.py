import pytest

from jismeshcode.jismeshcode import latlon2mc

@pytest.mark.parametrize(
    "latlon",
    [
        # 4
        {'lat': 36.2010417, 'lon': 138.415625, 'mesh_level':  4, 'meshcode': '5438'},
        # 6
        {'lat': 36.2010417, 'lon': 138.415625, 'mesh_level':  6, 'meshcode': '543823'},
        # 8
        {'lat': 36.2010417, 'lon': 138.415625, 'mesh_level':  8, 'meshcode': '54382343'},
        # 9
        {'lat': 36.2010417, 'lon': 138.415625, 'mesh_level':  9, 'meshcode': '543823431'},
        # 10
        {'lat': 36.2010417, 'lon': 138.415625, 'mesh_level': 10, 'meshcode': '5438234312'},
        # 11
        {'lat': 36.2010417, 'lon': 138.415625, 'mesh_level': 11, 'meshcode': '54382343123'},
    ]
)

def test_latlon2mc(latlon):
    lat = latlon['lat']
    lon = latlon['lon']
    mlv = latlon['mesh_level']
    result = latlon2mc(lat, lon, mlv)
    assert result == latlon['meshcode']

def test_invalid_input():
    with pytest.raises(ValueError):
        latlon2mc(35, 135, 1)
    with pytest.raises(ValueError):
        latlon2mc(35, 135, 12)
    with pytest.raises(TypeError):
        latlon2mc(None)
