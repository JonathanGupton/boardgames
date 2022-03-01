from collections import deque
from typing import Sequence

from azulsummer.models.board import PlayerBoard
from azulsummer.models.enums import (
    TileColor,
    Phase,
    PlayerActions as P,
    StateActions as S,
)
from azulsummer.models.player import Player
from azulsummer.models.score import Score
from azulsummer.models.tilecollections import (
    FactoryDisplay,
    FactoryMiddle,
    PlayerReserve,
    SupplySpace,
    TileBag,
)

# Number of players : Number of factory displays ratio
PLAYER_TO_DISPLAY_RATIO = {2: 5, 3: 7, 4: 9}

# Wild Tiles in round order
WILD_TILES = [
    TileColor.Purple,
    TileColor.Green,
    TileColor.Orange,
    TileColor.Yellow,
    TileColor.Blue,
    TileColor.Red,
]

# TODO:  Create a to-file method or write bytes to postgres
class State:
    __slots__ = [
        "action_history",
        "available_actions",
        "bag",
        "boards",
        "current_player",
        "factory_displays",
        "middle",
        "next_action",
        "phase",
        "players",
        "reserves",
        "round",
        "score",
        "start_player",
        "supply",
        "turn",
        "wild_tile",
    ]

    def __init__(self, players: Sequence[Player], initialize: bool = True):
        if initialize:
            n_players = len(players)
            self.players = players
            self.boards = [PlayerBoard() for _ in range(n_players)]
            self.reserves = [PlayerReserve() for _ in range(n_players)]
            self.score = Score(n_players)

            # Global tile resources
            self.bag = TileBag()
            self.supply = SupplySpace()
            self.factory_displays = [
                FactoryDisplay() for _ in range(PLAYER_TO_DISPLAY_RATIO[n_players])
            ]
            self.middle = FactoryMiddle()

            # Phase, order, turn values
            self.turn: int = 0
            self.phase: Phase = Phase.AcquireTile
            self.round: int = 0
            self.current_player: int = 0
            self.start_player: int = 0
            self.wild_tile = WILD_TILES[self.round]

            # Previous and future actions
            self.action_history = deque()
            self.available_actions = []
            self.next_action = deque()

            # initialize starting actions
            self.next_action.extend([
                (S.LoadTilesToSupply, 10),
                (S.LoadTilesToFactoryDisplay,),
                (S.IncrementScore, -5),
                (P.AcquireTile,)
            ])

    def assign_start(self) -> None:
        """Assign the current player to start and logs the action"""
        self.start_player = self.current_player
        self.action_history.append(S.AssignStartPlayer)

    def advance_player(self) -> None:
        pass

    def update_score(self, points: int) -> None:
        """Update the player score by points at the current player index"""
        self.score.update(self.current_player, points)

    def add_tiles_to_player_reserve(self, tiles) -> None:
        pass

    def draw_from_middle(self, color: TileColor) -> int:
        """
        Transfer tiles from middle to the player at the current player index

        If the drawn tile is wild, returns one wild tile
        Otherwise returns all tiles of that color and one wild tile (if available)
        Logs the action performed at the end

        Args:
            The color of the tile drawn as TileColor value.
        Returns:
             number of tiles drawn
        """

        if color == self.wild_tile:
            self.reserves[self.current_player][color] += 1
            self.middle[self.wild_tile] -= 1
            drawn_tiles = 1
        else:
            drawn_tiles = self.middle[color]
            self.players[self.current_player] += drawn_tiles
            self.middle[color] = 0

            if self.middle[self.wild_tile]:
                self.players[self.wild_tile] += 1
                self.middle[self.wild_tile] -= 1
                drawn_tiles += 1
        return drawn_tiles

    def draw_from_factory_display(self, display: int, color: TileColor) -> int:
        return 0

    def apply_action(self, action, *args):
        """Method containing game flow logic for the game"""
        match [self.phase, action, self.round]:

            case [Phase.AcquireTile, _, _]:
                pass

            case [Phase.AcquireTile, P.DrawFromFactoryDisplay, _]:
                pass

            case [Phase.AcquireTile, P.DrawFromMiddle, _]:
                n_tiles_drawn = self.draw_from_middle(*args)

                # First player to draw from the middle gets pushed back n_tiles
                if self.start_player is None:
                    self.assign_start()
                    self.update_score(n_tiles_drawn)

            case [Phase.PlayTiles, P.PlaceTile, _] if self.round < 6:
                pass

            case [Phase.PrepareNextRound, S.LoadTilesToFactoryDisplay, round] \
                if self.round < 6:
                pass

            case [Phase.PrepareNextRound, _, round] if self.round == 6:
                # final score
                # declare winner
                pass
