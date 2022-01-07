from __future__ import annotations
from typing import Iterable, Optional
from uuid import uuid4

from azulsummer.models.player import Player
from azulsummer.state import State
from azulsummer.components import TileColor
from azulsummer.models.tilecollections import TileBag, Tower, FactoryDisplay, SupplySpace


class Game:

    def __init__(self, players: Iterable[Player], initialize: bool = True):
        """Initiate a game"""
        if initialize:
            self.id = str(uuid4())
            self.state = State(players)

    def play(self):
        pass

    def next_player_action(self):
        pass

    def execute(self):
        pass

    @property
    def winner(self) -> Optional[Player]:
        pass


class Score:
    pass


class Turn:
    pass


class Phase:
    pass


class AcquireTiles(Phase):
    pass


class PlayTilesAndScore(Phase):
    pass
