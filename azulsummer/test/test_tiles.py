"""Tests for the Tiles class"""

import pytest

from ..models.tiles import Tiles


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


def test_initial_supply_load():
    pass


def test_refill_bag_from_tower():
    pass
