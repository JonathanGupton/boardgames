from __future__ import annotations

import numpy as np

N_STARS = 7  # 6 stars + 1 rainbow star
N_PILLARS = 6
N_STATUES = 6
N_WINDOWS = 6


class DrawPosition:
    adjacent_tiles = {}

    def __init__(self):
        self.draw_position = []

    def __contains__(self, item):
        return item in self.adjacent_tiles


class Pillars(DrawPosition):
    adjacent_tiles = {4, 5, 10, 11, 16, 17, 22, 23, 28, 29, 34, 35}


class Statues(DrawPosition):
    adjacent_tiles = {
        0,
        1,
        2,
        3,
        6,
        7,
        8,
        9,
        12,
        13,
        14,
        15,
        18,
        19,
        20,
        21,
        24,
        25,
        26,
        27,
        30,
        31,
        32,
        33,
    }


class Windows(DrawPosition):
    adjacent_tiles = {
        2,
        3,
        8,
        9,
        14,
        15,
        20,
        21,
        26,
        27,
        32,
        33,
        36,
        37,
        38,
        39,
        40,
        41,
    }


class PlayerBoard:
    STATUE_POSITIONS = {
        0,
        1,
        2,
        3,
        6,
        7,
        8,
        9,
        12,
        13,
        14,
        15,
        18,
        19,
        20,
        21,
        24,
        25,
        26,
        27,
        30,
        31,
        32,
        33,
    }
    PILLAR_POSITIONS = {4, 5, 10, 11, 16, 17, 22, 23, 28, 29, 34, 35}
    WINDOW_POSITIONS = {
        2,
        3,
        8,
        9,
        14,
        15,
        20,
        21,
        26,
        27,
        32,
        33,
        36,
        37,
        38,
        39,
        40,
        41,
    }

    # TODO:  Make this a bit array?
    def __init__(self) -> None:
        self.board = np.zeros(shape=(10, 6), dtype="B")

    def __repr__(self) -> str:
        pass

    def place_tile(self, color, value):
        self.board[color * value] = True

    def play_statue_position(self, position: int):
        if position in self.STATUE_POSITIONS:
            pass

    def check_pillar_position(self, position: int):
        pass

    def check_window_position(self, position: int):
        pass

    def is_star_complete(self, star) -> bool:
        return all(self.board[star])

    def are_tile_values_complete(self, tile_value: int) -> bool:
        return all(self.board[0:7, tile_value])


"""
statue - 
    orange 1, orange 2, red 3, red 4
    red 1, red 2, blue 3, blue 4
    blue 1, blue 2, yellow 3, yellow 4
    yellow 1, yellow 2, green 3, green 4
    green 1, green 2, purple 3, purple 4
    purple 1, purple 2, orange 1, orange 2
    
window - 
    orange 5, 6
    red 5, 6
    blue 5, 6
    yellow 5, 6
    green 5, 6
    purple 5, 6
    
pillar -
    orange 2, 3, middle 1, 6
    red 2, 3, middle 1, 2
    blue 2, 3, middle 2, 3
    yellow 2, 3, middle 3, 4
    green 2, 3, middle 4, 5
    purple 2, 3, middle 5, 6


Orange -> Red -> Blue -> Yellow -> Green -> Purple -> Orange
"""
