"""Module containing the game logic around instantiating and registering games"""
from models import action
from models.game import Game
from models.state import State


def create_new_game(action: action.CreateGame):
    state = State(len(action.players))
    game = Game(players=action.players, state=state)


