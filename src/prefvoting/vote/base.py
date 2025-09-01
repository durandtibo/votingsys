r"""Contain the base class to implement a vote."""

from __future__ import annotations

__all__ = ["BaseVote"]

from abc import ABC, abstractmethod


class BaseVote(ABC):
    r"""Define the base class to implement a vote."""

    @abstractmethod
    def get_num_candidates(self) -> int:
        r"""Return the number of candidates.

        Returns:
            The number of candidates.
        """

    @abstractmethod
    def get_num_voters(self) -> int:
        r"""Return the number of voters.

        Returns:
            The number of voters.
        """
