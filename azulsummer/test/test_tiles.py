"""Tests for the Tiles class"""

import numpy as np
import pytest

from azulsummer.models.enums import TileColor
from azulsummer.models.tiles import VALID_TILE_DISTRIBUTION, Tiles


@pytest.mark.parametrize("n_players,n_tiles", [(2, 132), (3, 132), (4, 132)])
def test_instantiation_has_132_tiles(n_players, n_tiles):
    """Test that there are 132 tiles regardless of the number of players."""
    t = Tiles(n_players)
    assert t._tiles.sum() == n_tiles


@pytest.mark.parametrize("n_players,n_rows", [(2, 25), (3, 35), (4, 45)])
def test_n_players_n_tile_rows(n_players, n_rows):
    """Test that the correct number of rows are instantiated based on the
    number of players.
    """
    t = Tiles(n_players)
    assert len(t._tiles) == n_rows


@pytest.mark.parametrize("n_players", [-1, 0, 1, 5, 6])
def test_n_players_out_of_range_error(n_players):
    """Test that <2 or >4 players results in an error when instantiating the
    Tile class
    """
    with pytest.raises(ValueError):
        t = Tiles(n_players)


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_validate_invalid_tile_count(n_players):
    """Test that the validate_tile method raises an error when there are more
    than 132 tiles on the _tile property"""
    t = Tiles(n_players)
    t._tiles[0][0] += 1
    with pytest.raises(ValueError):
        t.validate_tile()


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_validate_invalid_column_tile_count(n_players):
    """Test that the validate_tile method raises an error when any _tile
    column != 22 tiles."""
    t = Tiles(n_players)
    t._tiles[0][0] += 1
    t._tiles[0][1] -= 1
    with pytest.raises(ValueError):
        t.validate_tile()


def test_tiles_equals_valid_tile_distribution():
    t = Tiles(2)
    assert np.array_equal(t._tiles.sum(axis=0), VALID_TILE_DISTRIBUTION)


def test_move_tiles_with_integer_tile():
    """Test moving tiles between two tile locations with int tile location"""
    t = Tiles(2)
    t.move_tiles(0, 1, 0, 22)
    assert t._tiles[0][0] == 0
    assert t._tiles[1][0] == 22


def test_move_tiles_with_tilecolor_enum():
    """Test moving tiles between two tile locations with IntEnum tile location"""
    t = Tiles(2)
    t.move_tiles(0, 1, TileColor.Orange, 22)
    assert t._tiles[0][TileColor.Orange] == 0
    assert t._tiles[1][TileColor.Orange] == 22


def test_move_tiles_value_error():
    """Test a move that results in an invalid tile value"""
    t = Tiles(2)
    with pytest.raises(ValueError):
        t.move_tiles(0, 1, TileColor.Orange, -1)  # overflow results in 255


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_get_bag_quantity_is_132_at_start(n_players):
    t = Tiles(n_players)
    assert t.get_bag_quantity() == 132


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_get_tower_quantity_is_0_at_start(n_players):
    t = Tiles(n_players)
    assert t.get_tower_quantity() == 0


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_refill_bag_from_tower(n_players):
    t = Tiles(n_players)
    t.move_tiles(0, 1, 0, 22)
    t.refill_bag_from_tower()
    assert np.array_equal(t.get_bag_view(), np.array([22, 22, 22, 22, 22, 22]))
    assert np.array_equal(t.get_tower_view(), np.array([0, 0, 0, 0, 0, 0]))


def test_draw_from_bag():
    pass


def test_draw_from_bag_more_than_available_from_bag_but_enough_in_tower():
    pass


def test_draw_from_bag_more_than_available_in_bag_and_tower():
    pass
