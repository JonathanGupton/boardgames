from abc import ABC, abstractmethod
from typing import Union

import numpy as np

from azulsummer.models.enums import TileColor, StarColor
from azulsummer.models.tiles import tile_distribution_repr


class ActionValue(ABC):
    """Class for representing the arguments associated with each action type.

    The class arguments should be the same as the class properties, e.g.,

      def __init__(self, argument_name):
          self.argument_name = argument_name

    This is necessary for the repr to accurately reflect the class data.

    The action value arguments should match the method arguments used in the
    Tiles and State classes.
    """

    @abstractmethod
    def __init__(self):
        pass

    def __repr__(self):
        vals = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({vals})"

    @abstractmethod
    def __str__(self):
        """Implement the argument string associated with the action values.

        E.g., 'draw X tiles from factory display Y'

        """
        pass


# PLAYER ACTIONS

class DiscardExcessTilesValues(ActionValue):
    """ActionValues associated with discard tiles from the player hand
    to the tower.

    This is action associated with tile placements to the board and the end
    of the Play Tiles phase.
    """
    def __init__(self, tiles: np.ndarray) -> None:
        self.tiles = tiles

    def __str__(self) -> str:
        """
        'Orange: 1, Red: 1, Blue: 1, Yellow: 1, Green: 1, Purple: 1 are discarded to the Tower'
        """
        return f"{tile_distribution_repr(self.tiles)} are discarded to the Tower"

class DrawFromCenterValues(ActionValue):
    """ActionValues for a player drawing tiles from the table center.
    """

    def __init__(self, tiles: np.ndarray) -> None:
        self.tiles = tiles

    def __str__(self):
        """
        'Draw Orange: 3, Blue: 2 from the Table Center'
        """
        return f"Draw {tile_distribution_repr(self.tiles)} from the Table Center"


class DrawFromFactoryDisplayValues(ActionValue):
    """ActionValues for a player drawing from a factory display."""

    def __init__(self, factory_display: int, tiles: np.ndarray):
        self.factory_display: int = factory_display
        self.tiles: np.ndarray = tiles

    def __str__(self):
        """
        'Draw Orange: 3, Blue: 2 from Factory Display 0'
        """
        return f"Draw {tile_distribution_repr(self.tiles)} from Factory Display {self.factory_display}"


class DrawFromSupplyValues(ActionValue):
    """ActionValues for a player drawing tiles from the supply field."""

    def __init__(self, tiles: np.ndarray) -> None:
        self.tiles: np.ndarray = tiles

    def __str__(self):
        """
        'Draw Orange: 3, Blue: 2 from Supply'
        """
        return f"Draw {tile_distribution_repr(self.tiles)} from Supply"


class PassValues(ActionValue):
    """ActionValue for a player passing for their remaining turns."""
    def __init__(self):
        pass

    def __str__(self):
        return "Pass for remaining turns"


class PlayTileToBoardValues(ActionValue):
    """ActionValue for a player playinga tile to their board."""
    def __init__(
        self, cost: int, color: Union[int, TileColor], star: Union[int, StarColor]
    ) -> None:
        self.cost = cost
        self.color = color
        self.star = star

    def __str__(self):
        """
        'Play a 1 cost Red tile to the Red star'
        'Play a 3 cost Purple tile to the Wild star'
        """
        return f"Play a {self.cost} cost {TileColor(self.color).name} tile to the {StarColor(self.star).name} star"
