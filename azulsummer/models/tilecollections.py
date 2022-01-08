from __future__ import annotations

import numpy as np

from azulsummer.components import TileColor


class TileCollection(np.ndarray):
    """Base class for Tile Collections"""

    N_TILE_TYPES = 6

    def __new__(cls, arr, *args, **kwargs):
        obj = np.asarray(arr, dtype="B").view(cls)
        return obj

    def __array_finalize__(self, obj):
        pass

    def __repr__(self):
        color_count = {
            TileColor(idx).name: tile_count for idx, tile_count in enumerate(self)
        }
        return f"{self.__class__.__name__}({color_count})"

    def zero(self):
        """Zero out a tile collection"""
        self.fill(0)


class TileBag(TileCollection):
    """Source of tiles for loading the factory displays and supply spaces"""

    INITIAL_TILE_COUNT = 22

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        pass

    def draw(self) -> int:
        """Draw a tile from the bag"""
        pass
        # if sum(self.tile_count) == 0:
        #     self.refill_bag_from_tower()
        # idx = sample(range(self.N_TILE_TYPES), k=1, counts=self.tile_count)[0]
        # self.tile_count[idx] -= 1
        # return idx


class Tower(TileCollection):
    """Holds played tiles"""

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        pass


class FactoryDisplay(TileCollection):
    """Holds drawable tiles"""

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        pass

    def fill_factory_display(self, bag):
        pass

    @classmethod
    def from_bag(cls, bag: TileBag) -> FactoryDisplay:
        """Create the initial factory displays drawing tiles from the tile bag"""
        factory_display = FactoryDisplay()
        factory_display.fill_factory_display(bag)
        return factory_display


class SupplySpace(TileCollection):
    """10 tile supply to draw from when draw positions are filled e.g.,
    statues, pillars, windows
    """

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        pass

    def fill_supply_space(self, bag):
        pass
        # for i in range(10):
        #     self.tile_count[bag.draw()] += 1

    @classmethod
    def from_bag(cls, bag: TileBag) -> SupplySpace:
        supply_space = SupplySpace()
        supply_space.fill_supply_space(bag)
        return supply_space


class PlayerReserve(TileCollection):
    """Tiles held by each player"""

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        pass


class MiddleOfFactory(TileCollection):
    """Tiles holding un-drawn factory display tiles"""

    INITIAL_TILE_COUNT = 0

    def __new__(cls, *args, **kwargs):
        initial_tiles = [cls.INITIAL_TILE_COUNT] * super().N_TILE_TYPES
        obj = super().__new__(cls, arr=initial_tiles)
        return obj

    def __array_finalize__(self, obj):
        pass
