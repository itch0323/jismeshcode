import json
import pytest

from jismeshcode.jismeshcode import mc2geojson


@pytest.mark.parametrize(
    "geojson",
    [
        # 4 1次メッシュコード
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[138, 36.0], [139, 36.0], [
            139, 36.666666666666664], [138, 36.666666666666664], [138, 36.0]]]}, 'properties': {'meshcode': '5438'}},
        # 6 2次メッシュコード
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[138.375, 36.166666666666664], [
            138.5, 36.166666666666664], [138.5, 36.25], [138.375, 36.25], [138.375, 36.166666666666664]]]}, 'properties': {'meshcode': '543823'}},
        # 7 5倍地域メッシュコード
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[138.4375, 36.20833333333333], [
            138.5, 36.20833333333333], [138.5, 36.24999999999999], [138.4375, 36.24999999999999], [138.4375, 36.20833333333333]]]}, 'properties': {'meshcode': '5438234'}},
        # 8 3次メッシュコード
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[138.4125, 36.199999999999996], [
            138.42499999999998, 36.199999999999996], [138.42499999999998, 36.20833333333333], [138.4125, 36.20833333333333], [138.4125, 36.199999999999996]]]}, 'properties': {'meshcode': '54382343'}},
        # 9 4次メッシュコード
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[138.4125, 36.199999999999996], [
            138.41875, 36.199999999999996], [138.41875, 36.204166666666666], [138.4125, 36.204166666666666], [138.4125, 36.199999999999996]]]}, 'properties': {'meshcode': '543823431'}},
        # 9 2倍地域メッシュコード
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[138.6, 36.266666666666666], [
            138.625, 36.266666666666666], [138.625, 36.28333333333333], [138.6, 36.28333333333333], [138.6, 36.266666666666666]]]}, 'properties': {'meshcode': '543823465'}},
        # 10 5次メッシュコード
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[138.415625, 36.199999999999996], [
            138.41875000000002, 36.199999999999996], [138.41875000000002, 36.20208333333333], [138.415625, 36.20208333333333], [138.415625, 36.199999999999996]]]}, 'properties': {'meshcode': '5438234312'}},
        # 11 6次メッシュコード
        {'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[138.415625, 36.20104166666666], [
            138.4171875, 36.20104166666666], [138.4171875, 36.20208333333333], [138.415625, 36.20208333333333], [138.415625, 36.20104166666666]]]}, 'properties': {'meshcode': '54382343123'}}
    ]
)
def test_mc2geojson(geojson):
    meshcode = geojson['properties']['meshcode']
    result = mc2geojson(meshcode)
    assert result == json.dumps(geojson)


def test_invalid_input():
    with pytest.raises(ValueError):
        mc2geojson('invalid_meshcode')
    with pytest.raises(ValueError):
        mc2geojson('')
    with pytest.raises(TypeError):
        mc2geojson(None)


def test_invalid_meshcode():
    with pytest.raises(ValueError):
        mc2geojson('1')  # メッシュコードは4桁以上
    with pytest.raises(ValueError):
        mc2geojson('12')  # メッシュコードは4桁以上
    with pytest.raises(ValueError):
        mc2geojson('123')  # メッシュコードは4桁以上
    with pytest.raises(ValueError):
        mc2geojson('543829')  # 2次メッシュコードの末尾が取りうる値は1から8
    with pytest.raises(ValueError):
        mc2geojson('543823435')  # 2倍地域メッシュコードの7, 8番目の要素が取りうる値は偶数
    with pytest.raises(ValueError):
        mc2geojson('543823436')  # 4次メッシュコードの末尾が取りうる値は1から4
    with pytest.raises(ValueError):
        mc2geojson('5438234355')  # 5次メッシュコードの末尾が取りうる値は1から4
    with pytest.raises(ValueError):
        mc2geojson('54382343555')  # 6次メッシュコードの末尾が取りうる値は1から4
