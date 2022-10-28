"""Module containing the logic for Phase Two of an Azul Summer Pavilion game"""

from azulsummer.models.actions import AssignCurrentPlayerToStartPlayer
from azulsummer.models.actions import PhaseTwoPreparationComplete
from azulsummer.models.actions import PlayPhaseTwoTurn
from azulsummer.models.actions import ResetPhaseTurn
from azulsummer.models.actions import SelectTilePlacement
from azulsummer.models.actions import SetAllPlayersActive
from azulsummer.models.events import AllPlayersSetToActive
from azulsummer.models.events import PhaseTwoPrepared
from azulsummer.models.events import PhaseTwoTilePlacementsGenerated
from azulsummer.models.logic.board import generate_available_player_tile_placements


def prepare_phase_two(action):
    actions = [
        ResetPhaseTurn(game=action.game),
        SetAllPlayersActive(game=action.game),
        AssignCurrentPlayerToStartPlayer(game=action.game),
        PhaseTwoPreparationComplete(game=action.game),
    ]
    for action_ in actions:
        action.game.enqueue_action(action_)


def phase_two_preparation_complete(action: PhaseTwoPreparationComplete) -> None:
    action.game.enqueue_event(PhaseTwoPrepared(game=action.game))
    action.game.enqueue_action(PlayPhaseTwoTurn(game=action.game))


def set_all_players_active(action: SetAllPlayersActive) -> None:
    action.game.reset_active_players()
    action.game.enqueue_event(AllPlayersSetToActive(action.game))


def prepare_phase_two_turn(action):
    # -- Advance turn, phase_turn, etc.
    # assess next player - depending on who has passed
    pass


def play_phase_two_turn(action: PlayPhaseTwoTurn):
    board_placements = [*generate_available_player_tile_placements(action.game)]
    action.game.enqueue_event(PhaseTwoTilePlacementsGenerated(action.game, [*map(str, board_placements)]))
    tile_placement = action.game.current_player.assess(
        SelectTilePlacement(action.game, board_placements)
    )
    # action.game.enqueue_event()
    handle_player_action(tile_placement)
    # enqueue_

    pass


def handle_player_action(action):
    # if player_action is Pass:
    #   handle_passing
    # else:
    #    play_tile(action)
    pass


def play_tile(action):
    # Play tile to board
    # Move tiles from hand to board
    # Update score
    # evaluate_bonus_space()

    pass


def handle_player_passing(action):
    # Generate tiles to keep options and emit back to player
    # Discard remaining tiles
    # Update score
    # Remove player from remaining phase two players (game.active_players)
    # Resolve phase two action()
    pass


def resolve_phase_two_action(action):
    # Check if there are still players in phase two
    # - If yes:
    # -- Refill the empty space on the supply spaces

    # -- prepare_phase_two_turn()
    # - If no:
    # -- Is it the end of the game?
    # -- If yes: enqueue resolve_end_of_game()
    # -- If no:  begin_phase_three()
    pass


def set_start_player():
    pass


def increment_score():
    pass


def generate_available_plays():
    pass


def discard_tiles_to_tower():
    pass


def score_tile_placement():
    pass


def evaluate_bonus_positions():
    pass


def generate_supply_space_draws():
    pass


def draw_from_supply_space():
    pass


def pass_turn():
    pass


def generate_saved_tiles_options():
    pass


def evaluate_end_of_phase_two():
    pass


def are_players_playing_in_phase_two() -> bool:
    """Confirm if players are still playing in Phase Two"""
    pass


def evaluate_hand_size():
    pass
