from __future__ import annotations

from typing import Optional

import numpy as np

from azulsummer.models.enums import TileColor


class TileCollection(np.ndarray):
    """Base class for Tile Collections"""

    N_TILE_TYPES = len(TileColor)

    def __new__(cls, arr, *args, **kwargs):
        obj = np.asarray(arr, dtype="B").view(cls)
        return obj

    def __array_finalize__(self, obj):
        """Numpy method required for subclassing np.array"""
        pass

    def __repr__(self):
        color_count = {
            TileColor(idx).name: tile_count
            for idx, tile_count in enumerate(self)
            if tile_count
        }
        return f"{self.__class__.__name__}({color_count})"

    def zero(self):
        """Zero out a tile collection"""
        self.fill(0)

    def is_empty(self) -> bool:
        """Check if the tile collection is empty of tiles"""
        return sum(self) == 0


class TileTransition(TileCollection):
    """Generic collection to transfer tiles between collections"""

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        """Numpy method required for subclassing np.array"""
        pass


class TileBag(TileCollection):
    """
    Source of tiles for loading the factory displays and supply spaces
    Initializes with 22 tiles of each color (132 in total) per the game.
    """

    INITIAL_TILE_COUNT = 22

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        """Numpy method required for subclassing np.array"""
        pass

    def draw(self) -> int:
        """Draw a tile from the bag"""
        pass


class Tower(TileCollection):
    """
    Stores played tiles until the tile bag is empty
    Initializes without any tiles
    """

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        """Numpy method required for subclassing np.array"""
        pass


class FactoryDisplay(TileCollection):
    """Holds drawable factory display tiles"""

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        """Numpy method required for subclassing np.array"""
        pass

    def draw(self, color: TileColor, n_tiles: Optional[int] = None) -> TileTransition:
        """
        Draw the given tile type from the display.

        Args:
          color: The tile color to draw.
          n_tiles: The number of tiles to draw.  The default value of
            None returns all tiles of that color.  Only n_tiles will be
            returned of the given color when specified.

        Returns:
          A TileTransition object with the count of tiles drawn of the given
            color.

        Raises:
            ValueError: If n_tiles is greater than available tiles for the color.
        """

        tile_transition = TileTransition()
        if n_tiles is None:
            tile_transition[color], self[color] = self[color], 0
        else:
            if n_tiles > self[color]:
                raise ValueError(
                    f"Attempted draw of {n_tiles} of {TileColor(color).name} is greater than the available {self[color]} tiles"
                )
            else:
                self[color] -= n_tiles
                tile_transition[color] += n_tiles
        return tile_transition


class SupplySpace(TileCollection):
    """
    10 tile supply to draw from when draw positions are filled e.g.,
    statues, pillars, windows
    """

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        """Numpy method required for subclassing np.array"""
        pass


class PlayerReserve(TileCollection):
    """Tiles held by each player"""

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        """Numpy method required for subclassing np.array"""
        pass


class MiddleOfFactory(TileCollection):
    """Tiles holding un-drawn factory display tiles"""

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        """Numpy method required for subclassing np.array"""
        pass
