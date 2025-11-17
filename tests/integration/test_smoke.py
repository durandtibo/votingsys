from __future__ import annotations

import polars as pl

from votingsys.utils.dataframe import (
    check_column_exist,
)


def test_smoke() -> None:
    check_column_exist(
        pl.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"], "c": [1.1, 2.2, 3.3]}), col="a"
    )
