from __future__ import annotations

from collections import deque
from typing import Sequence, Optional
from uuid import uuid4

from azulsummer.players.player import Player
from azulsummer.state import State, apply_action


class Game:
    """Class to interface actions between the state and the players."""

    def __init__(self, players: Sequence[Player], seed: Optional[int] = None) -> None:
        """Initiate a game

        Args:
            players:  A sequence of class Player.  Player at index 0 will be
                the starting player.
            seed:  Optional int for the random seed
        """
        self.id = str(uuid4())
        self.players = players
        self.state = State(len(players), seed=seed)
        self.state_history = deque()

    def play(self) -> int:
        """Play the game.  Return the integer index of the winning player."""
        while self.state.next_action:
            self.play_tick()
        return self.state.winner

    def play_tick(self) -> None:
        """Get the current player to assess their next action."""
        if self.state.available_actions:
            action = self.players[self.state.get_current_player()].assess(self.state)
            self.state.next_action.extendleft(action) # TODO:  Validate extend left enqueues the values in the correct order
        apply_action(self.state)

    def execute_action(self) -> None:
        """Execute the next action in queue."""
        pass

# Ply - One turn taken by one of the players