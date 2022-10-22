"""Module containing the logic for Phase One of an Azul Summer Pavilion game"""

from azulsummer.models.actions import AssignStartPlayer
from azulsummer.models.actions import FillFactoryDisplays
from azulsummer.models.actions import FillSupply
from azulsummer.models.actions import PhaseOneComplete
from azulsummer.models.actions import PreparePhaseOne
from azulsummer.models.actions import ResetStartToken
from azulsummer.models.events import BeginningPhaseOnePreparation
from azulsummer.models.events import PhaseOnePrepared
from azulsummer.models.logic import tiles


def prepare_phase_one(action: PreparePhaseOne):
    """ "
    Prepare the game for Phase One
    - Load tiles to supply
    - load factory displays
    - Set current_player to first_player
    - Reset first_player flag

    """
    action.game.enqueue_event(BeginningPhaseOnePreparation(game=action.game))
    actions = [
        FillSupply(game=action.game),
        FillFactoryDisplays(game=action.game),
        AssignStartPlayer(game=action.game),
        ResetStartToken(game=action.game),
        PhaseOneComplete(game=action.game),
    ]
    for action_ in actions:
        action.game.enqueue_action(action_)


def phase_one_preparation_complete(action: PhaseOneComplete) -> None:
    """
    This is called at the end of prepare_phase_one to ensure all steps
    are completed before publishing the completion of the event

    This should call the 'generate tiles' action and enqueue calling the player
    """
    action.game.enqueue_event(PhaseOnePrepared(game=action.game))



def prepare_phase_one_turn():
    # advance to next player
    # advance phase turn
    # Generate available draws and emit to player
    pass


def acquire_tile(action):
    # transfer tile to player hand
    # emit event
    # if tile is the middle and flag is None:  reduce player score by n_tiles
    # emit event
    # transfer remainder to middle
    # emit event
    # resolve_phase_one_action()
    pass


def draw_from_table_center():
    pass


def draw_from_factory_display():
    pass


def discard_to_table_center():
    pass


def decrement_score():
    pass


def set_start_player_token():
    pass


def evaluate_end_of_phase_one():
    pass


def clear_start_player_token():
    pass


def resolve_phase_one_action():
    # evaluate remaining tiles in the factory and middle
    # - If tiles -
    # -- prepare_phase_one_turn()
    # - If not tiles -
    # -- enqueue begin phase 2 action

    pass


def are_phase_one_end_criteria_met() -> bool:
    pass


def fill_factory_displays(action: FillFactoryDisplays) -> None:
    for display in range(action.game.n_factory_displays):
        tiles.fill_factory_display(game=action.game, nth=display)


def generate_middle_draws():
    pass
