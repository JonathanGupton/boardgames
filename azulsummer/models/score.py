import numpy as np

from azulsummer.models.enums import StarColor

# TODO:  Are these value objects really in the right place?
# The point value for completing a star at the end of the game
COMPLETE_STAR_VALUE = {
    StarColor.Wild: 12,
    StarColor.Red: 14,
    StarColor.Blue: 15,
    StarColor.Yellow: 16,
    StarColor.Orange: 17,
    StarColor.Green: 18,
    StarColor.Purple: 20,
}

# The point value gained for covering all star pieces of the given cost,
# e.g., covering the 1's on all stars provides 4 points
COVER_ALL_VALUE = {
    1: 4,
    2: 8,
    3: 12,
    4: 16,
}


class Score(np.ndarray):
    """Base class for player scores

    Score is a subclassed np.ndarray with a length of the number of players
    (n_players).  Score is initialized to the start value of 5 points per
    player.
    """

    def __new__(cls, n_players, *args, **kwargs):
        obj = np.asarray([5] * n_players, dtype=np.uint16).view(cls)
        return obj

    def __array_finalize__(self, obj):
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join([f'P{i}: {n}' for i, n in enumerate(self)])})"

    def update(self, player: int, n_points: int):
        """Increase/decrease the player's score by n_points"""
        self[player] += n_points
