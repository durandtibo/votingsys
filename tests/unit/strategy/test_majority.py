from __future__ import annotations

import polars as pl
from coola import objects_are_equal

from prefvoting.strategy.majority import majority_voting


def test_majority_voting_1_row() -> None:
    assert objects_are_equal(
        majority_voting(pl.DataFrame({"a": [0], "b": [1], "c": [2]})),
        {"winner": ["a"], "count": {"a": 1, "b": 0, "c": 0}},
    )
