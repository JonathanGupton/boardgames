from __future__ import annotations

from dataclasses import dataclass


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
