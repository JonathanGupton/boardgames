import pytest

from azulsummer.models.board import Board, InvalidTilePlacement
from azulsummer.models.enums import StarColor


def test_board_place_tile():
    board = Board()
    board.place_tile(StarColor.Orange, 1)
    assert board.board[0, 0] == 1

    with pytest.raises(InvalidTilePlacement):
        board.place_tile(StarColor.Orange, 1)


@pytest.mark.parametrize("position", [-1, 0, 7])
@pytest.mark.parametrize("star", iter(StarColor))
def test_invalid_bord_locations(star, position):
    board = Board()

    with pytest.raises(InvalidTilePlacement):
        board.place_tile(star, position)


def test_score_tile_placement_scores_placement_correctly():
    b = Board()
    score = b.place_tile(StarColor.Orange, 1)
    assert score == 1

    score = b.place_tile(StarColor.Orange, 2)
    assert score == 2

    score = b.place_tile(StarColor.Orange, 3)
    assert score == 3

    score = b.place_tile(StarColor.Orange, 5)
    assert score == 1

    score = b.place_tile(StarColor.Orange, 4)
    assert score == 5

    score = b.place_tile(StarColor.Orange, 6)
    assert score == 6


def test_score_count_circles_around_the_star_edge():
    # check that [1, 0, 0, 0, 0, 1] includes both edges in the calculation
    b = Board()
    score = b.place_tile(StarColor.Red, 6)
    assert score == 1

    score = b.place_tile(StarColor.Red, 1)
    assert score == 2

    score = b.place_tile(StarColor.Red, 2)
    assert score == 3


def test_score_doesnt_cross_star_boundaries():
    b = Board()
    score = b.place_tile(StarColor.Orange, 6)
    assert score == 1

    score = b.place_tile(StarColor.Red, 1)
    assert score == 1
