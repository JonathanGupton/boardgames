from typing import Sequence

from azulsummer.models.actions import Action
from azulsummer.players.player import Player


class PlayerInterface:
    def __init__(self, player: Player, actions: Sequence[Action]):
        self.player = player
        self.actions = actions

    def assess(self) -> Action:
        return self.actions[self.player.assess(self.actions)]
