r"""Contain the implementation of the single-mark vote."""

from __future__ import annotations

__all__ = ["SingleMarkVote"]


from typing import TYPE_CHECKING, Any

from coola import objects_are_equal
from coola.utils.format import repr_indent, repr_mapping

from prefvoting.utils.counter import check_non_negative_count
from prefvoting.vote.base import BaseVote

if TYPE_CHECKING:
    from collections import Counter


class SingleMarkVote(BaseVote):
    r"""Define a single-mark vote.

    Args:
        counter: The counter with the number of votes for each candidate.

    Example usage:

    ```pycon

    >>> from collections import Counter
    >>> from prefvoting.vote import SingleMarkVote
    >>> v = SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3}))
    >>> v
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

    def plurality_winner(self) -> str:
        pass

    def plurality_winners(self) -> tuple[str, ...]:
        # sort by aphabetical order if ties
        pass
