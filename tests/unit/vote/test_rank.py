from __future__ import annotations

import polars as pl
import pytest

from votingsys.vote import (
    RankedVote,
)

################################
#     Tests for RankedVote     #
################################


@pytest.fixture
def ranking() -> pl.DataFrame:
    return pl.DataFrame({"a": [0, 1, 2, 1, 0], "b": [1, 2, 0, 2, 1], "c": [2, 0, 1, 0, 2]})


def test_ranked_vote_repr(ranking: pl.DataFrame) -> None:
    assert repr(RankedVote(ranking)).startswith("RankedVote(")


def test_ranked_vote_str(ranking: pl.DataFrame) -> None:
    assert str(RankedVote(ranking)).startswith("RankedVote(")


def test_ranked_vote_equal_true() -> None:
    assert RankedVote(
        pl.DataFrame({"a": [0, 1, 2, 1, 0], "b": [1, 2, 0, 2, 1], "c": [2, 0, 1, 0, 2]})
    ).equal(
        RankedVote(pl.DataFrame({"a": [0, 1, 2, 1, 0], "b": [1, 2, 0, 2, 1], "c": [2, 0, 1, 0, 2]}))
    )


def test_ranked_vote_equal_false_different_ranking() -> None:
    assert not RankedVote(
        pl.DataFrame({"a": [0, 1, 2, 1, 0], "b": [1, 2, 0, 2, 1], "c": [2, 0, 1, 0, 2]})
    ).equal(
        RankedVote(pl.DataFrame({"a": [0, 0, 0, 0, 0], "b": [1, 1, 1, 1, 1], "c": [2, 2, 2, 2, 2]}))
    )


def test_ranked_vote_equal_false_different_type(ranking: pl.DataFrame) -> None:
    assert not RankedVote(ranking).equal(1)


def test_ranked_vote_get_num_candidates(ranking: pl.DataFrame) -> None:
    assert RankedVote(ranking).get_num_candidates() == 3


def test_ranked_vote_get_num_candidates_2() -> None:
    assert (
        RankedVote(
            pl.DataFrame(
                {
                    "a": [0, 1, 2, 1, 0, 3],
                    "b": [1, 2, 0, 2, 1, 2],
                    "c": [2, 0, 1, 0, 2, 1],
                    "d": [3, 3, 3, 3, 3, 0],
                }
            )
        ).get_num_candidates()
        == 4
    )


def test_ranked_vote_get_num_votes(ranking: pl.DataFrame) -> None:
    assert RankedVote(ranking).get_num_voters() == 5


def test_ranked_vote_get_num_voters_2() -> None:
    assert (
        RankedVote(
            pl.DataFrame(
                {
                    "a": [0, 1, 2, 1, 0, 3],
                    "b": [1, 2, 0, 2, 1, 2],
                    "c": [2, 0, 1, 0, 2, 1],
                    "d": [3, 3, 3, 3, 3, 0],
                }
            )
        ).get_num_voters()
        == 6
    )
