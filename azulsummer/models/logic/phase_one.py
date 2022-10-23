"""Module containing the logic for Phase One of an Azul Summer Pavilion game"""

from azulsummer.models.actions import AdvancePhase
from azulsummer.models.actions import AssessPhaseOneTileDrawAction
from azulsummer.models.actions import AssignCurrentPlayerToStartPlayer
from azulsummer.models.actions import FillFactoryDisplays
from azulsummer.models.actions import FillSupply
from azulsummer.models.actions import PhaseOneComplete
from azulsummer.models.actions import PlayPhaseOneTurn
from azulsummer.models.actions import PreparePhaseOne
from azulsummer.models.actions import PreparePhaseOneTurn
from azulsummer.models.actions import PreparePhaseTwo
from azulsummer.models.actions import ResetStartPlayerToken
from azulsummer.models.actions import ResolvePhaseOneTurn
from azulsummer.models.enums import TileTarget
from azulsummer.models.events import BeginningPhaseOnePreparation
from azulsummer.models.events import BeginningTurn
from azulsummer.models.events import DiscardTilesFromFactoryDisplayToTableCenter
from azulsummer.models.events import PhaseOneDrawsGenerated
from azulsummer.models.events import PhaseOneEndCriteriaHaveBeenMet
from azulsummer.models.events import PhaseOnePrepared
from azulsummer.models.events import PlayerIsFirstToDrawFromTableCenter
from azulsummer.models.events import PlayerSelectedTilesToAcquire
from azulsummer.models.events import StartPlayerTokenWasSet
from azulsummer.models.game import Game
from azulsummer.models.logic import all_phase
from azulsummer.models.logic import score
from azulsummer.models.logic import tiles
from azulsummer.models.position import DrawPosition
from azulsummer.models.position import TileIndex
from azulsummer.models.position import TilePosition
from azulsummer.models.tile_array import TileArray


def prepare_phase_one(action: PreparePhaseOne):
    """
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
        AssignCurrentPlayerToStartPlayer(game=action.game),
        ResetStartPlayerToken(game=action.game),
        PhaseOneComplete(game=action.game),
    ]
    for action_ in actions:
        action.game.enqueue_action(action_)


def phase_one_preparation_complete(action: PhaseOneComplete) -> None:
    """
    This is called at the end of prepare_phase_one to ensure all steps
    are completed before publishing the completion of the event

    Once phase one preparation is complete the game enters into the first turn.
    """
    action.game.enqueue_event(PhaseOnePrepared(game=action.game))
    action.game.enqueue_action(PlayPhaseOneTurn(game=action.game))


def prepare_phase_one_turn(action: PreparePhaseOneTurn):
    """
    - Advance to the next turn
    - Advance to the next player
    - increment turn
    - enqueue PlayPhaseOneTurn
    """
    all_phase.increment_turn(action.game)
    all_phase.increment_phase_turn(action.game)
    all_phase.advance_to_next_player(action.game)
    action.game.enqueue_action(PlayPhaseOneTurn(game=action.game))


def play_phase_one_turn(action: PlayPhaseOneTurn):
    """Play a phase one turn
    - Create the possible tile draws for the player
    - Have the player assess the tile draws
    - Transfer the tiles drawn to the player reserve, move the rest to the center
    - Resolve the turn
    """
    # TODO: Enqueue a "Begin Phase 1, Turn #, Phase turn #, player #" event
    action.game.enqueue_event(
        BeginningTurn(action.game, action.game.turn, action.game.phase_turn, action.game.current_player_index))
    draws = [
        *tiles.generate_acquire_tile_draws(
            tiles=action.game.tiles, wild_color=action.game.wild_tile
        )
    ]
    action.game.enqueue_event(PhaseOneDrawsGenerated(action.game, [*map(str, draws)]))

    draw_to_play = action.game.current_player.assess(
        AssessPhaseOneTileDrawAction(action.game, draws)
    )
    action.game.enqueue_event(
        PlayerSelectedTilesToAcquire(
            action.game, action.game.current_player_index, str(draw_to_play)
        )
    )

    handle_tile_acquisition(game=action.game, draw_position=draw_to_play)
    action.game.enqueue_action(ResolvePhaseOneTurn(action.game))


def resolve_phase_one_turn(action) -> None:
    if phase_one_end_criteria_are_met(action.game):
        action.game.enqueue_action(AdvancePhase(action.game))
        action.game.enqueue_action(PreparePhaseTwo(action.game))
    else:
        action.game.enqueue_action(PreparePhaseOneTurn(action.game))


def phase_one_end_criteria_are_met(game: Game) -> bool:
    """Verify if the criteria to end phase one have been met"""
    if game.phase_one_end_criteria_are_met():
        game.enqueue_event(PhaseOneEndCriteriaHaveBeenMet(game))
        return True


def handle_tile_acquisition(game: Game, draw_position: DrawPosition) -> None:
    """
    Handles the tile acquisition process for Phase One
    - Transfers the selected tile(s) to the player
    - Handle if the player is the first to draw from the center
    - Transfer tiles to the middle from the factory display
    - Enqueue turn resolution action
    """
    source = draw_position.as_tile_position()
    destination = TilePosition(
        location=TileTarget.PlayerReserve, nth=game.current_player_index
    )
    tiles.move_tiles(
        game=game, source=source, destination=destination, tiles=draw_position.tiles
    )

    if player_is_first_to_draw_from_table_center(
        game=game, draw_position=draw_position
    ):
        handle_first_draw_from_table_center(game=game, draw_position=draw_position)

    discard_from_factory_display_to_table_center(
        game=game, factory_display_n=draw_position.tiles_position
    )


def player_is_first_to_draw_from_table_center(
    game: Game, draw_position: DrawPosition
) -> bool:
    """
    Check if the current player is the first to draw from the table
    center in the current round.
    """
    if (
        draw_position.location is TileIndex.TableCenter
        and game.start_player_index is None
    ):
        game.enqueue_event(
            PlayerIsFirstToDrawFromTableCenter(game, game.current_player_index)
        )
        return True


def handle_first_draw_from_table_center(
    game: Game, draw_position: DrawPosition
) -> None:
    """
    The first player to draw from the table center in each round is set to
    be the start player in the next play_tile and acquire_tile phases.

    Drawing from the table center first reduces your score by the number of
    tiles drawn from the table center down to a minimum of 0 points.
    """
    set_starting_player(game, game.current_player_index)
    score.decrement_score(game, sum(draw_position.tiles))


def set_starting_player(game: Game, player_index: int) -> None:
    """
    Set the starting player for the subsequent play_tile and acquire_tile phases.
    """
    game.start_player_index = player_index
    game.enqueue_event(StartPlayerTokenWasSet(game=game, player=player_index))


def discard_from_factory_display_to_table_center(
    game: Game, factory_display_n: int
) -> None:
    """
    Un-drawn tiles in a factory display are discarded to the table center.
    """
    moved_tiles = TileArray(
        game.factory_display_tile_distribution(factory_display_n=factory_display_n)
    )
    game.discard_from_factory_display_to_center(factory_display_n)
    game.enqueue_event(
        DiscardTilesFromFactoryDisplayToTableCenter(
            game=game, factory_display=factory_display_n, tiles_moved=str(moved_tiles)
        )
    )


def fill_factory_displays(action: FillFactoryDisplays) -> None:
    """Fills all factory displays at start of Phase One"""
    for display in range(action.game.n_factory_displays):
        tiles.fill_factory_display(game=action.game, nth=display)
