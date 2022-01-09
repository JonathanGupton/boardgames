from __future__ import annotations

from enum import Enum, IntEnum, unique, auto


@unique
class TileColors(IntEnum):
    """Tile color indices"""

    Orange = 0
    Red = 1
    Blue = 2
    Yellow = 3
    Green = 4
    Purple = 5


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
class Phase(Enum):
    """Enum representing each phase in a round"""

    AcquireTile = auto()
    PlayTiles = auto()
    PrepareNextRound = auto()


@unique
class PlayerActions(Enum):
    """Enum representing each possible player action"""

    DrawFromSupply = auto()
    DrawFromFactoryDisplay = auto()
    DrawFromMiddle = auto()
    PlaceTile = auto()
    DiscardExcessTiles = auto()


@unique
class StateActions(Enum):
    """Enum representing actions taken by the game state"""

    AdvancePhase = auto()
    AdvanceCurrentPlayerIndex = auto()
    AdvanceTurn = auto()
    AdvanceWildTileIndex = auto()
    AssignStartPlayer = auto()
    IncrementScore = auto()
    LoadBagFromTower = auto()
    LoadFactoryDisplayTiles = auto()
    LoadSupplyTiles = auto()
    LoadTowerTiles = auto()
    LoadMiddleTiles = auto()
    UnassignStartPlayer = auto()
    ScoreEndOfGame = auto()
