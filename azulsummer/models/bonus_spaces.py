from __future__ import annotations

from dataclasses import dataclass
from functools import partial
from typing import Sequence, Union, Type

from azulsummer.models.board import Board
from azulsummer.models.enums import StarColor


@dataclass(frozen=True)
class Position:
    star: int
    tile_value: int

    def flatten(self) -> int:
        """Convert the 2D (star, tile_value) to the 1D position on the board"""
        return self.star * 6 + self.tile_value - 1

    def __iter__(self):
        yield self.star
        yield self.tile_value


_PILLAR_POSITIONS = (
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

_STATUE_POSITIONS = (
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

_WINDOW_POSITIONS = (
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


class BonusSpace:
    """Base class to unite windows, pillars and statues under a single superclass"""

    def __init__(self, *args, **kwargs):
        pass


@dataclass(frozen=True)
class Pillar(BonusSpace):
    adjacent: tuple[int]
    draw_count: int = 1


@dataclass(frozen=True)
class Statue(BonusSpace):
    adjacent: tuple[int]
    draw_count: int = 2


@dataclass(frozen=True)
class Window(BonusSpace):
    adjacent: tuple[int]
    draw_count: int = 3


def is_bonus_space_surrounded(
    bonus_space: Union[Pillar, Statue, Window], board: Board
) -> bool:
    """Check if the bonus space is surrounded at all four adjacent locations"""
    return all(board.board.flatten().take(bonus_space.adjacent))


def _make_bonus_space_collection(
    bonus_space_positions: Sequence[Sequence[Position]], class_type: Type[BonusSpace]
):
    """Create a set of all bonus space coordinates."""
    bonus_space = set()
    for group in bonus_space_positions:
        positions = tuple(p.flatten() for p in group)
        bonus_space.add(class_type(positions))
    return bonus_space


make_pillars = partial(_make_bonus_space_collection, _PILLAR_POSITIONS, Pillar)
make_windows = partial(_make_bonus_space_collection, _WINDOW_POSITIONS, Window)
make_statues = partial(_make_bonus_space_collection, _STATUE_POSITIONS, Statue)
