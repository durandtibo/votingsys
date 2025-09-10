r"""Contain the implementation of the ranked vote."""

from __future__ import annotations

__all__ = ["RankedVote"]

from typing import TYPE_CHECKING, Any

from coola import objects_are_equal

from votingsys.utils.dataframe import check_column_exist
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
            column represents a candidate, and each row is a voter
            ranking. The ranking goes from ``0`` to ``n-1``, where
            ``n`` is the number of candidates. One column contains
            the number of voters for this ranking.
        count_col: The column with the count data for each ranking.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from votingsys.vote import RankedVote
    >>> vote = RankedVote(
    ...     pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 5, 2]}),
    ...     count_col="count",
    ... )
    >>> vote
    RankedVote(num_candidates=3, num_voters=10, count_col='count')

    ```
    """

    def __init__(self, ranking: pl.DataFrame, count_col: str = "count") -> None:
        check_column_exist(ranking, count_col)
        self._ranking = ranking
        self._count_col = count_col

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(num_candidates={self.get_num_candidates():,}, "
            f"num_voters={self.get_num_voters():,}, count_col={self._count_col!r})"
        )

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return objects_are_equal(self._ranking, other._ranking, equal_nan=equal_nan)

    def get_num_candidates(self) -> int:
        return self._ranking.shape[1] - 1

    def get_num_voters(self) -> int:
        return self._ranking[self._count_col].sum()

    def absolute_majority_winner(self) -> str:
        r"""Compute the winner based on the absolute majority rule.

        The candidate receiving more than 50% of the vote is the winner.

        Returns:
            The winner based on the absolute majority rule.

        Raises:
            WinnerNotFoundError: if no candidate has the majority of votes.

        Example usage:

        ```pycon

        >>> import polars as pl
        >>> from votingsys.vote import RankedVote
        >>> vote = RankedVote(
        ...     pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 5, 2]}),
        ...     count_col="count",
        ... )
        >>> vote.absolute_majority_winner()
        'b'

        ```
        """
