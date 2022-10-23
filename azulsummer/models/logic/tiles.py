"""Module containing the game logic acting on the Tile object"""
from __future__ import annotations

from itertools import chain
from typing import Generator

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


def generate_draws(
    tile_index: TileIndex,
    tile_distribution: np.ndarray,
    nth_tile_position: int,
    wild_position: TileColor,
) -> Generator[DrawPosition, None, None]:
    if tile_distribution.sum() == 0:
        return
    wild_value: int = min(tile_distribution[wild_position], 1)
    for tile_position, tile_value in enumerate(tile_distribution):
        if not tile_value:
            continue
        if tile_position != wild_position:
            yield DrawPosition(
                location=tile_index,
                tiles_position=nth_tile_position,
                tiles=TileArray.from_dict(
                    {tile_position: tile_value, wild_position: wild_value}
                ),
            )
        else:
            if (tile_position == wild_position) and (
                tile_distribution.sum() == tile_value
            ):
                yield DrawPosition(
                    location=TileIndex.FactoryDisplay,
                    tiles_position=nth_tile_position,
                    tiles=TileArray.from_dict({wild_position: wild_value}),
                )


def generate_factory_display_tile_draws(
    tiles: Tiles, wild_position: TileColor
) -> Generator[DrawPosition, None, None]:
    for tiles_position, factory_display in enumerate(tiles.view_factory_displays()):
        yield from generate_draws(
            tile_index=TileIndex.FactoryDisplay,
            tile_distribution=factory_display,
            nth_tile_position=tiles_position,
            wild_position=wild_position,
        )


def generate_table_middle_tile_draws(
    tiles: Tiles, wild_position: TileColor
) -> Generator[TilePosition, None, None]:
    yield from generate_draws(
        tile_index=TileIndex.TableCenter,
        tile_distribution=tiles.view_table_center(),
        nth_tile_position=0,
        wild_position=wild_position,
    )


def generate_acquire_tile_draws(
    tiles: Tiles, wild_color: WildTiles
) -> Generator[DrawPosition, None, None]:
    """Generate the Acquire Tile draw actions to be assessed by the player"""
    wild_position: TileColor = TileColor[wild_color.name]
    yield from chain(
        generate_factory_display_tile_draws(tiles, wild_position),
        generate_table_middle_tile_draws(tiles, wild_position),
    )


def fill_factory_display(game: Game, nth: int):
    """Load a single factory display"""
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
    if game.bag_quantity < n_tiles_to_draw:
        initial_bag_quantity = game.bag_quantity
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
    else:
        raise ValueError("Position not found")