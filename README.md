# jismeshcode

## このライブラリは
- 地域メッシュコードを操作するライブラリです
- 現在はメッシュコードに対応する矩形をジオデータ(GeoJSON)に変換する関数が提供されています

## インストール方法
```shell
pip install jismeshcode
```

## 使い方
### mc2geojson
- 入力
    - メッシュコード(4桁〜11桁)
- 出力
    - メッシュコードで表されるエリアを囲うポリゴンを表すGeoJSONを返す

```Python
>>> from jismeshcode.jismeshcode import mc2geojson
>>> mc2geojson(5438)
{'type': 'Feature', 'geometry': {'type': 'Polygon', 'coordinates': [[[138, 36.0], [139, 36.0], [139, 36.666666666666664], [138, 36.666666666666664], [138, 36.0]]]}, 'properties': {'meshcode': '5438'}}
```
