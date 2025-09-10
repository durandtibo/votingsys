r"""Contain the implementation of the ranked vote."""

from __future__ import annotations

__all__ = ["RankedVote"]

from typing import TYPE_CHECKING, Any

from coola import objects_are_equal

from votingsys.vote.base import (
    BaseVote,
)

if TYPE_CHECKING:
    import polars as pl


class RankedVote(BaseVote):
    r"""Define the ranked vote.

    A ranked vote, also known as a preferential vote, is a voting
    system in which voters rank candidates or options in order of
    preference, rather than choosing just one.

    Args:
        ranking: A DataFrame with the ranking for each voters. Each
            column represents a candidate, and each row is a voter.
            The ranking goes from ``0`` to ``n-1``, where ``n`` is
            the number of candidates.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from votingsys.vote import RankedVote
    >>> vote = RankedVote(
    ...     pl.DataFrame({"a": [0, 1, 2, 1, 0], "b": [1, 2, 0, 2, 1], "c": [2, 0, 1, 0, 2]})
    ... )
    >>> vote
    RankedVote(num_candidates=3, num_voters=5)

    ```
    """

    def __init__(self, ranking: pl.DataFrame) -> None:
        self._ranking = ranking

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(num_candidates={self.get_num_candidates():,}, "
            f"num_voters={self.get_num_voters():,})"
        )

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return objects_are_equal(self._ranking, other._ranking, equal_nan=equal_nan)

    def get_num_candidates(self) -> int:
        return self._ranking.shape[1]

    def get_num_voters(self) -> int:
        return self._ranking.shape[0]
