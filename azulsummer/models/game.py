from __future__ import annotations

from typing import Sequence, Optional
from uuid import uuid4

from azulsummer.players.player import Player


class Game:
    def __init__(self, players: Sequence[Player], seed: Optional[int] = None) -> None:
        """Initiate a game

        Args:
            players:  A sequence of class Player.  Player at index 0 will be
                the starting player.
            seed:  Optional int for the random seed
        """
        self.id = str(uuid4())
        self.players = players
        self.seed = seed
        self.random = None


# Ply - One turn taken by one of the players

"""
Create the players
Create a game 

"""