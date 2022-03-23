"""Module containing the named values for Azul Summer Pavilion."""

from __future__ import annotations

from enum import Enum, IntEnum, unique, auto

# Ratio of Number of players : Number of factory displays
PLAYER_TO_DISPLAY_RATIO: dict[int, int] = {2: 5, 3: 7, 4: 9}


@unique
class TileColor(IntEnum):
    """Tile color indices"""

    Orange = 0
    Red = 1
    Blue = 2
    Yellow = 3
    Green = 4
    Purple = 5


@unique
class StarColor(IntEnum):
    """Star indices"""

    Orange = 0
    Red = 1
    Blue = 2
    Yellow = 3
    Green = 4
    Purple = 5
    Wild = 6


@unique
class WildTiles(IntEnum):
    """Wild tiles in round order"""

    Purple = 0
    Green = 1
    Orange = 2
    Yellow = 3
    Blue = 4
    Red = 5


@unique
class Phase(IntEnum):
    """Enum representing each phase in a round"""

    acquire_tile = 0
    play_tiles = 1
    prepare_next_round = 2


@unique
class PlayerActions(Enum):
    """Enum representing each possible player action"""

    draw_from_factory_display = auto()
    draw_from_supply = auto()
    draw_from_middle = auto()
    place_tile = auto()
    discard_excess_tiles = auto()
    pass_turn = auto()


@unique
class StateActions(Enum):
    """Enum representing actions taken by the game state"""

    advance_phase = auto()
    advance_current_player_index = auto()
    advance_round = auto()
    advance_turn = auto()
    advance_wild_tile_index = auto()
    assign_start_player = auto()
    declare_winner = auto()
    end_of_game_scoring = auto()
    increment_score = auto()
    load_bag_from_tower = auto()
    load_tiles_to_center = auto()
    load_tiles_to_factory_display = auto()
    load_tiles_to_supply = auto()
    load_tiles_to_tower = auto()
    unassign_start_player = auto()
