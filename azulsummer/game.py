from __future__ import annotations

from typing import Sequence
from uuid import uuid4

from azulsummer.models.player import Player
from azulsummer.state import State


class Game:
    def __init__(self, players: Sequence[Player], initialize: bool = True):
        """Initiate a game

        Players:  A sequence of class Player.  Player at index 0 will be the
          starting player.



        """
        if initialize:
            self.id = str(uuid4())
            self.state = State(players)

    def play(self):
        while self.state.next_action:
            action, args = self.state.next_action.popleft()

    def __iter__(self):
        return self

    def __next__(self):
        player = self.state.players[self.state.current_player]
        self.actions = self.state.available_actions

        action = None  # decision function for player

        return self.execute(action)

    def execute(self, action):
        pass
