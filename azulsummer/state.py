
from components import TileColor
from typing import Optional

from azulsummer.models.board import PlayerBoard
from azulsummer.models.player import Player
from azulsummer.models.tilecollections import (
    TileBag,
    MiddleOfFactory,
    FactoryDisplay,
    SupplySpace,
    PlayerReserve,
)


PLAYER_TO_DISPLAY_RATIO = {2: 5, 3: 7, 4: 9}
WILD_TILES = [  # in round order
    TileColor.Purple,
    TileColor.Green,
    TileColor.Orange,
    TileColor.Yellow,
    TileColor.Blue,
    TileColor.Red,
]


# TODO:  Create a to-file method or write bytes to postgres
class State:
    # __slots__ = ['players', 'phase', 'round', 'playable_actions', 'first']

    def __init__(self, players):
        self.boards = [PlayerBoard() for _ in range(len(players))]
        self.reserves = [PlayerReserve() for _ in range(len(players))]
        self.scores = [5 for _ in range(len(players))]
        self.first: int = 0

        # Global tile resources
        self.bag = TileBag()
        self.supply = SupplySpace().from_bag(self.bag)
        self.factory_displays = [
            FactoryDisplay().from_bag(self.bag)
            for _ in range(PLAYER_TO_DISPLAY_RATIO[len(players)])
        ]
        self.middle = MiddleOfFactory()

        self.phase: int = 0
        self.round: int = 0
        self.playable_actions = []

    @property
    def current_player(self) -> Optional[Player]:
        return None

    def assign_first(self):
        pass


def apply_action(state: State, action):
    pass
