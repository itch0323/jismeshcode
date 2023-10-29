import pytest

from jismeshcode.jismeshcode import mc2geojson


@pytest.mark.parametrize(
    "geojson",
    [
        # 4
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[139, 36.0], [140, 36.0], [
            140, 36.666666666666664], [139, 36.666666666666664], [139, 36.0]]]}, 'properties': {'meshcode': '5439'}},
        # 6
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[139.625, 36.333333333333336], [139.75, 36.333333333333336], [
            139.75, 36.41666666666667], [139.625, 36.41666666666667], [139.625, 36.333333333333336]]]}, 'properties': {'meshcode': '543945'}},
        # 8
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[139.7375, 36.333333333333336], [139.75, 36.333333333333336], [
            139.75, 36.34166666666667], [139.7375, 36.34166666666667], [139.7375, 36.333333333333336]]]}, 'properties': {'meshcode': '54394509'}},
        # 9
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[139.74062500000002, 35.66875], [139.74687500000002, 35.66875], [
            139.74687500000002, 35.67291666666667], [139.74062500000002, 35.67291666666667], [139.74062500000002, 35.66875]]]}, 'properties': {'meshcode': '533945092'}},
        # 10
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[139.74062500000002, 35.66875], [139.74375000000003, 35.66875], [
            139.74375000000003, 35.670833333333334], [139.74062500000002, 35.670833333333334], [139.74062500000002, 35.66875]]]}, 'properties': {'meshcode': '5339450921'}},
        # 11
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[139.74062500000002, 35.66875], [139.74218750000003, 35.66875], [
            139.74218750000003, 35.66979166666667], [139.74062500000002, 35.66979166666667], [139.74062500000002, 35.66875]]]}, 'properties': {'meshcode': '53394509211'}}
    ]
)
def test_mc2geojson(geojson):
    meshcode = geojson['properties']['meshcode']
    result = mc2geojson(meshcode)
    assert result == geojson


def test_invalid_input():
    with pytest.raises(ValueError):
        mc2geojson('invalid_meshcode')
    with pytest.raises(ValueError):
        mc2geojson('')
    with pytest.raises(TypeError):
        mc2geojson(None)
