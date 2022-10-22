"""Module containing the named values for Azul Summer Pavilion."""

from __future__ import annotations

from enum import IntEnum, unique, Enum

# Ratio of Number of players : Number of factory displays
PLAYER_TO_DISPLAY_RATIO: dict[int, int] = {2: 5, 3: 7, 4: 9}


@unique
class TileColor(IntEnum):
    """Tile color indices"""

    Orange = 0
    Red = 1
    Blue = 2
    Yellow = 3
    Green = 4
    Purple = 5


@unique
class StarColor(IntEnum):
    """Star indices"""

    Orange = 0
    Red = 1
    Blue = 2
    Yellow = 3
    Green = 4
    Purple = 5
    Wild = 6


@unique
class WildTiles(IntEnum):
    """Wild tiles in round order"""

    Purple = 0
    Green = 1
    Orange = 2
    Yellow = 3
    Blue = 4
    Red = 5


@unique
class Phase(IntEnum):
    """Enum representing each phase in a round"""

    acquire_tile = 0
    play_tiles = 1
    prepare_next_round = 2


class TileIndex(IntEnum):
    """Tile indices for Tile class"""
    Bag = 0
    Tower = 1
    TableCenter = 2
    Supply = 3
    FactoryDisplay = 4


class TileTarget(Enum):
    Bag = "Bag"
    Tower = "Tower"
    TableCenter = "Table Center"
    Supply = "Supply"
    FactoryDisplay = "Factory Display"
    PlayerBoard = "Player Board"
    PlayerReserve = "Player Reserve"
