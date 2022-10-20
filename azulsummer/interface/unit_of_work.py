from __future__ import annotations

import abc

from adapters import repository


class AbstractUnitOfWork(abc.ABC):
    games: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def collect_new_events(self):
        for game in self.games.seen:
            while game.events:
                yield game.events.popleft()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class DictUnitOfWork(AbstractUnitOfWork):
    games = repository.DictRepository()

    def __init__(self):
        super().__init__()

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass
