r"""Contain DataFrame utility functions."""

from __future__ import annotations

__all__ = ["check_colum_missing"]

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import polars as pl


def check_colum_missing(frame: pl.DataFrame, col: str) -> None:
    r"""Check if a column is missing in a DataFrame.

    Args:
        frame: The DataFrame to check.
        col: The column that should be missing in the DataFrame.

    Raises:
        ValueError: if the column exists in the DataFrame.
    """
    if col in frame:
        msg = f"column '{col}' exists in the DataFrame: {sorted(frame.columns)}"
        raise ValueError(msg)
