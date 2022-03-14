"""Module containing the Tile class"""
from __future__ import annotations

from typing import Optional, Union

import numpy as np

from azulsummer.models.enums import TileColor, StarColor, PLAYER_TO_DISPLAY_RATIO

# Referenced in the Tiles.validate_tiles() method
# This is created here to avoid instantiating a new object every time the Tile
# class self validates.
VALID_TILE_DISTRIBUTION = np.array([22, 22, 22, 22, 22, 22], "B")


class Tiles:
    """Class to manage the distribution of all game tiles.

    The Tiles class manages the state of all tiles in the game at all times.
    This includes those tiles on the player boards, the player hands,
    the tower, factory display, bag, table-center, and supply spaces.

    All interactions with the game tiles are managed through the Tiles class.

    Each group of tiles is represented as a 6-wide row in 2D numpy
    array _tiles.
    """
    # TODO:  Add properties and methods to Tiles docstring
    # TODO:  Add __slots__ to Tiles class
    # There are 22 tiles for each of the 6 colors for a total of 132 tiles
    TILE_COUNT: int = 22

    # Indices for the tile locations that do not change based on player count
    BAG_INDEX: int = 0
    TOWER_INDEX: int = 1
    TABLE_CENTER_INDEX: int = 2
    SUPPLY_INDEX: int = 3
    FACTORY_DISPLAY_INDEX: int = 4

    # 7 rows of 6 are assigned for each player's board which is
    #   1 row for each color and 1 row for the 'wild' color
    PLAYER_BOARD_RANGE: int = 7

    # Max number of tiles held in the Supply row
    SUPPLY_TILE_MAX: int = 10

    # Number of tiles held on each factory display
    FACTORY_DISPLAY_TILE_MAX: int = 4

    def __init__(self, n_players: int, seed: Optional[int] = None) -> None:
        """Initialize a Tile class.

        Tiles begin with the 132 available tiles assigned to the bag.

        Args:
            n_players:  The number of players as an integer
            seed:  The RNG seed to be used.
        """
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
            Tiles.FACTORY_DISPLAY_INDEX + self.n_factory_displays
        )
        self.player_reserve_index: int = self.player_board_index + (
            n_players * Tiles.PLAYER_BOARD_RANGE
        )

        n_tile_rows: int = (
            4  # bag, tower, table center, and supply rows
            + self.n_factory_displays
            + (self.n_players * Tiles.PLAYER_BOARD_RANGE)
            + self.n_players  # player reserves
        )
        self.tiles: np.array = np.zeros((n_tile_rows, len(TileColor)), "B")

        # Create the initial distribution of 22 tiles * 6 tile colors
        self.tiles[self.BAG_INDEX] += np.array([Tiles.TILE_COUNT] * len(TileColor), "B")

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(n_players={self.n_players}, seed={self.seed})"
        )

    """ VIEWS """

    def get_bag_view(self) -> np.ndarray:
        """Get the distribution of tiles in the bag."""
        return self.tiles[self.BAG_INDEX]

    def get_bag_quantity(self) -> int:
        """Get the total number of tiles in the bag"""
        return self.get_bag_view().sum()

    def get_tower_view(self) -> np.ndarray:
        """Get the distribution of tiles in the tower."""
        return self.tiles[self.TOWER_INDEX]

    def get_tower_quantity(self) -> int:
        """Get the total number of tiles in the tower"""
        return self.get_tower_view().sum()

    def get_table_center_view(self) -> np.ndarray:
        """Get the distribution of tiles in the center of the table."""
        return self.tiles[self.TABLE_CENTER_INDEX]

    def get_table_center_quantity(self) -> int:
        """Get the number of tiles currently in the table center"""
        return self.get_table_center_view().sum()

    def get_supply_view(self) -> np.ndarray:
        """Get the distribution of tiles in the supply."""
        return self.tiles[self.SUPPLY_INDEX]

    def get_supply_quantity(self) -> int:
        """Get the total number of tiles held in supply."""
        return self.get_supply_view().sum()

    def get_factory_displays_view(self) -> np.ndarray:
        """Get the distribution of tiles across all factory displays.

        Returns:
             The tile distributions as a 2D numpy array.
        """
        return self.tiles[self.FACTORY_DISPLAY_INDEX : self.player_board_index]

    def get_factory_displays_quantity(self) -> int:
        """Get the total number of tiles across all factory displays."""
        return self.get_factory_displays_view().sum()

    def get_nth_factory_display_view(self, factory_display_n: int) -> np.ndarray:
        """Get the distribution of tiles for the given factory display.

        Args:
            factory_display_n:  The integer index of the factory display starting at 0

        Returns:
             The tile distribution as a numpy array.
        """
        return self.get_factory_displays_view()[factory_display_n]

    def get_player_boards_view(self) -> np.ndarray:
        """Get the distribution of tiles across all players' boards."""
        return self.tiles[self.player_board_index : self.player_reserve_index]

    def get_nth_player_board_view(self, player_n: int) -> np.ndarray:
        """Get the distribution of tiles for the given player board.

        Args:
            player_n: The 0-indexed integer index of the player

        Returns:
            The player board as a 2D 7x6 numpy array
        """
        return self.get_player_boards_view()[
            player_n * self.PLAYER_BOARD_RANGE : player_n * self.PLAYER_BOARD_RANGE
            + self.PLAYER_BOARD_RANGE
        ]

    def get_player_reserves_view(self) -> np.ndarray:
        """Get the distribution of tiles across all player reserves"""
        return self.tiles[
            self.player_reserve_index : self.player_reserve_index + self.n_players
        ]

    def get_nth_player_reserve_view(self, player_n: int) -> np.ndarray:
        """Get the distribution of tiles in reserve that are held by player n."""
        return self.get_player_reserves_view()[player_n]

    def is_supply_full(self) -> bool:
        """Check if the supply is filled to 10 tiles.

        Returns:
            Bool:  True if the supply has 10 tiles, False if it has <10 tiles.
        """
        return self.get_supply_quantity() == self.SUPPLY_TILE_MAX

    ############  MOVE TILES  ############

    def move_tiles(
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
        self.tiles[destination_index] += tiles
        self.tiles[source_index] -= tiles
        self.validate_tile()

    def draw_from_bag(self, n_tiles: int, destination: int) -> None:
        """Draw tiles from the bag and transfer the tiles to the destination.

        If n_tiles exceeds the number of tiles in the bag, tiles in the tower
        will be transferred to the bag.

        If n_tiles exceeds the number of tiles in the bag and tower, only those
        in the bag will be transferred.

        Args:
            n_tiles: integer number of tiles to move
            destination:  integer index of the destination to receive the tiles

        Returns:
            None
        """

        # Send over tiles and try to refill from tower
        if self.get_bag_quantity() < n_tiles:
            moved_tiles = self.get_bag_quantity()
            self.move_tiles(
                source_index=self.BAG_INDEX,
                destination_index=destination,
                tiles=self.tiles[self.BAG_INDEX],
            )
            n_tiles -= moved_tiles
            self.refill_bag_from_tower()

        n_tiles = min(n_tiles, self.get_bag_quantity())

        # multivariate_hypergeometric draws tiles without replacement from a
        # 1-D array of tiles e.g. [22, 22, 22, 22, 22, 22] results
        # in a distribution of drawn tiles in a 1x6 shape such as
        # [1, 2, 1, 3, 1, 1].
        delta = self.rng.multivariate_hypergeometric(
            self.tiles[self.BAG_INDEX], n_tiles
        ).astype("B")
        self.move_tiles(
            source_index=self.BAG_INDEX, destination_index=destination, tiles=delta
        )

    def refill_bag_from_tower(self) -> None:
        """Move all tiles from the Tower to the Bag.

        This method should only be called by the draw_from_bag() method when
        the bag runs out of tiles.
        """
        self.move_tiles(
            source_index=self.TOWER_INDEX,
            destination_index=self.BAG_INDEX,
            tiles=self.tiles[self.TOWER_INDEX],
        )

    def fill_supply(self) -> None:
        """Fill the supply space to the maximum number of allowed supply tiles.

        This method is called at the start of the game for the initial fill.
        It is also called at the end of a turn when tiles are drawn from the
        supply space.
        """
        unfilled_supply = self.SUPPLY_TILE_MAX - self.get_supply_quantity()
        self.draw_from_bag(unfilled_supply, self.SUPPLY_INDEX)

    def fill_factory_displays(self) -> None:
        """Fill each factory display with 4 tiles drawn from the bag per
        display.

        This method should only be called at the beginning of an 'Acquire Tile'
        round.
        """
        # TODO:  Consider trying to make this a single action
        #  will need to retool draw_from_bag or move_tiles I suspect to
        #  accommodate 2D arrays.

        for display_index in range(self.FACTORY_DISPLAY_INDEX, self.player_board_index):
            self.draw_from_bag(self.FACTORY_DISPLAY_TILE_MAX, display_index)

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
        self.move_tiles(
            source_index=self.FACTORY_DISPLAY_INDEX + factory_display,
            destination_index=self.player_reserve_index + player,
            tiles=tiles,
        )

    def discard_from_factory_display_to_center(self, factory_display: int) -> None:
        """Discard remaining tiles from the factory display to the center."""
        self.move_tiles(
            source_index=self.FACTORY_DISPLAY_INDEX + factory_display,
            destination_index=self.TABLE_CENTER_INDEX,
            tiles=self.get_nth_factory_display_view(factory_display),
        )

    def discard_from_reserve_to_tower(self, player: int, tiles: np.ndarray) -> None:
        """Discard tiles to the tower from the player reserve.

        Args:
            player: Integer index of the player whose tiles are to be moved
            tiles: np.ndarray of tiles

        Returns:
            None
        """
        self.move_tiles(
            source_index=self.player_reserve_index + player,
            destination_index=self.TOWER_INDEX,
            tiles=tiles,
        )

    def play_tile_to_board(
        self, player: int, cost: int, color: Union[int, StarColor]
    ) -> None:
        """Play a tile from the player reserve to the board.

        Args:
            player: Integer index of the player whose tiles are to be moved.
            cost: The integer total cost of tiles spent to place the tile.
            color: TileColor value or integer value associated with the
                    tile color.

        Returns:
            None
        """
        # Create a tile array and increment the color to be placed on the board
        tiles = np.array([0] * len(TileColor), "B")
        tiles[color] += 1

        self.move_tiles(
            source_index=self.player_reserve_index + player,
            destination_index=self.player_board_index
            + player * self.PLAYER_BOARD_RANGE
            + cost
            - 1,  # offset 1 due to 1-indexed costs
            tiles=tiles,
        )

    """ VALIDATION """

    def validate_tile(self) -> None:
        """Validate that the Tiles.tile object contains exactly 132 tiles and
        each column contains exactly 22 tiles.

        Returns:
            None

        Raises:
            ValueError if an invalid number of tiles are found in the rows or
            columns.
        """
        if np.array_equal(self.tiles.sum(axis=0), VALID_TILE_DISTRIBUTION):
            return
        raise ValueError(
            f"{self.tiles.sum(axis=0)} is invalid. Only 22 tiles"
            f" are allowed per tile type."
        )
