"""Tests for the Tiles class"""

import numpy as np
import pytest

from azulsummer.models.enums import PLAYER_TO_DISPLAY_RATIO, StarColor, TileColor
from azulsummer.models.tiles import (
    VALID_TILE_DISTRIBUTION,
    Tiles,
    tile_distribution_repr,
)


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
        Tiles(n_players)


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_validate_invalid_tile_count(n_players):
    """Test that the validate_tile method raises an error when there are more
    than 132 tiles on the _tile property
    """
    t = Tiles(n_players)
    t.tiles[0][0] += 1
    with pytest.raises(ValueError):
        t.validate_tile()


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_validate_invalid_column_tile_count(n_players):
    """Test that the validate_tile method raises an error when any _tile
    column != 22 tiles.
    """
    t = Tiles(n_players)
    t.tiles[0][0] += 1
    t.tiles[0][1] -= 1
    with pytest.raises(ValueError):
        t.validate_tile()


def test_tiles_equals_valid_tile_distribution():
    """Test that the sum of all tiles is equal to the valid_tile_distribution."""
    t = Tiles(2)
    assert np.array_equal(t.tiles.sum(axis=0), VALID_TILE_DISTRIBUTION)


def test_move_tiles_with_integer_tile():
    """Test moving tiles between two tile locations with int tile location."""
    t = Tiles(2)
    t.move_tiles(0, 1, np.array([22, 0, 0, 0, 0, 0], "B"))
    assert t.tiles[0][0] == 0
    assert t.tiles[1][0] == 22


def test_move_tiles_value_error():
    """Test a move that results in an invalid tile value."""
    t = Tiles(2)
    with pytest.raises(ValueError):
        t.move_tiles(
            0, 1, np.array([-1, 0, 0, 0, 0, 0], "B")
        )  # overflow results in 255


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_get_bag_quantity_is_132_at_start(n_players):
    """Test that the bag starts with 132 tiles at the game start."""
    t = Tiles(n_players)
    assert t.get_bag_quantity() == 132


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_get_tower_quantity_is_0_at_start(n_players):
    """Test that the tower starts with zero tiles at the game start."""
    t = Tiles(n_players)
    assert t.get_tower_quantity() == 0


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_refill_bag_from_tower(n_players):
    """Test refilling the bag from the tower."""
    t = Tiles(n_players)
    t.tiles[t.BAG_INDEX] *= 0
    t.tiles[t.TOWER_INDEX] += 22
    t.refill_bag_from_tower()
    assert np.array_equal(t.get_bag_view(), np.array([22, 22, 22, 22, 22, 22]))
    assert np.array_equal(t.get_tower_view(), np.array([0, 0, 0, 0, 0, 0]))


