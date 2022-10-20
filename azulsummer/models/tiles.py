"""Module containing the Tile class"""
from __future__ import annotations

from typing import Union

import numpy as np

from azulsummer.models.enums import (
    TileColor,
    PLAYER_TO_DISPLAY_RATIO,
    StarColor,
)

# Referenced in the Tiles.validate_tiles() method
# This is created here to avoid instantiating a new object every time the Tile
# class self validates.
_VALID_TILE_DISTRIBUTION = np.array([22, 22, 22, 22, 22, 22], "B")


class Tiles:
    """Class to manage the distribution of all game tiles.

    The Tiles class manages the state of all tiles in the game at all times.
    This includes those tiles on the player boards, the player hands,
    the tower, factory display, bag, table-center, and supply spaces.

    All direct interactions with the game tiles are handled through the Tiles
    class.

    Each group of tiles is represented as a 6-wide row in the 2D numpy
    array _tiles.
    """

    # TODO:  Add properties and methods to Tiles docstring

    # There are 22 tiles for each of the 6 colors for a total of 132 tiles
    _TILE_COUNT: int = 22

    # Indices for the tile locations that do not change based on player count
    _BAG_INDEX: int = 0
    _TOWER_INDEX: int = 1
    _TABLE_CENTER_INDEX: int = 2
    _SUPPLY_INDEX: int = 3
    _FACTORY_DISPLAY_INDEX: int = 4

    # 7 rows of 6 are assigned for each player's board which is
    #   1 row for each color and 1 row for the 'wild' color
    _PLAYER_BOARD_ROW_COUNT: int = 7

    # Max number of tiles held in the Supply row
    _SUPPLY_TILE_MAX: int = 10

    # Number of tiles held on each factory display
    _FACTORY_DISPLAY_TILE_MAX: int = 4

    def __init__(self, n_players: int, tile_array: np.ndarray) -> None:
        """Initialize a Tile class.

        Tiles begin with the 132 available tiles assigned to the bag.

        Args:
            n_players:  The number of players as an integer

        """
        self._n_players: int = n_players
        self._tiles: np.array = tile_array

    @classmethod
    def new(cls, n_players: int) -> Tiles:
        """Create a new tile array for n_players"""
        n_factory_displays = PLAYER_TO_DISPLAY_RATIO[n_players]

        # Instantiate the tile array
        n_tile_rows = (
            4 + n_factory_displays + n_players * cls._PLAYER_BOARD_ROW_COUNT + n_players
        )
        tiles_array: np.ndarray = np.zeros((n_tile_rows, len(TileColor)), "B")

        # Create the initial distribution of 22 tiles * 6 tile colors
        tiles_array[cls._BAG_INDEX] += np.array([cls._TILE_COUNT] * len(TileColor), "B")

        return cls(n_players, tiles_array)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(n_players={self._n_players}, seed={self._seed})"
        )

    @property
    def _player_board_index(self) -> int:
        return self._FACTORY_DISPLAY_INDEX + self._n_factory_displays

    @property
    def _n_factory_displays(self) -> int:
        return PLAYER_TO_DISPLAY_RATIO[self._n_players]

    @property
    def _player_reserve_index(self) -> int:
        return self._player_board_index + (
            self._n_players * self._PLAYER_BOARD_ROW_COUNT
        )

    """ VIEWS """

    def view_bag(self) -> np.ndarray:
        """Get the distribution of tiles in the bag."""
        return self._tiles[self._BAG_INDEX]

    def get_bag_quantity(self) -> int:
        """Get the total number of tiles in the bag"""
        return self.view_bag().sum()

    def view_tower(self) -> np.ndarray:
        """Get the distribution of tiles in the tower."""
        return self._tiles[self._TOWER_INDEX]

    def get_tower_quantity(self) -> int:
        """Get the total number of tiles in the tower"""
        return self.view_tower().sum()

    def view_table_center(self) -> np.ndarray:
        """Get the distribution of tiles in the center of the table."""
        return self._tiles[self._TABLE_CENTER_INDEX]

    def get_table_center_quantity(self) -> int:
        """Get the number of tiles currently in the table center"""
        return self.view_table_center().sum()

    def view_supply(self) -> np.ndarray:
        """Get the distribution of tiles in the supply."""
        return self._tiles[self._SUPPLY_INDEX]

    def get_supply_quantity(self) -> int:
        """Get the total number of tiles held in supply."""
        return self.view_supply().sum()

    def view_factory_displays(self) -> np.ndarray:
        """Get the distribution of tiles across all factory displays.

        Returns:
             The tile distributions as a 2D numpy array.
        """
        return self._tiles[self._FACTORY_DISPLAY_INDEX : self._player_board_index]

    def get_factory_displays_quantity(self) -> int:
        """Get the total number of tiles across all factory displays."""
        return self.view_factory_displays().sum()

    def view_factory_display_n(self, factory_display_n: int) -> np.ndarray:
        """Get the distribution of tiles for the given factory display.

        Args:
            factory_display_n:  The integer index of the factory display starting at 0

        Returns:
             The tile distribution as a numpy array.
        """
        return self.view_factory_displays()[factory_display_n]

    def view_player_boards(self) -> np.ndarray:
        """Get the distribution of tiles across all players' boards."""
        return self._tiles[self._player_board_index : self._player_reserve_index]

    def view_player_board_n(self, player_n: int) -> np.ndarray:
        """Get the distribution of tiles for the given player board.

        Args:
            player_n: The 0-indexed integer index of the player

        Returns:
            The player board as a 2D 7x6 numpy array
        """
        return self.view_player_boards()[
            player_n
            * self._PLAYER_BOARD_ROW_COUNT : player_n
            * self._PLAYER_BOARD_ROW_COUNT
            + self._PLAYER_BOARD_ROW_COUNT
        ]

    def view_player_reserves(self) -> np.ndarray:
        """Get the distribution of tiles across all player reserves"""
        return self._tiles[
            self._player_reserve_index : self._player_reserve_index + self._n_players
        ]

    def view_player_reserve_n(self, player_n: int) -> np.ndarray:
        """Get the distribution of tiles in reserve that are held by player n."""
        return self.view_player_reserves()[player_n]

    def supply_is_full(self) -> bool:
        """Check if the supply is filled to 10 tiles.

        Returns:
            Bool:  True if the supply has 10 tiles, False if it has <10 tiles.
        """
        return self.get_supply_quantity() == self._SUPPLY_TILE_MAX

    ############  MOVE TILES  ############

    def _move_tiles(
        self,
        source_index: int,
        destination_index: int,
        tiles: np.ndarray,
    ) -> None:
        """
        Move tiles between two tile locations.

        Args:
            source_index:  Integer tile index from which tiles are sent.
            destination_index: Integer tile index where tiles are received.
            tiles: 6 width unsigned int ndarray with corresponding tiles to be
             moved, e.g. np.array([1, 0, 0, 0, 0, 0], "B")

        Returns:
            None
        """
        self._tiles[destination_index] += tiles
        self._tiles[source_index] -= tiles
        self._check_tile_integrity()

    def _draw_from_bag(self, n_tiles_to_draw: int, destination: int) -> None:
        """Draw tiles from the bag and transfer the tiles to the destination.

        If n_tiles exceeds the number of tiles in the bag, tiles in the tower
        will be transferred to the bag.

        If n_tiles exceeds the number of tiles in the bag and tower, only those
        in the bag will be transferred.

        Args:
            n_tiles_to_draw: integer number of tiles to move
            destination:  integer index of the destination to receive the tiles

        Returns:
            None
        """
        # TODO:  Move the handle empty bag logic outside of Tile class

        # Send over tiles and try to refill from tower
        if self.get_bag_quantity() < n_tiles_to_draw:
            bag_tile_count = self.get_bag_quantity()
            self._move_tiles(
                source_index=self._BAG_INDEX,
                destination_index=destination,
                tiles=self._tiles[self._BAG_INDEX],
            )
            n_tiles_to_draw -= bag_tile_count
            self.refill_bag_from_tower()

        # TODO:  Move this logic out of the Tile class
        n_tiles_to_draw = min(n_tiles_to_draw, self.get_bag_quantity())

        # multivariate_hypergeometric draws tiles without replacement from a
        # 1-D array of tiles e.g. [22, 22, 22, 22, 22, 22] results
        # in a distribution of drawn tiles in a 1x6 shape such as
        # [1, 2, 1, 3, 1, 1].
        delta = self._rng.multivariate_hypergeometric(
            self._tiles[self._BAG_INDEX], n_tiles_to_draw
        ).astype("B")

        self._move_tiles(
            source_index=self._BAG_INDEX, destination_index=destination, tiles=delta
        )

    def refill_bag_from_tower(self) -> None:
        """Move all tiles from the Tower to the Bag.

        This method should only be called by the _draw_from_bag() method when
        the bag runs out of tiles.
        """
        self._move_tiles(
            source_index=self._TOWER_INDEX,
            destination_index=self._BAG_INDEX,
            tiles=self._tiles[self._TOWER_INDEX],
        )

    def fill_supply(self) -> None:
        """Fill the supply space to the maximum number of allowed supply tiles.

        This method is called at the start of the game for the initial fill.
        It is also called at the end of a turn when tiles are drawn from the
        supply space.
        """
        unfilled_supply = self._SUPPLY_TILE_MAX - self.get_supply_quantity()
        self._draw_from_bag(unfilled_supply, self._SUPPLY_INDEX)

    def fill_factory_displays(self) -> None:
        """Fill each factory display with 4 tiles drawn from the bag per
        display.

        This method should only be called at the beginning of an 'Acquire Tile'
        round.
        """
        # TODO:  Move this function out of the Tile class

        for display_index in range(
            self._FACTORY_DISPLAY_INDEX, self._player_board_index
        ):
            self._draw_from_bag(self._FACTORY_DISPLAY_TILE_MAX, display_index)

    def draw_from_factory_display(
        self, player: int, factory_display: int, tiles: np.ndarray
    ) -> None:
        """Move tiles from the factory display to the player reserves.

        Args:
            player:  Integer index of the player (0-indexed)
            factory_display: Integer index of the factory display (0-indexed)
            tiles: np.ndarray of tiles to be moved.

        Returns:
            None
        """
        self._move_tiles(
            source_index=self._FACTORY_DISPLAY_INDEX + factory_display,
            destination_index=self._player_reserve_index + player,
            tiles=tiles,
        )

    def _discard_from_factory_display_to_center(self, factory_display: int) -> None:
        """Discard remaining tiles from the given factory display to the
        center.

        Args:
            factory_display:  The integer index of the factory_display to be
              emptied.

        Returns:
            None
        """
        self._move_tiles(
            source_index=self._FACTORY_DISPLAY_INDEX + factory_display,
            destination_index=self._TABLE_CENTER_INDEX,
            tiles=self.view_factory_display_n(factory_display),
        )

    def _discard_from_reserve_to_tower(self, player: int, tiles: np.ndarray) -> None:
        """Discard tiles to the tower from the player reserve.

        Args:
            player: Integer index of the player whose tiles are to be moved
            tiles: np.ndarray of tiles

        Returns:
            None
        """
        self._move_tiles(
            source_index=self._player_reserve_index + player,
            destination_index=self._TOWER_INDEX,
            tiles=tiles,
        )

    def _play_tile_to_color_star(
        self, player: int, cost: int, color: Union[int, TileColor]
    ) -> None:
        """Helper function to play a tile from the player reserve to a colored
        star.

        Args:
            player: Integer index of the player whose tiles are to be moved.
            cost: The integer total cost of tiles spent to place the tile.
            color: TileColor value or integer value associated with the
                    tile color.

        Returns:
            None
        """
        self.view_player_board_n(player)[cost - 1][color] += 1
        self.view_player_reserve_n(player)[color] -= 1
        self._check_tile_integrity()

    def _play_tile_to_wild_star(
        self,
        player: int,
        color: Union[int, TileColor],
    ) -> None:
        """Helper function to play a tile from the player reserve to the wild star.

        Playing to the wild star is seperated from other stars because the wild
        star cost distribution is handled by the state.  Only the color is
        tracked in the Wild Star.

        Args:
             player: Integer index of the player whose tiles are to be moved.
             color:  TileColor value or integer value associated with the tile
                color.

        Returns:
            None
        """
        self.view_player_board_n(player)[StarColor.Wild][color] += 1
        self.view_player_reserve_n(player)[color] -= 1
        self._check_tile_integrity()

    def play_tile(
        self,
        player: int,
        cost: int,
        color: Union[int, TileColor],
        star: Union[int, StarColor],
    ) -> None:
        """Play a tile from the player reserve to the board.

        Args:
            player: Integer index of the player whose tiles are to be moved.
            cost: The integer total cost of tiles spent to place the tile.
            color: TileColor value or integer value associated with the
                    tile color.
            star: The star on which to place the tile.  This is only important
                for the 'Wild' tile that can accept one of each color.

        Returns:
            None
        """
        if star == StarColor.Wild:
            self._play_tile_to_wild_star(player, color)
        else:
            self._play_tile_to_color_star(player, cost, color)

    """ VALIDATION """

    def _check_tile_integrity(self) -> None:
        """Validate that the Tiles.tile object contains exactly 132 tiles and
        each column contains exactly 22 tiles.

        Returns:
            None

        Raises:
            ValueError if an invalid number of tiles are found in the rows or
            columns.
        """
        if np.array_equal(self._tiles.sum(axis=0), _VALID_TILE_DISTRIBUTION):
            return
        raise ValueError(
            f"{self._tiles.sum(axis=0)} is invalid. Only 22 tiles"
            f" are allowed per tile type."
        )
