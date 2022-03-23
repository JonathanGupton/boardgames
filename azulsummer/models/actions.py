"""Module containing logic for generating actions."""

from azulsummer.models.actionvalues import ActionValue
from azulsummer.models.enums import PlayerActions


class Action:
    """Base class for holding action information.

    Action instances hold the arguments used by the apply_action function and
    are also used to store previous actions.
    """
    __slots__ = ["player", "action_type", "values"]

    def __init__(self, player: int, action_type: PlayerActions, values: ActionValue) -> None:
        self.player = player
        self.action_type = action_type
        self.values = values

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.player}, {self.action_type}, {self.values})"


def generate_actions(state) -> list:
    pass
