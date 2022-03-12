"""Module containing the State class"""
from collections import deque
from typing import Optional

from azulsummer.models.enums import (
    Phase,
    PlayerActions,
    StateActions,
)
from azulsummer.models.score import Score
from azulsummer.models.tiles import Tiles


class State:
    """The State class manages the state for an Azul Summer Pavilion game.

    Actions that affect the game state are applied via the various State methods.
    """
    def __init__(self, n_players: int, seed: Optional[int] = None) -> None:
        self.n_players = n_players
        self.tiles = Tiles(n_players, seed=seed)
        self.score = Score(n_players)

        # Phase, order, turn values
        self.turn: int = 0
        self.phase: Phase = Phase.AcquireTile
        self.round: int = 0
        self.current_player: int = 0
        self.start_player: int = 0

        # Previous and future actions
        self.action_history = deque()
        self.available_actions = []
        self.next_action = deque()

        # initialize starting actions
        self.next_action.extend([
            (StateActions.LoadTilesToSupply, 10),
            (StateActions.LoadTilesToFactoryDisplay,),
            (StateActions.IncrementScore, -5),
            (PlayerActions.AcquireTile,)
        ])

    def assign_start(self) -> None:
        """Assign the current player to start and logs the action"""
        self.start_player = self.current_player
        self.action_history.append(StateActions.AssignStartPlayer)

    def advance_player(self) -> None:
        pass

    def update_score(self, points: int) -> None:
        """Update the player score by points at the current player index"""
        self.score.update(self.current_player, points)

    def apply_action(self, action, *args):
        """Method containing game flow logic for the game"""
        match [self.phase, action, self.round]:

            case [Phase.AcquireTile, _, _]:
                pass

            case [Phase.AcquireTile, PlayerActions.DrawFromFactoryDisplay, _]:
                pass

            case [Phase.AcquireTile, PlayerActions.DrawFromMiddle, _]:
                n_tiles_drawn = self.draw_from_middle(*args)

                # First player to draw from the middle gets pushed back n_tiles
                if self.start_player is None:
                    self.assign_start()
                    self.update_score(n_tiles_drawn)

            case [Phase.PlayTiles, PlayerActions.PlaceTile, _] if self.round < 6:
                pass

            case [Phase.PrepareNextRound, StateActions.LoadTilesToFactoryDisplay, round] \
                if self.round < 6:
                pass

            case [Phase.PrepareNextRound, _, round] if self.round == 6:
                # final score
                # declare winner
                pass