@pytest.mark.parametrize(
    "n_players",
    [2, 3, 4],
)
def test_draw_from_bag(n_players):
    for i in range(1, 133):
        t = Tiles(n_players)
        t.draw_from_bag(i, t.SUPPLY_INDEX)
        assert np.array_equal(
            VALID_TILE_DISTRIBUTION - t.tiles[t.SUPPLY_INDEX], t.get_bag_view()
        )


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_draw_from_bag_more_than_available_from_bag_but_enough_in_tower(n_players):
    """Test that the draw_from_bag method automatically refills the bag
    from the tower when the number of tiles requested is greater than the
    number of tiles in the bag.
    """
    t = Tiles(n_players)

    # set bag to 0 tiles
    t.tiles[t.BAG_INDEX] *= 0

    # set tower to 4 tiles
    t.tiles[t.TOWER_INDEX] += np.array([2, 2, 0, 0, 0, 0], "B")

    # Move the rest of the tiles to table center and validate
    t.tiles[t.TABLE_CENTER_INDEX] += np.array([20, 20, 22, 22, 22, 22], "B")
    t.validate_tile()

    # Draw 4 tiles from the bag and confirm 4 tiles moved
    t.draw_from_bag(4, t.SUPPLY_INDEX)
    assert np.array_equal(t.get_supply_view(), np.array([2, 2, 0, 0, 0, 0], "B"))


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_draw_from_bag_more_than_available_in_bag_and_tower(n_players):
    """Test that the draw_from_bag method automatically refills then only sends
    over the remaining tiles in the bag.
    """
    t = Tiles(n_players)

    # Set bag to 0 tiles
    t.tiles[t.BAG_INDEX] *= 0

    # Put 3 tiles in the tower
    t.tiles[t.TOWER_INDEX] += np.array([1, 2, 0, 0, 0, 0], "B")

    # Move the rest to the table center and validate that there are still 22
    # tiles per color
    t.tiles[t.TABLE_CENTER_INDEX] += np.array([21, 20, 22, 22, 22, 22], "B")
    t.validate_tile()

    # Draw 6 tiles to supply_index and confirm only 3 tiles moved
    t.draw_from_bag(6, t.SUPPLY_INDEX)
    assert np.array_equal(t.get_supply_view(), np.array([1, 2, 0, 0, 0, 0], "B"))


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_is_supply_full_is_false_at_instantiation(n_players):
    """Test that the is_supply_full() method returns False when the
    Tile class is instantiated.
    """
    t = Tiles(n_players)
    assert not t.is_supply_full()


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_is_supply_full_is_true_at_first_fill(n_players):
    """Test that the is_supply_full() method returns True when the
    supply is filled the first time.
    """
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
    tiles.
    """
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
    displays.
    """
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


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_play_tile_to_board_standard_stars(n_players):
    """
    Load each player with full stack
    for each color and player load
    """
    for player in range(n_players):
        for cost in range(1, 7):
            for color in TileColor:
                for star in StarColor:
                    t = Tiles(n_players)
                    t.move_tiles(
                        t.BAG_INDEX,
                        t.player_reserve_index + player,
                        t.tiles[t.BAG_INDEX],
                    )
                    t.play_tile_to_board(player, cost, color, star)
                    if star == StarColor.Wild:
                        assert (
                            t.get_nth_player_board_view(player)[StarColor.Wild][color]
                            == 1
                        )
                    else:
                        assert t.get_nth_player_board_view(player)[cost - 1][color] == 1


@pytest.mark.parametrize(
    "n_players,positions", [(2, (23, 25)), (3, (32, 35)), (4, (41, 45))]
)
def test_get_player_reserves_view(n_players, positions):
    """Test get_player_reserves_view returns the all player reserves."""
    for position_index in range(*positions):
        t = Tiles(n_players)
        t.move_tiles(t.BAG_INDEX, position_index, t.tiles[t.BAG_INDEX])
        assert np.array_equal(
            t.get_player_reserves_view(), t.tiles[positions[0] : positions[1]]
        )


@pytest.mark.parametrize("n_players,reserve_position", [(2, 23), (3, 32), (4, 41)])
def test_get_nth_player_reserve_view(n_players, reserve_position):
    """Test get_nth_player_reserve_view returns the correct player reserve
    view.
    """
    for player_index in range(n_players):
        t = Tiles(n_players)
        t.move_tiles(
            source_index=t.BAG_INDEX,
            destination_index=t.player_reserve_index + player_index,
            tiles=t.tiles[t.BAG_INDEX],
        )
        assert np.array_equal(
            t.get_nth_player_reserve_view(player_index),
            t.tiles[reserve_position + player_index],
        )


