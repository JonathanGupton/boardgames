"""Module containing the logic for Phase Two of an Azul Summer Pavilion game"""


def begin_phase_two(action):
    # Advance the phase
    # Advance turn
    # Set phase turn to 0
    # prepare_phase_two_turn()
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
