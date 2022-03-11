"""Tests for the Tiles class"""

import numpy as np
import pytest

from azulsummer.models.enums import PLAYER_TO_DISPLAY_RATIO
from azulsummer.models.tiles import VALID_TILE_DISTRIBUTION, Tiles


@pytest.mark.parametrize("n_players,n_tiles", [(2, 132), (3, 132), (4, 132)])
def test_instantiation_has_132_tiles(n_players, n_tiles):
    """Test that there are 132 tiles regardless of the number of players."""
    t = Tiles(n_players)
    assert t.tiles.sum() == n_tiles


@pytest.mark.parametrize("n_players,n_rows", [(2, 25), (3, 35), (4, 45)])
def test_n_players_n_tile_rows(n_players, n_rows):
    """Test that the correct number of rows are instantiated based on the
    number of players.
    """
    t = Tiles(n_players)
    assert len(t.tiles) == n_rows


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
    t.tiles[0][0] += 1
    with pytest.raises(ValueError):
        t.validate_tile()


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_validate_invalid_column_tile_count(n_players):
    """Test that the validate_tile method raises an error when any _tile
    column != 22 tiles."""
    t = Tiles(n_players)
    t.tiles[0][0] += 1
    t.tiles[0][1] -= 1
    with pytest.raises(ValueError):
        t.validate_tile()


def test_tiles_equals_valid_tile_distribution():
    t = Tiles(2)
    assert np.array_equal(t.tiles.sum(axis=0), VALID_TILE_DISTRIBUTION)


def test_move_tiles_with_integer_tile():
    """Test moving tiles between two tile locations with int tile location"""
    t = Tiles(2)
    t.move_tiles(0, 1, np.array([22, 0, 0, 0, 0, 0], "B"))
    assert t.tiles[0][0] == 0
    assert t.tiles[1][0] == 22


def test_move_tiles_value_error():
    """Test a move that results in an invalid tile value"""
    t = Tiles(2)
    with pytest.raises(ValueError):
        t.move_tiles(
            0, 1, np.array([-1, 0, 0, 0, 0, 0], "B")
        )  # overflow results in 255


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
    t.tiles[t.BAG_INDEX] *= 0
    t.tiles[t.TOWER_INDEX] += 22
    t.refill_bag_from_tower()
    assert np.array_equal(t.get_bag_view(), np.array([22, 22, 22, 22, 22, 22]))
    assert np.array_equal(t.get_tower_view(), np.array([0, 0, 0, 0, 0, 0]))


def test_draw_from_bag():
    pass


def test_draw_from_bag_more_than_available_from_bag_but_enough_in_tower():
    pass


def test_draw_from_bag_more_than_available_in_bag_and_tower():
    pass


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_is_supply_full_is_false_at_instantiation(n_players):
    """Test that the is_supply_full() method returns False when the
    Tile class is instantiated. ."""
    t = Tiles(n_players)
    assert not t.is_supply_full()


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_is_supply_full_is_true_at_first_fill(n_players):
    """Test that the is_supply_full() method returns True when the
    supply is filled the first time."""
    t = Tiles(n_players)
    t.fill_supply()
    assert t.is_supply_full()


@pytest.mark.parametrize(
    "n_players,factory_idx_min,factory_idx_max,total_tiles,remaining_bag_tiles",
    [(2, 4, 9, 20, 112), (3, 4, 11, 28, 104), (4, 4, 13, 36, 96)],
)
def test_fill_factory_displays(
        n_players, factory_idx_min, factory_idx_max, total_tiles, remaining_bag_tiles
):
    """Test that filling the factory displays loads each display with four
    tiles."""
    t = Tiles(n_players)
    t.fill_factory_displays()
    assert t.tiles[factory_idx_min:factory_idx_max].sum() == total_tiles
    assert t.get_factory_displays_quantity() == total_tiles
    assert t.get_bag_quantity() == remaining_bag_tiles


@pytest.mark.parametrize(
    "n_players,factory_idx_min",
    [(2, 4), (3, 4), (4, 4)],
)
def test_get_nth_factory_display_view(n_players, factory_idx_min):
    """Test that the get_nth_factory_display_view shows the correct factory
    displays."""
    t = Tiles(n_players)
    t.fill_factory_displays()

    n_factory_displays = PLAYER_TO_DISPLAY_RATIO[n_players]
    for idx in range(n_factory_displays):
        assert np.array_equal(
            t.get_nth_factory_display_view(idx), t.tiles[factory_idx_min + idx]
        )


@pytest.mark.parametrize(
    "n_players,rows,cols",
    [(2, 14, 6), (3, 21, 6), (4, 28, 6)],
)
def test_get_player_board_views(n_players, rows, cols):
    """Test get_player_board_views returns the correct number of rows."""
    t = Tiles(n_players)
    assert t.get_player_boards_view().shape == (rows, cols)


def test_play_tile_to_board():
    pass


def test_play_tile_to_center_star():
    pass


def test_get_player_reserves_view():
    pass


def test_get_nth_player_reserve_view():
    pass
