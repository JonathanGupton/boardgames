"""Module containing logic for playing tiles to the player board"""
from itertools import product
from typing import Generator

from azulsummer.models.actions import BoardPlacement
from azulsummer.models.board import Board
from azulsummer.models.enums import StarColor
from azulsummer.models.enums import TileColor
from azulsummer.models.game import Game
from azulsummer.models.position import BoardPosition
from azulsummer.models.tile_array import TileArray

MAX_PLACEMENT_COST = 6


def generate_tile_placement_cost_pairs(
    n_color_tiles: int, n_wild_tiles: int
) -> Generator[tuple[int, int], None, None]:
    """Returns (color count, wild tile count) pair costs

    For example,
    generate_tile_placement_cost_pairs(1, 3)
    [(1, 3), (1, 2), (1, 1), (1, 0)]

    generate_tile_placement_cost_pairs(3, 3)
    [(3, 3), (3, 2), (3, 1), (3, 0), (2, 3), (2, 2), (2, 1), (2, 1), (2, 0), (1, 3),
    (1, 2), (1, 1), (1, 0)]
    """
    yield from (
        pair
        for pair in product(range(n_color_tiles, 0, -1), range(n_wild_tiles, -1, -1))
        if sum(pair) <= MAX_PLACEMENT_COST
    )


def tile_array_from_pair(pair, tile_color, wild_color) -> TileArray:
    """Logic for creating Tile Arrays from a tile pair"""
    if pair[1]:
        tile_cost = TileArray.from_dict(
            {tile_color: pair[0], wild_color: pair[1]}
        )
    else:
        tile_cost = TileArray.from_dict(
            {tile_color: pair[0]}
        )
    return tile_cost


def generate_tile_placements(
    game: Game,
    tile_count: int,
    wild_tile_count: int,
    color: TileColor,
    wild_tile_position: int,
) -> Generator[BoardPlacement, None, None]:
    """Responsible for the actual generation of the available placements"""
    for pair in generate_tile_placement_cost_pairs(tile_count, wild_tile_count):
        if color_star_space_is_valid(
            board=game.get_player_board(game.current_player_index),
            color=StarColor(color),
            cost=(star_position := sum(pair)),
        ):
            tile_cost = tile_array_from_pair(pair, color, wild_tile_position)
            yield BoardPlacement(
                game=game,
                board_position=BoardPosition(StarColor(color), star_position),
                tile_cost=tile_cost,
            )
        if wild_star_space_is_valid(
            game=game,
            color=color,
            position=star_position,
        ):
            tile_cost = tile_array_from_pair(pair, color, wild_tile_position)
            yield BoardPlacement(
                game=game,
                board_position=BoardPosition(StarColor.Wild, star_position),
                tile_cost=tile_cost,
            )


def generate_wild_tile_placements(
    game: Game, tile_count, color, wild_tile_position
) -> Generator[BoardPlacement, None, None]:
    """Generate the tile placements for wild tile colors"""
    yield from generate_tile_placements(
        game=game,
        tile_count=tile_count,
        wild_tile_count=0,
        color=color,
        wild_tile_position=wild_tile_position,
    )


def generate_available_player_tile_placements(
    game: Game,
) -> Generator[BoardPlacement, None, None]:
    """Generate the combinations of tiles and board positions that are available to a player."""
    player_hand = game.get_player_reserve(game.current_player_index)
    wild_tile_position = getattr(TileColor, game.wild_tile.name)
    wild_tile_count = game.get_player_reserve_tile_count(
        game.current_player_index, wild_tile_position
    )
    for color, tile_count in enumerate(player_hand):
        if tile_count:
            color = TileColor(color)
            if color != wild_tile_position:
                yield from generate_tile_placements(
                    game=game,
                    tile_count=tile_count,
                    wild_tile_count=wild_tile_count,
                    color=color,
                    wild_tile_position=wild_tile_position,
                )
            else:
                yield from generate_wild_tile_placements(
                    game=game,
                    tile_count=tile_count,
                    color=color,
                    wild_tile_position=wild_tile_position,
                )


def color_star_space_is_valid(board: Board, color: StarColor, cost: int) -> bool:
    """Check if a color star tile placement is valid"""
    return star_space_is_empty(board, color, cost)


def wild_star_space_is_valid(game: Game, color: TileColor, position: int) -> bool:
    """Check if a wild star placement is valid for the current player"""
    return star_space_is_empty(
        game.get_player_board(game.current_player_index), StarColor.Wild, position
    ) and not tile_color_is_already_played_in_wild_star(game, color)


def star_space_is_empty(board: Board, star: StarColor, tile_value: int) -> bool:
    """Check if a tile has been played to a given star color and cost"""
    return board.is_placement_location_open(star, tile_value)


def tile_color_is_already_played_in_wild_star(game: Game, color: TileColor) -> bool:
    """Check if the given color has been played to the current player's WildStar"""
    return game.color_is_played_in_wild_star(game.current_player_index, color)


"""


Examples:

    Returns -> BoardPlacement(position: BoardPosition(Star, TileValue), Cost: TileArray))

    def generate_board_placements(hand, WildTile, board) -> Generator[BoardPlacement]:
        pass

    generate_board_placements([0, 0, 7, 0, 0, 0], <WildTile.Purple: 0>, <empty board>)
    -> [
            BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 1),
                TileArray(0, 0, 1, 0, 0, 0)
            ),
             BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 2),
                TileArray(0, 0, 2, 0, 0, 0)
            ),
            BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 3),
                TileArray(0, 0, 3, 0, 0, 0)
            ),
            BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 4),
                TileArray(0, 0, 4, 0, 0, 0)
            ),
            BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 5),
                TileArray(0, 0, 5, 0, 0, 0)
            ),
            BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 6),
                TileArray(0, 0, 6, 0, 0, 0)
            ),
        ]

    generate_board_placements([0, 3, 0, 0, 0, 0, 0], <WildTile.Purple: 0>, <empty board>)
    -> [
            BoardPlacementAction(
                BoardPosition(<StarColor.Red: 1>, 1),
                TileArray(0, 1, 0, 0, 0, 0)
            ),
             BoardPlacementAction(
                BoardPosition(<StarColor.Red: 1>, 2),
                TileArray(0, 2, 0, 0, 0, 0)
            ),
            BoardPlacementAction(
                BoardPosition(<StarColor.Red: 1>, 3),
                TileArray(0, 3, 0, 0, 0, 0)
            ),
        ]

    generate_board_placements([0, 0, 3, 0, 0, 3], <WildTile.Purple: 0>, <empty board>)
    -> [
            BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 1),
                TileArray(0, 1, 0, 0, 0, 0)
            ),
             BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 2),
                TileArray(0, 2, 0, 0, 0, 0)
            ),
            BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 2),
                TileArray(0, 1, 0, 0, 0, 1)
            ),
            BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 3),
                TileArray(0, 3, 0, 0, 0, 0)
            ),
            BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 3),
                TileArray(0, 2, 0, 0, 0, 1)
            ),
            BoardPlacementAction(
                BoardPosition(<StarColor.Blue: 2>, 3),
                TileArray(0, 1, 0, 0, 0, 2)
            ),
        ]


"""
