from __future__ import annotations

from azulsummer.models.board import PlayerBoard
from azulsummer.models.tilecollections import PlayerReserve


class Player:
    def __init__(self):
        self.board = PlayerBoard()
        self.tiles = PlayerReserve()
        self.is_first: bool = False
        self.score = 0
