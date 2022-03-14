"""Module containing the named values for Azul Summer Pavilion."""

from __future__ import annotations

from enum import Enum, IntEnum, unique, auto

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

    AcquireTile = auto()
    PlayTiles = auto()
    PrepareNextRound = auto()


@unique
class PlayerActions(Enum):
    """Enum representing each possible player action"""

    AcquireTiles = auto()
    DrawFromFactoryDisplay = auto()
    DrawFromSupply = auto()
    DrawFromMiddle = auto()
    PlaceTile = auto()
    DiscardExcessTiles = auto()
    Pass = auto()


@unique
class StateActions(Enum):
    """Enum representing actions taken by the game state"""

    AdvancePhase = auto()
    AdvanceCurrentPlayerIndex = auto()
    AdvanceTurn = auto()
    AdvanceWildTileIndex = auto()
    AssignStartPlayer = auto()
    DeclareWinner = auto()
    EndOfGameScoring = auto()
    IncrementScore = auto()
    LoadBagFromTower = auto()
    LoadTilesToFactoryDisplay = auto()
    LoadTilesToMiddle = auto()
    LoadTilesToSupply = auto()
    LoadTilesToTower = auto()
    UnassignStartPlayer = auto()
