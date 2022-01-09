from typing import Optional, Sequence

from azulsummer.models.board import PlayerBoard
from azulsummer.models.enums import TileColors, Phase
from azulsummer.models.player import Player
from azulsummer.models.score import Score
from azulsummer.models.tilecollections import (
    TileBag,
    MiddleOfFactory,
    FactoryDisplay,
    SupplySpace,
    PlayerReserve,
)

# Number of players : Number of factory displays ratio
PLAYER_TO_DISPLAY_RATIO = {2: 5, 3: 7, 4: 9}

# Wild Tiles in round order
WILD_TILES = [
    TileColors.Purple,
    TileColors.Green,
    TileColors.Orange,
    TileColors.Yellow,
    TileColors.Blue,
    TileColors.Red,
]


# TODO:  Create a to-file method or write bytes to postgres
class State:
    __slots__ = [
        "actions",
        "available_actions",
        "bag",
        "boards",
        "current_player",
        "factory_displays",
        "middle",
        "phase",
        "reserves",
        "round",
        "scores",
        "start_player",
        "supply",
        "turn",
    ]

    def __init__(self, players: Sequence[Player]):
        n_players = len(players)
        self.boards = [PlayerBoard() for _ in range(n_players)]
        self.reserves = [PlayerReserve() for _ in range(n_players)]
        self.scores = Score(n_players)
        self.start_player: Optional[int] = None

        # Global tile resources
        self.bag = TileBag()
        self.supply = SupplySpace()
        self.factory_displays = [
            FactoryDisplay() for _ in range(PLAYER_TO_DISPLAY_RATIO[len(players)])
        ]
        self.middle = MiddleOfFactory()
        self.turn: int = 0
        self.phase: int = 0
        self.round: int = 0
        self.current_player: int = 0

        # Previous and future actions
        self.actions = []
        self.available_actions = []

    def assign_first(self):
        pass


def apply_action(state: State, action, *args, **kwargs):
    match (state.phase, state.round, action):
        case [Phase.AcquireTile, _, _]:
            pass
        case [Phase.PlayTiles, _, _]:
            pass
        case [Phase.PrepareNextRound, state.round, _] if state.round == 6:
            # declare winner
            pass
        case Phase.PrepareNextRound, _, _:
            pass
