from __future__ import annotations

from typing import Optional

import numpy as np

from models.tile_array import TileArray
from models.tiles import Tiles


class RandomTileDraw:
    """Class used for randomly generating tile draws"""

    def __init__(self, seed: Optional[int] = None) -> None:
        if seed is None:
            seed = 0
        self.seed = seed
        self.rng = np.random.Generator = np.random.default_rng(seed)

    def __repr__(self):
        return f"{self.__class__.__name__}(seed={self.seed})"

    def __eq__(self, other):
        return self.seed == other.seed

    def random_tile_distribution(
        self, tiles: np.ndarray, n_tiles_to_draw: int
    ) -> TileArray:
        return TileArray(
            self.rng.multivariate_hypergeometric(tiles, n_tiles_to_draw).astype("B")
        )

    def bag_draw(self, tiles: Tiles, n_tiles_to_draw: int) -> TileArray:
        """
        Generate a random bag draw.

        Args:
            tiles: Tiles object on which the draw is to be made
            n_tiles_to_draw: integer number of tiles to move

        Returns:
            TileArray containing the tiles to be moved from the bag to the
            destination.
        """
        # multivariate_hypergeometric draws tiles without replacement from a
        # 1-D array of tiles e.g. [22, 22, 22, 22, 22, 22] results
        # in a distribution of drawn tiles in a 1x6 shape such as
        # [1, 2, 1, 3, 1, 1].
        return self.random_tile_distribution(
            tiles=tiles.view_bag(), n_tiles_to_draw=n_tiles_to_draw
        )
