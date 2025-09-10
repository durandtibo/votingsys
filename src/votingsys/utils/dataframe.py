r"""Contain DataFrame utility functions."""

from __future__ import annotations

__all__ = ["check_column_exist", "check_column_missing", "count_value_per_column"]

from typing import TYPE_CHECKING, Any

import polars as pl

if TYPE_CHECKING:
    import numpy as np


def check_column_exist(frame: pl.DataFrame, col: str) -> None:
    r"""Check if a column exists in a DataFrame.

    Args:
        frame: The DataFrame to check.
        col: The column that should exist in the DataFrame.

    Raises:
        ValueError: if the column is missing in the DataFrame.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from votingsys.utils.dataframe import check_column_exist
    >>> check_column_exist(
    ...     pl.DataFrame({"a": [0, 1, 2, 1, 0], "b": [1, 2, 0, 2, 1], "c": [2, 0, 1, 0, 2]}),
    ...     col="a",
    ... )

    ```
    """
    if col not in frame:
        msg = f"column '{col}' is missing in the DataFrame: {sorted(frame.columns)}"
        raise ValueError(msg)


def check_column_missing(frame: pl.DataFrame, col: str) -> None:
    r"""Check if a column is missing in a DataFrame.

    Args:
        frame: The DataFrame to check.
        col: The column that should be missing in the DataFrame.

    Raises:
        ValueError: if the column exists in the DataFrame.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from votingsys.utils.dataframe import check_column_missing
    >>> check_column_missing(
    ...     pl.DataFrame({"a": [0, 1, 2, 1, 0], "b": [1, 2, 0, 2, 1], "c": [2, 0, 1, 0, 2]}),
    ...     col="col",
    ... )

    ```
    """
    if col in frame:
        msg = f"column '{col}' exists in the DataFrame: {sorted(frame.columns)}"
        raise ValueError(msg)


def count_value_per_column(frame: pl.DataFrame, value: Any) -> np.ndarray:
    r"""Count the number of value occurrences per column.

    Args:
        frame: The DataFrame containg the data.
        value: The target value used to find the number of occurences.

    Returns:
        A dictionary with the count per column.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from votingsys.utils.dataframe import count_value_per_column
    >>> counts = count_value_per_column(
    ...     pl.DataFrame({"a": [0, 1, 2, 1, 0], "b": [1, 2, 0, 2, 1], "c": [2, 0, 1, 0, 2]}),
    ...     value=1,
    ... )
    >>> counts
    {'a': 2, 'b': 2, 'c': 1}

    ```
    """
    if value is None:
        msg = "value cannot be None"
        raise ValueError(msg)
    counts = frame.select(
        [
            ((pl.col(col) == value) & pl.col(col).is_not_null()).sum().alias(col)
            for col in frame.columns
        ]
    ).to_dict(as_series=False)
    return {key: value[0] for key, value in counts.items()}
