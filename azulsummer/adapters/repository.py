"""Repository for accessing and storing live games"""

import abc

from azulsummer.models.game import Game


class AbstractRepository(abc.ABC):
    """Base repository for accessing and storing live games"""
    def __init__(self) -> None:
        self.seen = set()

    def get(self, game_id: str) -> Game:
        """Get a Game from the live game repository"""
        return self._get(game_id)

    def save(self, game: Game) -> None:
        """Save a game to the game repository"""
        self._save(game)

    @abc.abstractmethod
    def _get(self, game_id: str) -> Game:
        raise NotImplementedError

    @abc.abstractmethod
    def _save(self, game: Game) -> None:
        raise NotImplementedError


class DictRepository(AbstractRepository):
    def __init__(self) -> None:
        super().__init__()
        self.store = {}

    def _save(self, game: Game) -> None:
        self.store[game.game_id] = game

    def _get(self, game_id: str) -> Game:
        return self.store[game_id]
