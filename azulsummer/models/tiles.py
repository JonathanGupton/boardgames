"""Module containing the Tile class"""
from __future__ import annotations

from typing import Optional

import numpy as np

from azulsummer.models.enums import TileColor, PLAYER_TO_DISPLAY_RATIO


class Tiles:
    """Class to manage the distribution of all game tiles.

    The Tiles class manages the state of all tiles in the game at all times.
    This includes those tiles on the player boards, the player hands,
    the tower, factory display, bag and supply spaces.

    All interactions with the game tiles are managed through the Tiles class.

    Each group of tiles is represented as a 6-wide row in 2D numpy
    array _tiles.
    """

    # There are 22 tiles for each of the 6 colors for a total of 132 tiles
    _TILE_COUNT: int = 22

    # Indices for the tile locations that do not change based on player count
    _BAG_INDEX: int = 0
    _TOWER_INDEX: int = 1
    _TABLE_CENTER_INDEX: int = 2
    _SUPPLY_INDEX: int = 3
    _FACTORY_DISPLAY_INDEX: int = 4

    # 7 rows of 6 are assigned for each player's board
    # 1 row for each color and 1 row for the 'wild' color
    _PLAYER_BOARD_RANGE: int = 7

    def __init__(self, n_players: int, seed: Optional[int] = None) -> None:
        # Check for a valid number of players
        if (n_players < 2) or (n_players > 4):
            raise ValueError(
                f"{n_players} players is invalid.  " f"Must be 2, 3, or 4 players."
            )

        # Set the seed and random number generator
        if seed is None:
            seed = 0
        self.seed = seed
        self.rng: np.random.Generator = np.random.default_rng(seed)

        self.n_players: int = n_players
        self.n_factory_displays: int = PLAYER_TO_DISPLAY_RATIO[n_players]
        self.player_board_index: int = (
                Tiles._FACTORY_DISPLAY_INDEX + self.n_factory_displays
        )
        self.player_reserve_index: int = self.player_board_index + (
                n_players * Tiles._PLAYER_BOARD_RANGE
        )

        n_rows = (
                4  # bag, tower, table center, and supply rows
                + self.n_factory_displays
                + (self.n_players * Tiles._PLAYER_BOARD_RANGE)
                + self.n_players  # player reserves
        )
        self._tiles: np.ndarray = np.zeros((n_rows, len(TileColor)), "B")

        # Create the initial distribution of 22 tiles * 6 tile colors
        self._tiles[0] += np.array([Tiles._TILE_COUNT] * len(TileColor), "B")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(n_players={self.n_players}, seed={self.seed})"
        )

    def get_bag_view(self) -> np.ndarray:
        """Get the distribution of tiles in the bag."""
        return self._tiles[Tiles._BAG_INDEX]

    def get_tower_view(self) -> np.ndarray:
        """Get the distribution of tiles in the tower."""
        return self._tiles[Tiles._TOWER_INDEX]

    def get_table_center_view(self) -> np.ndarray:
        """Get the distribution of tiles in the center of the table."""
        return self._tiles[Tiles._TABLE_CENTER_INDEX]

    def get_supply_view(self) -> np.ndarray:
        """Get the distribution of tiles in the supply."""
        return self._tiles[Tiles._SUPPLY_INDEX]

    def get_factory_displays_view(self) -> np.ndarray:
        """Get the distribution of tiles across all factory displays.

        Returns:
             The tile distributions as a 2D numpy array.
        """
        return self._tiles

    def get_factory_display_n_view(self, factory_display_n: int) -> np.ndarray:
        """Get the distribution of tiles for the given factory display.

        Args:
            factory_display_n:  The integer index of the factory display starting at 0

        Returns:
             The tile distribution as a numpy array.
        """
        pass

    def get_player_boards_view(self) -> np.ndarray:
        """Get the distribution of tiles across all players' boards."""
        return self._tiles[self.player_board_index:]

    def get_player_board_n_view(self, player_n: int) -> np.ndarray:
        """Get the distribution of tiles for the given player board.

        Args:
            player_n: The 0-indexed integer index of the player

        Returns:
            The player board as a 2D 7x6 numpy array
        """
        pass

    def get_player_reserves_view(self) -> np.ndarray:
        """Get the distribution of tiles across all player reserves"""
        pass

    def get_player_n_reserve_view(self, player_n: int) -> np.ndarray:
        """Get the distribution of tiles in reserve that are held by player n."""
        pass

    def fill_supply_space_from_bag(self) -> None:
        """Load the supply space from the bag."""
        pass

    def refill_bag_from_tower(self):
        pass
