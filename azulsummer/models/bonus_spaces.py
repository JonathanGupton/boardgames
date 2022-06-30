from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Sequence

from azulsummer.models.board import Board
from azulsummer.models.enums import StarColor
from azulsummer.models.position import Position

_PILLAR_POSITIONS: Sequence[Sequence[Position]] = (
    (
        Position(StarColor.Orange, 2),
        Position(StarColor.Orange, 3),
        Position(StarColor.Wild, 6),
        Position(StarColor.Wild, 1),
    ),
    (
        Position(StarColor.Red, 2),
        Position(StarColor.Red, 3),
        Position(StarColor.Wild, 1),
        Position(StarColor.Wild, 2),
    ),
    (
        Position(StarColor.Blue, 2),
        Position(StarColor.Blue, 3),
        Position(StarColor.Wild, 2),
        Position(StarColor.Wild, 3),
    ),
    (
        Position(StarColor.Yellow, 2),
        Position(StarColor.Yellow, 3),
        Position(StarColor.Wild, 3),
        Position(StarColor.Wild, 4),
    ),
    (
        Position(StarColor.Green, 2),
        Position(StarColor.Green, 3),
        Position(StarColor.Wild, 4),
        Position(StarColor.Wild, 5),
    ),
    (
        Position(StarColor.Purple, 2),
        Position(StarColor.Purple, 3),
        Position(StarColor.Wild, 5),
        Position(StarColor.Wild, 6),
    ),
)

_STATUE_POSITIONS: Sequence[Sequence[Position]] = (
    (
        Position(StarColor.Orange, 1),
        Position(StarColor.Orange, 2),
        Position(StarColor.Red, 3),
        Position(StarColor.Red, 4),
    ),
    (
        Position(StarColor.Red, 1),
        Position(StarColor.Red, 2),
        Position(StarColor.Blue, 3),
        Position(StarColor.Blue, 4),
    ),
    (
        Position(StarColor.Blue, 1),
        Position(StarColor.Blue, 2),
        Position(StarColor.Yellow, 3),
        Position(StarColor.Yellow, 4),
    ),
    (
        Position(StarColor.Yellow, 1),
        Position(StarColor.Yellow, 2),
        Position(StarColor.Green, 3),
        Position(StarColor.Green, 4),
    ),
    (
        Position(StarColor.Green, 1),
        Position(StarColor.Green, 2),
        Position(StarColor.Purple, 3),
        Position(StarColor.Purple, 4),
    ),
    (
        Position(StarColor.Purple, 1),
        Position(StarColor.Purple, 2),
        Position(StarColor.Orange, 3),
        Position(StarColor.Orange, 4),
    ),
)

_WINDOW_POSITIONS: Sequence[Sequence[Position]] = (
    (
        Position(StarColor.Orange, 5),
        Position(StarColor.Orange, 6),
    ),
    (
        Position(StarColor.Red, 5),
        Position(StarColor.Red, 6),
    ),
    (
        Position(StarColor.Blue, 5),
        Position(StarColor.Blue, 6),
    ),
    (
        Position(StarColor.Yellow, 5),
        Position(StarColor.Yellow, 6),
    ),
    (
        Position(StarColor.Green, 5),
        Position(StarColor.Green, 6),
    ),
    (
        Position(StarColor.Purple, 5),
        Position(StarColor.Purple, 6),
    ),
)


@dataclass(frozen=True)
class Pillar:
    adjacent: tuple[int, ...]
    draw_count: int = 1


@dataclass(frozen=True)
class Statue:
    adjacent: tuple[int, ...]
    draw_count: int = 2


@dataclass(frozen=True)
class Window:
    adjacent: tuple[int, ...]
    draw_count: int = 3


class BonusSpace:
    """
    Base class to unite windows, pillars and statues bonus spaces under a
    single API
    """

    _positions = [_PILLAR_POSITIONS, _STATUE_POSITIONS, _WINDOW_POSITIONS]
    _bonus_space_classes = [Pillar, Statue, Window]

    def __init__(self):
        self._bonus_space: set[Pillar | Statue | Window] = set()
        for _class_positions, _class in zip(self._positions, self._bonus_space_classes):
            for group in _class_positions:
                positions: tuple[int, ...] = tuple(p.flatten() for p in group)
                self._bonus_space.add(_class(positions))

    def surrounded_spaces(
        self, board: Board
    ) -> Iterator[Pillar | Statue | Window]:
        for space in self._bonus_space:
            if all(board.board.flatten().take(space.adjacent)):
                yield space

    def remove_space(self, space: Pillar| Statue | Window):
        self._bonus_space.remove(space)

