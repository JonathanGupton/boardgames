import pytest

from azulsummer.state import State


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_advance_round_method(n_players):
    """Test advancing the round with the State method."""
    s = State(n_players)
    s.advance_round()
    assert s.round == 0


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_fill_supply_method(n_players):
    """Test filling supply from the State method."""
    s = State(n_players)
    s.fill_supply()
    assert s.tiles.is_supply_full()


@pytest.mark.parametrize("n_players", [2, 3, 4])
def test_fill_factory_displays_method(n_players):
    """Test filling factory display from State method."""
    s = State(n_players)
    s.fill_factory_displays()
    assert s.tiles.get_factory_displays_quantity()


def test_set_start_token():
    """Test the logic around the start token:
    Set a player to start in phase 2 and the subsequent round
    Un-set the player from start during setup for the next phase.
    """
    # TODO
    pass


def test_advance_phase():
    """Test moving from one phase to another from State actions"""
    # TODO
    pass


@pytest.mark.parametrize(
    "n_players,current_player",
    [(2, [0, 1, 0]), (3, [0, 1, 2, 0]), (4, [0, 1, 2, 3, 0])],
)
def test_increment_current_player_method(n_players, current_player):
    """Test advancing the turn to the next player from State method.

    The current player should look back to 0 when hitting the n_player value.
    """
    s = State(n_players)
    for player in current_player:
        assert s.current_player == player
        s.increment_current_player()


def test_creating_tile_selection_options_from_factory_display():
    # TODO
    pass


def test_selecting_tile_selection_from_factory_display():
    """Test selecting a tile from the factory display.
    This should move tiles to the player reserve and potentially to the center.
    This is also impacted by the wild tile.
    """
    # TODO
    pass


def test_selecting_tile_selection_from_table_center():
    """
    Test selecting a tile from the table center to the player reserve.
    This should move tiles to the player reserve and potentially pick up a
    wild tile.
    If the user is the first to pick up a tile it should impact first player
    for next round and score.
    """
    # TODO
    pass


def test_end_phase_one_criteria_are_met():
    """Test if the state recognizes all factory displays and center of the
    table contain no more tiles."""
    # TODO
    pass


def test_end_phase_one_criteria_met_in_the_wrong_phase_raises_error():
    """Test that calling the phase_one_end_criteria_are_met in the wrong phase
    raises an error."""
    # TODO
    pass


def test_end_phase_two_criteria_are_met():
    """Test ."""
    # TODO
    pass


def test_end_phase_two_criteria_met_in_the_wrong_phase_raises_error():
    """Test that calling the phase_two_end_criteria_are_met in the wrong phase
    raises an error."""
    # TODO
    pass


def test_play_tile_to_board_without_draw():
    """Play a single tile to the board, move other tiles to the tower as appropriate without additional draw."""
    # TODO
    pass


def test_play_tile_to_board_and_trigger_pillar_supply_draw():
    # TODO
    pass


def test_play_tile_to_board_and_trigger_statue_supply_draw():
    # TODO
    pass


def test_play_tile_to_board_and_trigger_window_supply_draw():
    # TODO
    pass
