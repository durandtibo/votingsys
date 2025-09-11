from __future__ import annotations

import polars as pl
import pytest
from coola import objects_are_equal

from votingsys.vote import (
    RankedVote,
)

################################
#     Tests for RankedVote     #
################################


@pytest.fixture
def ranking() -> pl.DataFrame:
    return pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 5, 2]})


def test_ranked_vote_init_missing_count_col(ranking: pl.DataFrame) -> None:
    with pytest.raises(ValueError, match=r"column 'missing' is missing in the DataFrame:"):
        RankedVote(ranking, count_col="missing")


def test_ranked_vote_ranking(ranking: pl.DataFrame) -> None:
    assert objects_are_equal(
        RankedVote(ranking).ranking,
        pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 5, 2]}),
    )


def test_ranked_vote_repr(ranking: pl.DataFrame) -> None:
    assert repr(RankedVote(ranking)).startswith("RankedVote(")


def test_ranked_vote_str(ranking: pl.DataFrame) -> None:
    assert str(RankedVote(ranking)).startswith("RankedVote(")


def test_ranked_vote_equal_true() -> None:
    assert RankedVote(
        pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 5, 2]})
    ).equal(
        RankedVote(
            pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 5, 2]})
        )
    )


def test_ranked_vote_equal_false_different_ranking() -> None:
    assert not RankedVote(
        pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [3, 5, 2]})
    ).equal(
        RankedVote(
            pl.DataFrame({"a": [0, 1, 2], "b": [1, 2, 0], "c": [2, 0, 1], "count": [2, 1, 3]})
        )
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
                    "a": [0, 1, 2, 3],
                    "b": [1, 2, 0, 2],
                    "c": [2, 0, 1, 1],
                    "d": [3, 3, 3, 0],
                    "count": [3, 5, 2, 1],
                }
            )
        ).get_num_candidates()
        == 4
    )


def test_ranked_vote_get_num_votes(ranking: pl.DataFrame) -> None:
    assert RankedVote(ranking).get_num_voters() == 10


def test_ranked_vote_get_num_voters_2() -> None:
    assert (
        RankedVote(
            pl.DataFrame(
                {
                    "a": [0, 1, 2, 3],
                    "b": [1, 2, 0, 2],
                    "c": [2, 0, 1, 1],
                    "d": [3, 3, 3, 0],
                    "count": [3, 5, 2, 1],
                }
            )
        ).get_num_voters()
        == 11
    )


def test_ranked_vote_from_dataframe() -> None:
    assert RankedVote.from_dataframe(
        pl.DataFrame(
            {
                "a": [0, 0, 0, 1, 1, 1, 1, 1, 2, 2],
                "b": [1, 1, 1, 2, 2, 2, 2, 2, 0, 0],
                "c": [2, 2, 2, 0, 0, 0, 0, 0, 1, 1],
            }
        )
    ).equal(
        RankedVote(
            pl.DataFrame({"a": [1, 0, 2], "b": [2, 1, 0], "c": [0, 2, 1], "count": [5, 3, 2]})
        )
    )


def test_ranked_vote_from_dataframe_count_col() -> None:
    assert RankedVote.from_dataframe(
        pl.DataFrame(
            {
                "a": [0, 0, 0, 1, 1, 1, 1, 1, 2, 2],
                "b": [1, 1, 1, 2, 2, 2, 2, 2, 0, 0],
                "c": [2, 2, 2, 0, 0, 0, 0, 0, 1, 1],
            }
        ),
        count_col="#n",
    ).equal(
        RankedVote(
            pl.DataFrame({"a": [1, 0, 2], "b": [2, 1, 0], "c": [0, 2, 1], "#n": [5, 3, 2]}),
            count_col="#n",
        )
    )


def test_ranked_vote_from_dataframe_count_col_exist() -> None:
    with pytest.raises(ValueError, match=r"column 'c' exists in the DataFrame:"):
        RankedVote.from_dataframe(
            pl.DataFrame(
                {
                    "a": [0, 0, 0, 1, 1, 1, 1, 1, 2, 2],
                    "b": [1, 1, 1, 2, 2, 2, 2, 2, 0, 0],
                    "c": [2, 2, 2, 0, 0, 0, 0, 0, 1, 1],
                }
            ),
            count_col="c",
        )


def test_ranked_vote_from_count_dataframe() -> None:
    assert RankedVote.from_count_dataframe(
        pl.DataFrame(
            {
                "a": [0, 1, 2, 0, 2],
                "b": [1, 2, 0, 1, 1],
                "c": [2, 0, 1, 2, 0],
                "count": [3, 5, 2, 1, 0],
            }
        ),
    ).equal(
        RankedVote(
            pl.DataFrame({"a": [1, 0, 2], "b": [2, 1, 0], "c": [0, 2, 1], "count": [5, 4, 2]})
        )
    )


def test_ranked_vote_from_count_dataframe_count_col() -> None:
    assert RankedVote.from_count_dataframe(
        pl.DataFrame(
            {
                "a": [0, 1, 2, 0, 2],
                "b": [1, 2, 0, 1, 1],
                "c": [2, 0, 1, 2, 0],
                "#n": [3, 5, 2, 1, 0],
            }
        ),
        count_col="#n",
    ).equal(
        RankedVote(
            pl.DataFrame({"a": [1, 0, 2], "b": [2, 1, 0], "c": [0, 2, 1], "#n": [5, 4, 2]}),
            count_col="#n",
        )
    )
