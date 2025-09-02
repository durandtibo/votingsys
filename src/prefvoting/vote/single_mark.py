r"""Contain the implementation of the single-mark vote."""

from __future__ import annotations

__all__ = ["SingleMarkVote"]

from collections import Counter
from typing import TYPE_CHECKING, Any

from coola import objects_are_equal
from coola.utils.format import repr_indent, repr_mapping

from prefvoting.utils.counter import check_non_negative_count
from prefvoting.vote.base import (
    BaseVote,
    MultipleWinnersFoundError,
    WinnerNotFoundError,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    import polars as pl


class SingleMarkVote(BaseVote):
    r"""Define a single-mark vote.

    This vote assumes that the voter must mark one and only one candidate.

    Args:
        counter: The counter with the number of votes for each candidate.

    Example usage:

    ```pycon

    >>> from collections import Counter
    >>> from prefvoting.vote import SingleMarkVote
    >>> vote = SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3}))
    >>> vote
    SingleMarkVote(
      (counter): Counter({'a': 10, 'c': 5, 'd': 3, 'b': 2})
    )

    ```
    """

    def __init__(self, counter: Counter) -> None:
        check_non_negative_count(counter)
        self._counter = counter

    def __repr__(self) -> str:
        args = repr_indent(repr_mapping({"counter": self._counter}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return objects_are_equal(self._counter, other._counter, equal_nan=equal_nan)

    def get_num_candidates(self) -> int:
        return len(self._counter)

    def get_num_voters(self) -> int:
        return self._counter.total()

    def absolute_majority_winner(self) -> str:
        r"""Compute the winner based on the absolute majority rule.

        The candidate receiving more than 50% of the vote is the winner.

        Returns:
            The winner based on the absolute majority rule.

        Raises:
            WinnerNotFoundError: if no candidate has the majority of votes.

        Example usage:

        ```pycon

        >>> from collections import Counter
        >>> from prefvoting.vote import SingleMarkVote
        >>> vote = SingleMarkVote(Counter({"a": 10, "b": 20, "c": 5, "d": 3}))
        >>> vote.absolute_majority_winner()
        'b'

        ```
        """
        total_votes = self.get_num_voters()
        candidate, num_votes = self._counter.most_common(1)[0]
        if num_votes / total_votes > 0.5:
            return candidate
        msg = "No winner found using absolute majority rule"
        raise WinnerNotFoundError(msg)

    def plurality_winner(self) -> str:
        r"""Compute the winner based on the plurality rule.

        This rule is also named First-Past-The-Post (FPTP).
        The leading candidate, whether or not they have a majority of votes, is the winner.

        Returns:
            The winner based on the plurality rule.

        Raises:
            WinnerNotFoundError: if there is no voters.
            MultipleWinnersFoundError: if the leading candidates are tied.

        Example usage:

        ```pycon

        >>> from collections import Counter
        >>> from prefvoting.vote import SingleMarkVote
        >>> vote = SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3}))
        >>> vote.plurality_winner()
        'a'

        ```
        """
        winners = self.plurality_winners()
        if len(winners) > 1:
            msg = f"Multiple winners found: {winners}"
            raise MultipleWinnersFoundError(msg)
        return winners[0]

    def plurality_winners(self) -> tuple[str, ...]:
        r"""Compute the winner based on the plurality rule.

        This rule is also named First-Past-The-Post (FPTP).
        The leading candidate, whether or not they have a majority of votes, is the winner.

        Returns:
            The winners based on the plurality rule. Multiple winners
                can be returned if the leading candidates are tied.

        Example usage:

        ```pycon

        >>> from collections import Counter
        >>> from prefvoting.vote import SingleMarkVote
        >>> vote = SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3}))
        >>> vote.plurality_winners()
        ('a',)

        ```
        """
        if not self.get_num_voters():
            msg = "No winner found because there is no voters"
            raise WinnerNotFoundError(msg)
        max_count = max(self._counter.values())
        max_candidates = [cand for cand, count in self._counter.items() if count == max_count]
        return tuple(sorted(max_candidates))

    @classmethod
    def from_sequence(cls, votes: Sequence[str]) -> SingleMarkVote:
        r"""Instantiate a ``SingleMarkVote`` object from the sequence of
        votes.

        Args:
            votes: The sequence of votes.

        Returns:
            The instantiated ``SingleMarkVote``.

        Example usage:

        ```pycon

        >>> from prefvoting.vote import SingleMarkVote
        >>> vote = SingleMarkVote.from_sequence(["a", "b", "a", "c", "a", "a", "b"])
        >>> vote
        SingleMarkVote(
          (counter): Counter({'a': 4, 'b': 2, 'c': 1})
        )

        ```
        """
        return cls(Counter(votes))

    @classmethod
    def from_series(cls, votes: pl.Series) -> SingleMarkVote:
        r"""Instantiate a ``SingleMarkVote`` object from a
        ``polars.Series`` containing the votes.

        Args:
            votes: The ``polars.Series`` containing the votes.

        Returns:
            The instantiated ``SingleMarkVote``.

        Example usage:

        ```pycon

        >>> import polars as pl
        >>> from prefvoting.vote import SingleMarkVote
        >>> vote = SingleMarkVote.from_sequence(pl.Series(["a", "b", "a", "c", "a", "a", "b"]))
        >>> vote
        SingleMarkVote(
          (counter): Counter({'a': 4, 'b': 2, 'c': 1})
        )

        ```
        """
        return cls.from_sequence(votes.to_list())
