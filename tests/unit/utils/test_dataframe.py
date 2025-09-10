from __future__ import annotations

import polars as pl
import pytest

from votingsys.utils.dataframe import check_column_exist, check_column_missing

########################################
#     Tests for check_column_exist     #
########################################


def test_check_column_exist() -> None:
    check_column_exist(
        pl.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"], "c": [1.1, 2.2, 3.3]}), col="a"
    )


def test_check_column_exist_missing() -> None:
    with pytest.raises(ValueError, match=r"column 'd' is missing in the DataFrame:"):
        check_column_exist(
            pl.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"], "c": [1.1, 2.2, 3.3]}), col="d"
        )


##########################################
#     Tests for check_column_missing     #
##########################################


def test_check_column_missing() -> None:
    check_column_missing(
        pl.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"], "c": [1.1, 2.2, 3.3]}), col="col"
    )


def test_check_column_missing_empty() -> None:
    check_column_missing(pl.DataFrame({}), col="col")


def test_check_column_missing_exist() -> None:
    with pytest.raises(ValueError, match=r"column 'a' exists in the DataFrame:"):
        check_column_missing(
            pl.DataFrame({"a": [1, 2, 3], "b": ["a", "b", "c"], "c": [1.1, 2.2, 3.3]}), col="a"
        )
