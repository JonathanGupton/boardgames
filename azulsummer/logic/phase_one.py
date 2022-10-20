"""Module containing the logic for Phase One of an Azul Summer Pavilion game"""


def begin_phase_one():
    # - Loading Factory tiles (emit "2 green, 1 red placed on tile 1" or
    #   Event.LoadFactorySpace(space=1, tiles_distrubtion=[])
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


def resolve_phase_one_action():
    # evaluate remaining tiles in the factory and middle
    # - If tiles -
    # -- prepare_phase_one_turn()
    # - If not tiles -
    # -- enqueue begin phase 2 action

    pass
