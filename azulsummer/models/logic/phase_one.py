"""Module containing the logic for Phase One of an Azul Summer Pavilion game"""


def begin_phase_one():
    # load factory displays
    # set player 1
    # reset start token
    # Set first player
    # Reset first_player flag
    # generate_acquire_tile_actions
    pass


def prepare_phase_one_turn():
    # advance to next player
    # advance phase turn
    # Generate available draws and emit to player
    pass


def acquire_tile(action):
    # transfer tile to player hand
    # emit event
    # if tile is the middle and flag is None:  reduce player score by n_tiles
    # emit event
    # transfer remainder to middle
    # emit event
    # resolve_phase_one_action()
    pass


def draw_from_table_center():
    pass


def draw_from_factory_display():
    pass


def discard_to_table_center():
    pass


def decrement_score():
    pass


def set_start_player_token():
    pass


def evaluate_end_of_phase_one():
    pass


def clear_start_player_token():
    pass


def resolve_phase_one_action():
    # evaluate remaining tiles in the factory and middle
    # - If tiles -
    # -- prepare_phase_one_turn()
    # - If not tiles -
    # -- enqueue begin phase 2 action

    pass


def are_phase_one_end_criteria_met() -> bool:
    pass


def fill_supply():
    pass


def load_factory_displays():
    pass


def generate_factory_display_draws():
    pass


def generate_middle_draws():
    pass

