from __future__ import annotations

from typing import Sequence
from uuid import uuid4

from azulsummer.models.player import Player
from azulsummer.state import State


class Game:
    def __init__(self, players: Sequence[Player], initialize: bool = True):
        """Initiate a game"""
        if initialize:
            self.id = str(uuid4())
            self.state = State(players)

    def play(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        player = self.state.players[self.state.current_player]
        self.actions = self.state.available_actions

        action = None  # decision function for player

        return self.execute(action)

    def execute(self, action):
        pass
