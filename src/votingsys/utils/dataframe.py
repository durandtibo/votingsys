r"""Contain DataFrame utility functions."""

from __future__ import annotations

__all__ = ["check_column_missing"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import polars as pl


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
