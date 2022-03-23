"""Module containing logic for generating actions."""

from abc import ABC, abstractmethod

from azulsummer.models.enums import PlayerActions


class Action(ABC):
    """Base class for holding action information.

    Action instances hold the arguments used by the apply_action function and
    are also used to store previous actions.
    """
    __slots__ = ["player", "action_type", "values"]

    def __init__(self, player: int, action_type: PlayerActions, values: tuple) -> None:
        self.player = player
        self.action_type = action_type
        self.values = values

    @abstractmethod
    def __repr__(self):
        pass


def generate_actions(state) -> list:
    pass
