"""Module containing the ActionOnePlayer class.  This player always plays the
first action in the action list."""

from __future__ import annotations

import random
from typing import Optional

from azulsummer.players.player import Player


class RandomPlayer(Player):
    """Player class that randomly chooses an available action."""

    def __init__(self, seed: Optional[int]):
        super().__init__()
        self.seed = seed if seed else 1

    def assess(self, state):
        return random.choice(state.available_actions)
