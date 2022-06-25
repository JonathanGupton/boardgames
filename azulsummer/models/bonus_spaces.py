from __future__ import annotations

from dataclasses import dataclass
from typing import Union

import numpy as np

from azulsummer.models.enums import StarColor


@dataclass(frozen=True)
class Position:
    star: int
    tile_value: int

    def flatten(self) -> int:
        """Convert the 2D (star, tile_value) to the 1D position on the board"""
        return self.star * 6 + self.tile_value - 1


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


@dataclass(frozen=True)
class Pillar:
    adjacent: tuple[int]
    draw_count: int = 1


@dataclass(frozen=True)
class Statue:
    adjacent: tuple[int]
    draw_count: int = 2


@dataclass(frozen=True)
class Window:
    adjacent: tuple[int]
    draw_count: int = 3


def is_bonus_space_surrounded(
    bonus_space: Union[Pillar, Statue, Window], board: np.ndarray
) -> bool:
    """Check if the bonus space is surrounded at all four adjacent locations"""
    return all(board.flatten().take(bonus_space.adjacent))
