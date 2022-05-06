"""Module containing the Action interface classes"""
from abc import ABC, abstractmethod

from azulsummer.models.player_interface import PlayerInterface


class Action(ABC):
    """
    Command base class to interface various game actions with their
    associated arguments and methods.

    All Actions must have an execute method.  This is called by the game
    to apply the action to the game state.

    The Action base class also supplies the human-readable action
    description for each action.
    """

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        # TODO:  Fix the repr to include args/kwargs
        return f"{self.__class__.__name__}()"


class AdvancePhase(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class AdvanceCurrentPlayerIndex(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class AdvanceRound(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class AdvanceTurn(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class AdvanceWildTileIndex(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class AssignStartPlayer(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class ScoreGame(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class IncrementPlayerScore(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class DecrementPlayerScore(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class LoadBagFromTower(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class LoadTilesToCenter(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class LoadTilesToFactoryDisplay(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class LoadTilesToSupply(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class LoadTilesToTower(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class UnAssignStartPlayer(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class DrawFromFactoryDisplay(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class DrawFromSupply(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class DrawFromMiddle(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class PlayTileToPlayerBoard(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class DiscardExcessTiles(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class PassTurn(Action):
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class MakePlayerActions(Action):
    """Creates a PlayerAction class with current player"""
    def __init__(self):
        super().__init__()

    def execute(self):
        pass

    def __str__(self):
        pass


class GetPlayerAction(Action):
    def __init__(self, state, player_interface: PlayerInterface):
        self.state = state
        self.player_interface = player_interface

    def execute(self):
        action = self.player_interface.assess()

    def __str__(self):
        pass


class PlayerAction(Action):
    def __init__(self, state, action):
        self.state = state
        self.action = action

    def execute(self):
        self.action.execute()

    def __str__(self):
        pass
