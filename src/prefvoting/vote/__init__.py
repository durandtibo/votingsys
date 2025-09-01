r"""Contain the vote implementations."""

from __future__ import annotations

__all__ = ["BaseVote", "SingleMarkVote"]

from prefvoting.vote.base import BaseVote
from prefvoting.vote.single_mark import SingleMarkVote
