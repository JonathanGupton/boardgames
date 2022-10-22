"""Module containing the game logic acting on the Tile object"""
from __future__ import annotations

from typing import Optional

import numpy as np

from azulsummer.models.actions import FillSupply
from azulsummer.models.enums import TileColor
from azulsummer.models.enums import TileIndex
from azulsummer.models.enums import TileTarget
from azulsummer.models.enums import WildTiles
from azulsummer.models.events import RefillBagFromTower
from azulsummer.models.events import TilesMoved
from azulsummer.models.game import Game
from azulsummer.models.position import DrawPosition
from azulsummer.models.position import TilePosition
from azulsummer.models.tile_array import TileArray
from azulsummer.models.tiles import Tiles


def _generate_draws(
    tile_index: TileIndex,
    tiles_values: np.ndarray,
    tiles_position: int,
    wild_position: TileColor,
    draws: list[DrawPosition],
) -> None:
    # TODO:  Add docstring for _generate_draws function
    # TODO:  Split this into a 'append to draws' func and a 'generate the draws' func
    if tiles_values.sum() == 0:
        return
    wild_value: int = 1 if tiles_values[wild_position] > 0 else 0
    for tile_position, tile_value in enumerate(tiles_values):
        if not tile_value:
            continue
        if tile_position != wild_position:
            draws.append(
                DrawPosition(
                    location=tile_index,
                    tiles_position=tiles_position,
                    tiles=TileArray.from_dict(
                        {tile_index: tile_value, wild_position: wild_value}
                    ),
                )
            )
        else:
            if tiles_values.sum() == tile_value:
                draws.append(
                    DrawPosition(
                        location=TileIndex.FactoryDisplay,
                        tiles_position=tiles_position,
                        tiles=TileArray.from_dict({wild_position: wild_value}),
                    )
                )


def _generate_factory_display_tile_draws(
    tiles: Tiles, wild_position: TileColor, draws: list[DrawPosition]
) -> None:
    for tiles_position, factory_display in enumerate(tiles.view_factory_displays()):
        _generate_draws(
            tile_index=TileIndex.FactoryDisplay,
            tiles_values=factory_display,
            tiles_position=tiles_position,
            wild_position=wild_position,
            draws=draws,
        )


def _generate_table_middle_tile_draws(
    tiles: Tiles, wild_position: TileColor, draws: list[DrawPosition]
) -> None:
    _generate_draws(
        tile_index=TileIndex.TableCenter,
        tiles_values=tiles.view_table_center(),
        tiles_position=0,
        wild_position=wild_position,
        draws=draws,
    )


def generate_acquire_tile_draws(
    tiles: Tiles, wild_color: WildTiles
) -> list[DrawPosition]:
    draw_positions: list[Optional[DrawPosition]] = []
    wild_position: TileColor = TileColor[wild_color.name]
    _generate_factory_display_tile_draws(tiles, wild_position, draw_positions)
    _generate_table_middle_tile_draws(tiles, wild_position, draw_positions)
    return draw_positions


def fill_factory_display(game: Game, nth: int):
    draw_from_bag(
        game=game,
        n_tiles_to_draw=game.factory_display_tile_max,
        destination=TilePosition(TileTarget.FactoryDisplay, nth=nth),
    )


def fill_supply(action: FillSupply) -> None:
    tiles_to_draw: int = action.game.supply_deficit
    draw_from_bag(
        game=action.game,
        n_tiles_to_draw=tiles_to_draw,
        destination=TilePosition(TileTarget.Supply),
    )


def draw_from_bag(game: Game, n_tiles_to_draw: int, destination: TilePosition) -> None:
    """Draw tiles from the bag and transfer the tiles to the destination.

    If n_tiles exceeds the number of tiles in the bag, tiles in the tower
    will be transferred to the bag.

    If n_tiles exceeds the number of tiles in the bag and tower, only those
    in the bag will be transferred.

    Args:
        game: Game
        n_tiles_to_draw: integer number of tiles to move
        destination:  integer index of the destination to receive the tiles

    Returns:
        None
    """
    moved = None
    if game.bag_quantity < n_tiles_to_draw:
        initial_bag_quantity = game.bag_quantity
        moved = game.bag_tiles
        move_tiles(
            game,
            source=TilePosition(TileTarget.Bag),
            destination=destination,
            tiles=game.bag_tiles,
        )
        n_tiles_to_draw -= initial_bag_quantity
        refill_bag_from_tower(game)

    n_tiles_to_draw = min(n_tiles_to_draw, game.bag_quantity)
    delta = game.random.random_tile_distribution(game.bag_tiles, n_tiles_to_draw)
    move_tiles(
        game,
        source=TilePosition(TileTarget.Bag),
        destination=destination,
        tiles=delta,
    )
    moved = moved + delta if moved else delta
    # game.event_queue.append(TilesDrawnFromBag(game, moved))


def parse_position(game, position: TilePosition) -> int:
    if position.location == TileTarget.Bag:
        return game.bag_index
    elif position.location == TileTarget.Tower:
        return game.tower_index
    elif position.location == TileTarget.TableCenter:
        return game.table_center_index
    elif position.location == TileTarget.Supply:
        return game.supply_index
    elif position.location == TileTarget.FactoryDisplay:
        return game.factory_display_index + position.nth
    elif position.location == TileTarget.PlayerBoard:
        return game.player_board_index + (game.player_board_row_count * position.nth)
    elif position.location == TileTarget.PlayerReserve:
        return game.player_reserve_index + position.nth


def move_tiles(
    game: Game, source: TilePosition, destination: TilePosition, tiles: TileArray
) -> None:
    """Move an array of tiles from the source to the destination."""
    source_index = parse_position(game, source)
    destination_index = parse_position(game, destination)
    game.move_tiles(source_index, destination_index, tiles)
    # TODO:  Update TilesMoved event handler to make the source, destination
    #  and array strings rather than doing this at the logic level.  This will
    #  ensure the complete information set will transfer with the event rather
    #  than the stringified version.
    game.enqueue_event(
        TilesMoved(game, str(source), str(destination), str(TileArray(tiles)))
    )


def refill_bag_from_tower(game):
    """Refill the bag with the tower's tiles"""
    if game.tower_quantity:
        move_tiles(
            game,
            source=TilePosition(TileTarget.Tower),
            destination=TilePosition(TileTarget.Bag),
            tiles=game.tower_tiles,
        )
        game.enqueue_event(RefillBagFromTower(game, game.tower_tiles))
