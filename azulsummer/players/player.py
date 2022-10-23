"""Module containing the base Player class used for game decision-making."""

from __future__ import annotations

import abc
from abc import ABC


class Player(ABC):
    def __init__(self):
        pass

    def handle(self, message):
        """Function to process incoming messages"""
        pass

    def handle_action(self, state) -> int:
        """Method containing the player decision-making logic.

        Returns the integer index of the action to be taken.
        """
        pass

    def handle_event(self, message):
        pass

    def assess(self, message):
        return self._assess(message)

    @abc.abstractmethod
    def _assess(self, message):
        raise NotImplementedError
