# jismeshcode

[English version](README_en.md)

## このライブラリは

- 地域メッシュコードを操作するライブラリです
- 現在はメッシュコードに対応する矩形をジオデータ(GeoJSON)に変換する関数が提供されています

## インストール

- 環境
  - Python 3.8 以上

```shell
pip install jismeshcode
```

## 使い方

### mc2geojson

- 入力
  - メッシュコード(4, 6, 8, 9, 10, 11 桁)
- 出力
  - メッシュコードで表されるエリアを囲うポリゴンを表す GeoJSON を返す

```Python
>>> from jismeshcode.jismeshcode import mc2geojson
>>> mc2geojson(5439)
'{"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[139, 36.0], [140, 36.0], [140, 36.666666666666664], [139, 36.666666666666664], [139, 36.0]]]}, "properties": {"meshcode": "5439"}}'
```
