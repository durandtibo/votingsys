from __future__ import annotations

import polars as pl
import pytest

from votingsys.utils.dataframe import check_colum_missing

#########################################
#     Tests for check_colum_missing     #
#########################################


def test_check_colum_missing() -> None:
    check_colum_missing(
        pl.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"], "c": [1.1, 2.2, 3.3]}), col="col"
    )


def test_check_colum_missing_empty() -> None:
    check_colum_missing(pl.DataFrame({}), col="col")


def test_check_colum_missing_exist() -> None:
    with pytest.raises(ValueError, match="column 'a' exists in the DataFrame:"):
        check_colum_missing(
            pl.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"], "c": [1.1, 2.2, 3.3]}), col="a"
        )