@pytest.mark.parametrize(
    "n_players,seed", [(2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1)]
)
def test_tile_repr(n_players, seed):
    """Test that the tile repr returns a value"""
    t = Tiles(n_players, seed=seed)
    assert repr(t)


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_get_table_center_view(n_players):
    t = Tiles(n_players=n_players)
    t.move_tiles(t.BAG_INDEX, t.TABLE_CENTER_INDEX, t.tiles[t.BAG_INDEX])
    assert np.array_equal(t.get_table_center_view(), t.tiles[t.TABLE_CENTER_INDEX])


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_get_table_center_quantity(n_players):
    t = Tiles(n_players=n_players)
    t.move_tiles(t.BAG_INDEX, t.TABLE_CENTER_INDEX, t.tiles[t.BAG_INDEX])
    assert t.get_table_center_quantity() == 132


def test_get_nth_player_board_view():
    pass


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_draw_from_factory_display(n_players):
    """Test drawing all factory display tiles from a factory display to all
    player reserves"""
    for player in range(n_players):
        for factory_display in range(PLAYER_TO_DISPLAY_RATIO[n_players]):
            # Create a tile object
            t = Tiles(n_players)

            # Fill the supply and factory displays
            t.fill_supply()
            t.fill_factory_displays()

            # Copy the values at the tested factory display by expected index
            to_compare = t.tiles[t.FACTORY_DISPLAY_INDEX + factory_display].copy()

            # Copy values at the factory display via Tiles method to create
            # the array of tiles be drawn
            to_draw = t.get_nth_factory_display_view(factory_display).copy()

            # Move the tiles from the factory display to the player
            t.draw_from_factory_display(player, factory_display, to_draw)

            # Check the tiles moved match the to_compare array and check that
            # the factory display now has 0 tiles in it
            assert np.array_equal(to_compare, t.get_nth_player_reserve_view(player))
            assert t.get_nth_factory_display_view(factory_display).sum() == 0


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_discard_from_factory_display_to_center(n_players):
    """Test discarding from factory display to center for each factory display."""
    for factory_display in range(PLAYER_TO_DISPLAY_RATIO[n_players]):
        # Create a tile object and fill supply and factory displays
        t = Tiles(n_players)
        t.fill_supply()
        t.fill_factory_displays()

        # Copy the value at the nth factory display to to_discard then discard
        # the tiles at the nth factory display to the center
        to_discard = t.get_nth_factory_display_view(factory_display).copy()
        t.discard_from_factory_display_to_center(factory_display)

        # Verify that the new center_view is equal to the copied values and
        # the value at the nth factory display is 0.
        assert np.array_equal(t.get_table_center_view(), to_discard)
        assert t.get_nth_factory_display_view(factory_display).sum() == 0


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_discard_from_reserve_to_tower(n_players):
    # Reference array to be moved and compared against
    to_copy = np.array([1, 2, 3, 4, 5, 6], "B")

    for player in range(n_players):
        t = Tiles(n_players)

        # move the to_copy array from the bag to the player reserve
        t.move_tiles(t.BAG_INDEX, t.player_reserve_index + player, to_copy)

        # discard all tiles in the player reserve to the tower
        t.discard_from_reserve_to_tower(player, to_copy)

        # Verify the player reserve has 0 tiles and the tower has tiles
        # equal to the to_copy array
        assert t.get_nth_player_reserve_view(player).sum() == 0
        assert np.array_equal(t.get_tower_view(), to_copy)


def test_tile_distribution_repr():
    t = Tiles(2)
    t.fill_factory_displays()
    assert tile_distribution_repr(t.get_nth_factory_display_view(0))


def test_tile_distribution_repr_verbose():
    """Test that calling the verbose tile_distribution_repr returns:
        - an empty string when there are zero tiles in a distribution,
        - a full string when there are 0 tiles in the distribtuion, and
        - a verbose and non-verbose call of an array of 0's should return
          different values
        """
    t = Tiles(2)
    assert tile_distribution_repr(t.get_tower_view(), verbose=True)
    assert not tile_distribution_repr(t.get_tower_view(), verbose=False)
    assert tile_distribution_repr(
        t.get_tower_view(), verbose=False
    ) != tile_distribution_repr(t.get_tower_view(), verbose=True)
