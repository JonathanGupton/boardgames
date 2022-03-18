"""Module containing the base Player class used for game decision-making."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def assess(self, state) -> int:
        """Method containing the player decision-making logic."""
        pass
