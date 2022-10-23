from azulsummer.models.enums import StarColor
from azulsummer.models.events import DecrementedPlayerScore
from azulsummer.models.game import Game

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


def evaluate_complete_stars_score(tiles, star: StarColor) -> int:
    # Take the game board, return star count
    pass


def decrement_score(game: Game, points: int) -> None:
    player_index = game.current_player_index
    original_score = game.score[player_index]
    game.score[player_index] -= points
    decreased_by = original_score - game.score[player_index]
    game.enqueue_event(
        DecrementedPlayerScore(
            game=game,
            decreased_by=decreased_by,
            original_score=original_score,
            new_score=game.score[player_index],
        )
    )
