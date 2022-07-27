from typing import Sequence

import numpy as np

from azulsummer.models.enums import TileColor


class InvalidTileArrayLengthError(Exception):
    pass


class TileArray(np.ndarray):
    """Class to message the movement of tiles from one tile location to another"""

    def __new__(cls, tiles: Sequence[int]):
        if len(tiles) != 6:
            raise InvalidTileArrayLengthError(
                f"Invalid tile length of {len(tiles)}. Must be len of 6."
            )
        tile_array = super().__new__(cls, tiles, "b")
        return tile_array

    def __array_finalize__(self, tile_array):
        pass

    @classmethod
    def from_dict(cls, tiles: dict[TileColor, int]) -> "TileArray":
        """Create a TileArray from a dict of TileColor: Counts"""
        return cls([tiles.get(i, 0) for i in TileColor])
