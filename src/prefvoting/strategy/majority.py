from __future__ import annotations

__all__ = ["majority_voting"]

import polars as pl


def majority_voting(frame_rank: pl.DataFrame) -> dict:
    # Count the number of rank 0 in each column
    zero_counts = frame_rank.select(
        [(pl.col(col) == 0).sum().alias(col) for col in frame_rank.columns]
    )
    count_max = max(zero_counts.row(0))
    max_columns = [col for col in zero_counts.columns if zero_counts[0, col] == count_max]
    return {"winner": max_columns, "count": zero_counts.to_dict(as_series=False)}
