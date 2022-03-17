from __future__ import annotations

from collections import deque
from typing import Sequence, Optional
from uuid import uuid4

from azulsummer.models.player import Player
from azulsummer.state import State


class Game:
    """Class to interface actions between the state and the players."""

    def __init__(self, players: Sequence[Player], seed: Optional[int] = None):
        """Initiate a game

        Args:
            players:  A sequence of class Player.  Player at index 0 will be
                the starting player.
            seed:  Optional int
        """
        self.id = str(uuid4())
        self.players = players
        self.state = State(len(players), seed=seed)
        self.state_history = deque()

    def play(self):
        while self.state.next_action:
            action = self.state.next_action.popleft()

    def execute(self, action):
        pass
