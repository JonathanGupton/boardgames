from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        # TODO:  Fix the repr to include args/kwargs
        return f"{self.__class__.__name__}()"

