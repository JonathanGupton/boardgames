from __future__ import annotations

from abc import ABC
from array import array
from random import sample
from typing import Sequence

from azulsummer.components import TileColor

# TODO:  Subclass array.array for the TileCollections to avoid ugly "TileCollection.tile_count" smell OR add index, iterator, slice, etc. methods to the TileCollection
# TODO:  Add a to_file() and from_file() / to_bytes()? from_bytes()? methods? to store the arrays
# TODO:  Move "Refill bag from tower" to be a separately logged action?


class TileCollection(ABC):
    """Base class for Tile Collections"""

    N_TILE_TYPES = 6

    def __init__(self, tile_counts: Sequence[int]):
        if len(tile_counts) != self.N_TILE_TYPES:
            raise ValueError(
                f"tile_counts {tile_counts} value is invalid.  tile_counts must be len of {self.N_TILE_TYPES}."
            )
        self.tile_count = array("B", tile_counts)

    def __repr__(self):
        color_count = {
            TileColor(idx).name: tile_count
            for idx, tile_count in enumerate(self.tile_count)
        }
        return f"{self.__class__.__name__}({color_count})"


    def zero(self):
        """Zero out a tile collection"""
        self.tile_count = [0 for _ in self.tile_count]


class TileBag(TileCollection):
    """Source of tiles for loading the factory displays and supply spaces"""

    def __init__(self):
        initial_tiles = [22] * self.N_TILE_TYPES
        super().__init__(tile_counts=initial_tiles)
        self.tower = Tower()

    def draw(self) -> int:
        """Draw a tile from the bag"""
        if sum(self.tile_count) == 0:
            self.refill_bag_from_tower()
        idx = sample(range(self.N_TILE_TYPES), k=1, counts=self.tile_count)[0]
        self.tile_count[idx] -= 1
        return idx

    def refill_bag_from_tower(self):
        for i, tiles in enumerate(self.tower.tile_count):
            self.tile_count[i] = tiles
        self.tower.zero()

    def add_tiles(self, color: int, n_tiles: int = 1):
        self.tower.tile_count[color] += n_tiles


class Tower(TileCollection):
    """Holds played tiles"""

    def __init__(self):
        initial_tiles = [0] * self.N_TILE_TYPES
        super().__init__(tile_counts=initial_tiles)


class FactoryDisplay(TileCollection):
    """Holds drawable tiles"""

    def __init__(self):
        initial_tiles = [0] * self.N_TILE_TYPES
        super().__init__(tile_counts=initial_tiles)

    def fill_factory_display(self, bag: TileBag):
        """Fill the factory display with 4 tiles from the tile bag"""
        for i in range(4):
            self.tile_count[bag.draw()] += 1

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

    def __init__(self):
        initial_tiles = [0] * self.N_TILE_TYPES
        super().__init__(tile_counts=initial_tiles)

    def fill_supply_space(self, bag):
        for i in range(10):
            self.tile_count[bag.draw()] += 1

    @classmethod
    def from_bag(cls, bag: TileBag) -> SupplySpace:
        supply_space = SupplySpace()
        supply_space.fill_supply_space(bag)
        return supply_space


class PlayerReserve(TileCollection):
    """Tiles held by each player"""

    def __init__(self):
        initial_tiles = [0] * self.N_TILE_TYPES
        super().__init__(tile_counts=initial_tiles)

    def add_tile(self, tile):
        self.tile_count[tile] += 1


class MiddleOfFactory(TileCollection):
    """Tiles holding un-drawn factory display tiles"""

    def __init__(self):
        initial_tiles = [0] * self.N_TILE_TYPES
        super().__init__(tile_counts=initial_tiles)

    def add_tile(self, tile):
        self.tile_count[tile] += 1
