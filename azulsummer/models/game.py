from __future__ import annotations

from collections import deque
from typing import Sequence, Optional
from uuid import uuid4

from azulsummer.models.state import State
from azulsummer.players.player import Player


class Game:
    def __init__(
        self, game_id: str, players: Sequence[Optional[Player]], seed: Optional[int]
    ) -> None:
        """Initiate a game

        Args:
            players:  A sequence of class Player.  Player at index 0 will be
                the starting player.
            seed:  Optional int for the random seed
        """
        self.game_id = game_id
        self.players = players
        self.seed = seed
        self.random = None
        self.action_history = []
        self.events = deque()

        # state must be created with Game.make_state() after assigning players
        # to the game
        self.state = None

    @classmethod
    def new(
        cls, players: Optional[Sequence[Player]] = None, seed: Optional[int] = None
    ):
        """Instantiate a game without player information"""
        players = players if players else []
        seed = seed if seed else None
        return cls(str(uuid4()), players, seed)

    def make_state(self):
        """Create the initial game state for the game"""
        self.state = State.new(len(self.players))
