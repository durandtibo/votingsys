r"""Contain the vote implementations."""

from __future__ import annotations

__all__ = ["BaseVote", "MultipleWinnersFoundError", "SingleMarkVote", "WinnerNotFoundError"]

from prefvoting.vote.base import (
    BaseVote,
    MultipleWinnersFoundError,
    WinnerNotFoundError,
)
from prefvoting.vote.single_mark import SingleMarkVote
