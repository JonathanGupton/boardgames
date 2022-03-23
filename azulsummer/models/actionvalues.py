from abc import ABC, abstractmethod

import numpy as np


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


class DrawFromFactoryDisplayValues(ActionValue):
    def __init__(self, factory_display: int, tiles: np.ndarray):
        self.factory_display: int = factory_display
        self.tiles: np.ndarray = tiles

    def __str__(self):
        return f"Draw {self.tiles} from Factory Display {self.factory_display}"
