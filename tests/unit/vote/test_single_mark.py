from __future__ import annotations

from collections import Counter

from prefvoting.vote import SingleMarkVote

####################################
#     Tests for SingleMarkVote     #
####################################


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
