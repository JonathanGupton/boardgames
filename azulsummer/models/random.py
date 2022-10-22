from __future__ import annotations

from typing import Optional

import numpy as np

from models.tile_array import TileArray


class RandomTileDraw:
    """Class used for randomly generating tile draws"""

    def __init__(self, seed: Optional[int] = None) -> None:
        if seed is None:
            seed = 0
        self.seed = seed
        self.rng: np.random.Generator = np.random.default_rng(seed)

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
