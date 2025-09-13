r"""Contain the implementation of the ranked vote."""

from __future__ import annotations

__all__ = ["RankedVote"]

from typing import TYPE_CHECKING, Any

from coola import objects_are_equal

from votingsys.data.aggregation import compute_count_aggregated_dataframe
from votingsys.utils.dataframe import (
    check_column_exist,
    remove_zero_weight_rows,
    sum_weights_by_group,
    weighted_value_count,
)
from votingsys.utils.mapping import find_max_in_mapping
from votingsys.vote.base import (
    BaseVote,
    MultipleWinnersFoundError,
    WinnerNotFoundError,
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
    ...     pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 5, 2]})
    ... )
    >>> vote
    RankedVote(num_candidates=3, num_voters=10, count_col='count')
    >>> vote.ranking
    shape: (3, 4)
    ┌─────┬─────┬─────┬───────┐
    │ a   ┆ b   ┆ c   ┆ count │
    │ --- ┆ --- ┆ --- ┆ ---   │
    │ i64 ┆ i64 ┆ i64 ┆ i64   │
    ╞═════╪═════╪═════╪═══════╡
    │ 0   ┆ 1   ┆ 2   ┆ 3     │
    │ 1   ┆ 2   ┆ 0   ┆ 5     │
    │ 2   ┆ 0   ┆ 1   ┆ 2     │
    └─────┴─────┴─────┴───────┘

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

    @property
    def ranking(self) -> pl.DataFrame:
        r"""Return the DataFrame containing the rankings."""
        return self._ranking

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
        >>> vote = RankedVote.from_dataframe_with_count(
        ...     pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 6, 2]}),
        ... )
        >>> vote.absolute_majority_winner()
        'c'

        ```
        """
        counts = weighted_value_count(self._ranking, value=0, weight_col=self._count_col)
        candidates, max_votes = find_max_in_mapping(counts)
        total_votes = self.get_num_voters()
        if max_votes / total_votes > 0.5:
            return candidates[0]
        msg = "No winner found using absolute majority rule"
        raise WinnerNotFoundError(msg)

    def plurality_winner(self) -> str:
        r"""Compute the winner based on the plurality rule.

        This rule is also named First-Past-The-Post (FPTP).
        The leading candidate, whether or not they have a majority of votes, is the winner.

        Returns:
            The winner based on the plurality rule.

        Raises:
            MultipleWinnersFoundError: if the leading candidates are tied.

        Example usage:

        ```pycon

        >>> import polars as pl
        >>> from votingsys.vote import RankedVote
        >>> vote = RankedVote.from_dataframe_with_count(
        ...     pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 6, 2]}),
        ... )
        >>> vote.plurality_winner()
        'c'

        ```
        """
        winners = self.plurality_winners()
        if len(winners) > 1:
            msg = f"Multiple winners found using plurality rule: {winners}"
            raise MultipleWinnersFoundError(msg)
        return winners[0]

    def plurality_winners(self) -> tuple[str, ...]:
        r"""Compute the winner(s) based on the plurality rule.

        This rule is also named First-Past-The-Post (FPTP).
        The leading candidate, whether or not they have a majority of votes, is the winner.

        Returns:
            The winners based on the plurality rule. Multiple winners
                can be returned if the leading candidates are tied.
                The candiates are sorted by alphabetical order.

        Example usage:

        ```pycon

        >>> import polars as pl
        >>> from votingsys.vote import RankedVote
        >>> vote = RankedVote.from_dataframe_with_count(
        ...     pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 6, 2]}),
        ... )
        >>> vote.plurality_winners()
        ('c',)
        >>> vote = RankedVote.from_dataframe_with_count(
        ...     pl.DataFrame(
        ...         {"a": [0, 1, 2, 1], "b": [1, 2, 0, 0], "c": [2, 0, 1, 2], "count": [3, 6, 2, 4]}
        ...     ),
        ... )
        >>> vote.plurality_winners()
        ('b', 'c')

        ```
        """
        counts = weighted_value_count(self._ranking, value=0, weight_col=self._count_col)
        candidates, _ = find_max_in_mapping(counts)
        return tuple(sorted(candidates))

    @classmethod
    def from_dataframe(cls, ranking: pl.DataFrame, count_col: str = "count") -> RankedVote:
        r"""Instantiate a ``RankedVote`` object from a
        ``polars.DataFrame`` containing the ranking.

        Internally, ``RankedVote`` uses a compressed DataFrame with
        the number of occurrences for each ranking. For example if the
        same ranking is ``N`` times in the DataFrame, it will be
        re-encoded as a single row with a count of ``N``.
        The "compressed" representation is more efficient because the
        new DataFrame can be much smaller.

        Args:
            ranking: The DataFrame with the ranking for each voter.
            count_col: The column that will contain the count values
                for each ranking.

        Example usage:

        ```pycon

        >>> import polars as pl
        >>> from votingsys.vote import RankedVote
        >>> vote = RankedVote.from_dataframe(
        ...     pl.DataFrame(
        ...         {"a": [0, 1, 2, 1, 0, 0], "b": [1, 2, 0, 2, 1, 1], "c": [2, 0, 1, 0, 2, 2]}
        ...     )
        ... )
        >>> vote
        RankedVote(num_candidates=3, num_voters=6, count_col='count')
        >>> vote.ranking
        shape: (3, 4)
        ┌─────┬─────┬─────┬───────┐
        │ a   ┆ b   ┆ c   ┆ count │
        │ --- ┆ --- ┆ --- ┆ ---   │
        │ i64 ┆ i64 ┆ i64 ┆ i64   │
        ╞═════╪═════╪═════╪═══════╡
        │ 0   ┆ 1   ┆ 2   ┆ 3     │
        │ 1   ┆ 2   ┆ 0   ┆ 2     │
        │ 2   ┆ 0   ┆ 1   ┆ 1     │
        └─────┴─────┴─────┴───────┘

        ```
        """
        return cls.from_dataframe_with_count(
            ranking=compute_count_aggregated_dataframe(ranking, count_col=count_col),
            count_col=count_col,
        )

    @classmethod
    def from_dataframe_with_count(
        cls, ranking: pl.DataFrame, count_col: str = "count"
    ) -> RankedVote:
        r"""Instantiate a ``RankedVote`` object from a
        ``polars.DataFrame`` containing the rankings and their
        associated counts.

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
        >>> vote = RankedVote.from_dataframe_with_count(
        ...     pl.DataFrame(
        ...         {
        ...             "a": [0, 1, 2, 0, 2],
        ...             "b": [1, 2, 0, 1, 1],
        ...             "c": [2, 0, 1, 2, 0],
        ...             "count": [3, 5, 2, 1, 0],
        ...         }
        ...     ),
        ... )
        >>> vote
        RankedVote(num_candidates=3, num_voters=11, count_col='count')
        >>> vote.ranking
        shape: (3, 4)
        ┌─────┬─────┬─────┬───────┐
        │ a   ┆ b   ┆ c   ┆ count │
        │ --- ┆ --- ┆ --- ┆ ---   │
        │ i64 ┆ i64 ┆ i64 ┆ i64   │
        ╞═════╪═════╪═════╪═══════╡
        │ 1   ┆ 2   ┆ 0   ┆ 5     │
        │ 0   ┆ 1   ┆ 2   ┆ 4     │
        │ 2   ┆ 0   ┆ 1   ┆ 2     │
        └─────┴─────┴─────┴───────┘

        ```
        """
        cols = [count_col, *sorted([col for col in ranking.columns if col != count_col])]
        return cls(
            ranking=remove_zero_weight_rows(
                sum_weights_by_group(ranking, weight_col=count_col), weight_col=count_col
            ).sort(by=cols, descending=True),
            count_col=count_col,
        )
