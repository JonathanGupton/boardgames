"""Module containing the logic for Phase Two of an Azul Summer Pavilion game"""


def prepare_phase_two(action):
    # prepare_phase_two_turn()
    # set_start_player()
    print("You've reached phase two - Congratulations!")
    pass


def prepare_phase_two_turn(action):
    # Generate available tile plays + pass for the first player and emit those
    # plays
    pass


def play_tile(action):
    # Play tile to board
    # Move tiles from hand to board
    # Update score
    # Evaluate bonus tile draw

    pass


def pass_playing_tiles(action):
    # Generate tiles to keep options and emit back to player
    # Discard remaining tiles
    # Update score
    # Remove player from remaining phase two players
    # Resolve phase two action()
    pass


def resolve_phase_two_action(action):
    # Check if there are still players in phase two
    # - If yes:
    # -- Refill the empty space on the supply spaces
    # -- Advance turn, phase_turn, etc.
    # -- prepare_phase_two_turn()
    # - If no:
    # -- Is it the end of the game?
    # -- If yes: enqueue resolve_end_of_game()
    # -- If no:  begin_phase_three()
    pass


def set_start_player():
    pass


def increment_score():
    pass


def generate_available_plays():
    pass


def discard_tiles_to_tower():
    pass


def score_tile_placement():
    pass


def evaluate_bonus_positions():
    pass


def generate_supply_space_draws():
    pass


def draw_from_supply_space():
    pass


def pass_turn():
    pass


def generate_saved_tiles_options():
    pass


def evaluate_end_of_phase_two():
    pass


def are_players_playing_in_phase_two() -> bool:
    """Confirm if players are still playing in Phase Two"""
    pass


def evaluate_hand_size():
    pass
