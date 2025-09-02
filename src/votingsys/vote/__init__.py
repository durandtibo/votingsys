r"""Contain the vote implementations."""

from __future__ import annotations

__all__ = ["BaseVote", "MultipleWinnersFoundError", "SingleMarkVote", "WinnerNotFoundError"]

from votingsys.vote.base import (
    BaseVote,
    MultipleWinnersFoundError,
    WinnerNotFoundError,
)
from votingsys.vote.single_mark import SingleMarkVote
