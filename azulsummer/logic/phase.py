

def begin_phase_one():
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


def resolve_phase_one_action():
    # evaluate remaining tiles in the factory and middle
    # - If tiles -
    # -- prepare_phase_one_turn()
    # - If not tiles -
    # -- enqueue begin phase 2 action

    pass


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


def begin_phase_three(action):
    # Advance the WildTile counter by 1
    # Refill factory displays
    #
    pass


def resolve_end_of_game(action):
    # for each player:
    #   Assess points per store
    #   Assess all 1's, 2's, 3's and 4's
    #   Discard remaining tiles and lose points
    pass