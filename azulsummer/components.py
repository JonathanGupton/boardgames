from __future__ import annotations
from enum import IntEnum, unique


@unique
class TileColor(IntEnum):
    """Tile color indices"""

    Orange = 0
    Red = 1
    Blue = 2
    Yellow = 3
    Green = 4
    Purple = 5


