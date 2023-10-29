import pytest

from jismeshcode.jismeshcode import normalize_meshcode


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        ["5439", "5439"],  # 半角数字
        ["５４３９", "5439"],  # 全角数字
        ["6441-42-77", "64414277"],  # ハイフン
        ["6441 42 77", "64414277"],  # スペース
    ]
)
def test_normalize_meshcode(value, expected):
    normalize_meshcode(value) == expected
