"""Module containing the game logic acting on the Tile object"""
from __future__ import annotations

from typing import Optional

import numpy as np

from models.enums import TileIndex, TileColor, WildTiles
from models.position import DrawPosition
from models.tile_array import TileArray
from models.tiles import Tiles


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



def handle_empty_bag():
    pass


def fill_factory_displays():
    pass


