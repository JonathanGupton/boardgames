"""Module containing classes for referencing board and draw positions"""
from __future__ import annotations

from dataclasses import dataclass

from azulsummer.models.enums import TileIndex
from azulsummer.models.enums import TileTarget
from azulsummer.models.tile_array import TileArray


@dataclass(frozen=True)
class BoardPosition:
    star: int
    tile_value: int

    def flatten(self) -> int:
        """Convert the 2D (star, tile_value) to the 1D position on the board"""
        return self.star * 6 + self.tile_value - 1

    def __iter__(self):
        yield self.star
        yield self.tile_value


@dataclass(frozen=True)
class DrawPosition:
    location: TileIndex
    tiles_position: int = 0
    tiles: TileArray = TileArray([0, 0, 0, 0, 0, 0])


@dataclass
class TilePosition:
    """Dataclass for specifying the location to play a tile to or from which
    to retrieve a tile

    TilePosition is used as an argument in the logic modules
    """

    location: TileTarget
    nth: int = 0

    def __str__(self):
        if self.location in {
            TileTarget.Bag,
            TileTarget.Tower,
            TileTarget.TableCenter,
            TileTarget.Supply,
        }:
            return str(self.location.value)
        else:
            return f"{str(self.location.value)}-{self.nth}"
