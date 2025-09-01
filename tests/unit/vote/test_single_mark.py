from __future__ import annotations

from collections import Counter

import pytest

from prefvoting.vote import (
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
    assert repr(SingleMarkVote(Counter())).startswith("SingleMarkVote(")


def test_single_mark_vote_str() -> None:
    assert str(SingleMarkVote(Counter())).startswith("SingleMarkVote(")


def test_single_mark_vote_equal_true() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).equal(
        SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3}))
    )


def test_single_mark_vote_equal_false_different_counter() -> None:
    assert not SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).equal(
        SingleMarkVote(Counter())
    )


def test_single_mark_vote_equal_false_different_type() -> None:
    assert not SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).equal(1)


def test_single_mark_vote_get_num_candidates() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).get_num_candidates() == 4


def test_single_mark_vote_get_num_candidates_empty() -> None:
    assert SingleMarkVote(Counter()).get_num_candidates() == 0


def test_single_mark_vote_get_num_votes() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).get_num_voters() == 20


def test_single_mark_vote_get_num_voters_empty() -> None:
    assert SingleMarkVote(Counter()).get_num_voters() == 0


def test_single_mark_vote_plurality_winner() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).plurality_winner() == "a"


def test_single_mark_vote_plurality_winner_tie() -> None:
    vote = SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3, "e": 10}))
    with pytest.raises(MultipleWinnersFoundError):
        vote.plurality_winner()


def test_single_mark_vote_plurality_winner_1_candidate() -> None:
    assert SingleMarkVote(Counter({"a": 10})).plurality_winner() == "a"


def test_single_mark_vote_plurality_winner_empty() -> None:
    vote = SingleMarkVote(Counter())
    with pytest.raises(WinnerNotFoundError, match="No winner found because there is no voters"):
        vote.plurality_winner()


def test_single_mark_vote_plurality_winners() -> None:
    assert SingleMarkVote(Counter({"a": 10, "b": 2, "c": 5, "d": 3})).plurality_winners() == ("a",)


def test_single_mark_vote_plurality_winners_tie() -> None:
    assert SingleMarkVote(
        Counter({"a": 10, "b": 2, "c": 5, "d": 3, "e": 10})
    ).plurality_winners() == ("a", "e")


def test_single_mark_vote_plurality_winners_1_candidate() -> None:
    assert SingleMarkVote(Counter({"a": 10})).plurality_winners() == ("a",)


def test_single_mark_vote_plurality_winners_empty() -> None:
    assert SingleMarkVote(Counter()).plurality_winners() == ()
