"""Module containing the game logic around instantiating and registering games"""
from models import action


def create_new_game(action: action.CreateGame):
    # Create the empty Game object
    # Emit game info to player
    pass


def register_player(action):
    # Register player to a game and the game to a player
    pass


def start_game(action: action.StartGame):
    # Starting the game should instantiate all the game state values
    # You cannot know the board, tile, etc. counts without the players being
    # registered to the game

    # This should enqueue:
    # Call Game Setup
    # - Loading Supply spaces
    # - Loading Factory tiles (emit "2 green, 1 red placed on tile 1" or
    #   Event.LoadFactorySpace(space=1, tiles_distrubtion=[])
    # - Set player scores to 5 for each player
    # - Phase set
    # - Starting player set
    # - Wild Tile set

    # Emit first play action decision
    pass

