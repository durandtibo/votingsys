from __future__ import annotations

from collections import Counter

import polars as pl
import pytest

from votingsys.vote import (
    MultipleWinnersFoundError,
    SingleMarkVote,
    WinnerNotFoundError,
)

####################################
#     Tests for SingleMarkVote     #
####################################


def test_single_mark_vote_negative_count() -> None:
    with pytest.raises(ValueError, match="The count for 'b' is negative: -2"):
        SingleMarkVote(Counter({"a": 0, "b": -2, "c": 5, "d": 3}))


def test_single_mark_vote_repr() -> None:
    assert repr(SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3}))).startswith(
        "SingleMarkVote("
    )


def test_single_mark_vote_str() -> None:
    assert str(SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3}))).startswith(
        "SingleMarkVote("
    )


def test_single_mark_vote_equal_true() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).equal(
        SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3}))
    )


def test_single_mark_vote_equal_false_different_counter() -> None:
    assert not SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).equal(
        SingleMarkVote(Counter({"a": 10, "b": 2}))
    )


def test_single_mark_vote_equal_false_different_type() -> None:
    assert not SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).equal(1)


def test_single_mark_vote_get_num_candidates() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).get_num_candidates() == 4


def test_single_mark_vote_get_num_candidates_2() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2})).get_num_candidates() == 2


def test_single_mark_vote_get_num_votes() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).get_num_voters() == 20


def test_single_mark_vote_get_num_voters_2() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2})).get_num_voters() == 12


def test_single_mark_vote_absolute_majority_winner_majority() -> None:
    assert (
        SingleMarkVote(Counter({"a": 10, "b": 20, "c": 5, "d": 3})).absolute_majority_winner()
        == "b"
    )


def test_single_mark_vote_absolute_majority_winner_no_majority() -> None:
    vote = SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3, "e": 10}))
    with pytest.raises(WinnerNotFoundError, match="No winner found using absolute majority rule"):
        vote.absolute_majority_winner()


def test_single_mark_vote_absolute_majority_winner_no_absolute_majority() -> None:
    vote = SingleMarkVote(Counter({"a": 10, "b": 10}))
    with pytest.raises(WinnerNotFoundError, match="No winner found using absolute majority rule"):
        vote.absolute_majority_winner()


def test_single_mark_vote_super_majority_winner_majority() -> None:
    assert (
        SingleMarkVote(Counter({"a": 10, "b": 30, "c": 5, "d": 3})).super_majority_winner(0.6)
        == "b"
    )


def test_single_mark_vote_super_winner_no_majority() -> None:
    vote = SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3, "e": 10}))
    with pytest.raises(
        WinnerNotFoundError, match="No winner found using super majority rule with threshold=0.6"
    ):
        vote.super_majority_winner(0.6)


def test_single_mark_vote_super_winner_invalid_threshold() -> None:
    vote = SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3, "e": 10}))
    with pytest.raises(ValueError, match=r"threshold must be >0.5 \(received 0.4\)"):
        vote.super_majority_winner(0.4)


def test_single_mark_vote_plurality_winner() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).plurality_winner() == "a"


def test_single_mark_vote_plurality_winner_tie() -> None:
    vote = SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3, "e": 10}))
    with pytest.raises(
        MultipleWinnersFoundError, match="Multiple winners found using plurality rule:"
    ):
        vote.plurality_winner()


def test_single_mark_vote_plurality_winner_1_candidate() -> None:
    assert SingleMarkVote(Counter({"a": 10})).plurality_winner() == "a"


def test_single_mark_vote_plurality_winners() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).plurality_winners() == ("a",)


def test_single_mark_vote_plurality_winners_tie() -> None:
    assert SingleMarkVote(
        Counter({"a": 10, "b": 2, "c": 5, "d": 3, "e": 10})
    ).plurality_winners() == ("a", "e")


def test_single_mark_vote_plurality_winners_1_candidate() -> None:
    assert SingleMarkVote(Counter({"a": 10})).plurality_winners() == ("a",)


def test_single_mark_vote_from_sequence() -> None:
    assert SingleMarkVote.from_sequence(["a", "b", "a", "c", "a", "a", "b"]).equal(
        SingleMarkVote(Counter({"a": 4, "b": 2, "c": 1}))
    )


def test_single_mark_vote_from_series() -> None:
    assert SingleMarkVote.from_series(pl.Series(["a", "b", "a", "c", "a", "a", "b"])).equal(
        SingleMarkVote(Counter({"a": 4, "b": 2, "c": 1}))
    )
