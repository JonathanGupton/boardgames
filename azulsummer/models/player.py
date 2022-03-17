from __future__ import annotations

import random
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def assess(self, state):
        pass


class RandomPlayer(Player):
    """Player class that randomly chooses an available action."""

    def assess(self, state):
        return random.choice(state.available_actions)


class PlaysActionOne(Player):
    """Player class that always plays the first available action."""

    def assess(self, state):
        return state.available_actions[0]
