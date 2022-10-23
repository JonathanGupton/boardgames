"""Module containing the ActionOnePlayer class.  This player always plays the
first action in the action list."""

from __future__ import annotations

import random
from typing import Optional

from azulsummer.players.player import Player


class RandomPlayer(Player):
    """Player class that randomly chooses an available action."""

    def __init__(self, seed: Optional[int] = None) -> None:
        super().__init__()
        self.seed = seed if seed else 1

    def _assess(self, action):
        return random.choice(action.available_actions)
