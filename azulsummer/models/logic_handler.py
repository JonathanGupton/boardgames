"""Contains the mapping for action/event messages and the associated function """
import pprint
from typing import Callable
from typing import Type

from azulsummer.models import actions
from azulsummer.models.actions import AdvancePhase
from azulsummer.models.actions import AdvanceRound
from azulsummer.models.actions import AdvanceWildTileIndex
from azulsummer.models.actions import AssignCurrentPlayerToStartPlayer
from azulsummer.models.actions import FillFactoryDisplays
from azulsummer.models.actions import FillSupply
from azulsummer.models.actions import InitializeGameState
from azulsummer.models.actions import PhaseOneComplete
from azulsummer.models.actions import PlayPhaseOneTurn
from azulsummer.models.actions import PreparePhaseOne
from azulsummer.models.actions import PreparePhaseOneTurn
from azulsummer.models.actions import PreparePhaseTwo
from azulsummer.models.actions import ResetPhaseTurn
from azulsummer.models.actions import ResetStartPlayerToken
from azulsummer.models.actions import ResolvePhaseOneTurn
from azulsummer.models.actions import StartGame
from azulsummer.models.events import AssignedStartPlayer
from azulsummer.models.events import BagLoadedWith132Tiles
from azulsummer.models.events import BeginningPhaseOnePreparation
from azulsummer.models.events import BeginningTurn
from azulsummer.models.events import CurrentPlayerIndexAdvanced
from azulsummer.models.events import CurrentPlayerSet
from azulsummer.models.events import DecrementedPlayerScore
from azulsummer.models.events import DiscardTilesFromFactoryDisplayToTableCenter
from azulsummer.models.events import GameCreatedWithNFactoryDisplays
from azulsummer.models.events import GameCreatedWithNPlayers
from azulsummer.models.events import GameStarted
from azulsummer.models.events import GameStateInitialized
from azulsummer.models.events import LoadedTilesToFactoryDisplay
from azulsummer.models.events import LoadedTilesToSupply
from azulsummer.models.events import PhaseAdvanced
from azulsummer.models.events import PhaseOneDrawsGenerated
from azulsummer.models.events import PhaseOneEndCriteriaHaveBeenMet
from azulsummer.models.events import PhaseOnePrepared
from azulsummer.models.events import PhaseTurnIncremented
from azulsummer.models.events import PhaseTurnSetToZero
from azulsummer.models.events import PlayerIsFirstToDrawFromTableCenter
from azulsummer.models.events import PlayerScoresInitializedAt5
from azulsummer.models.events import PlayerSelectedTilesToAcquire
from azulsummer.models.events import RefillBagFromTower
from azulsummer.models.events import RoundAdvanced
from azulsummer.models.events import StartPlayerTokenWasReset
from azulsummer.models.events import StartPlayerTokenWasSet
from azulsummer.models.events import StartTokenReset
from azulsummer.models.events import TileDrawGenerated
from azulsummer.models.events import TilesDrawnFromBag
from azulsummer.models.events import TilesMoved
from azulsummer.models.events import TurnIncremented
from azulsummer.models.events import WildTileIndexAdvanced
from azulsummer.models.logic import all_phase
from azulsummer.models.logic import game
from azulsummer.models.logic import phase_one
from azulsummer.models.logic import phase_two
from azulsummer.models.logic import tiles

GAME_HANDLERS: dict[Type[actions.Action], Callable] = {
    StartGame: game.start_game,
    InitializeGameState: game.initialize_game_state,
}

TILE_HANDLERS: dict[Type[actions.Action], Callable] = {
    FillSupply: tiles.fill_supply,
}

ALL_PHASE_HANDLERS: dict[Type[actions.Action], Callable] = {
    AdvancePhase: all_phase.advance_phase,
    AdvanceRound: all_phase.advance_round,
    AdvanceWildTileIndex: all_phase.advance_wild_tile_index,
    AssignCurrentPlayerToStartPlayer: all_phase.assign_current_player_to_start_player,
    ResetStartPlayerToken: all_phase.reset_start_player_index_value,
    ResetPhaseTurn: all_phase.reset_phase_turn,
}

PHASE_ONE_HANDLERS: dict[Type[actions.Action], Callable] = {
    FillFactoryDisplays: phase_one.fill_factory_displays,
    PreparePhaseOne: phase_one.prepare_phase_one,
    PreparePhaseOneTurn: phase_one.prepare_phase_one_turn,
    PhaseOneComplete: phase_one.phase_one_preparation_complete,
    PlayPhaseOneTurn: phase_one.play_phase_one_turn,
    ResolvePhaseOneTurn: phase_one.resolve_phase_one_turn,
}

PHASE_TWO_HANDLERS: dict[Type[actions.Action], Callable] = {
    PreparePhaseTwo: phase_two.prepare_phase_two,
}

PHASE_THREE_HANDLERS: dict[Type[actions.Action], Callable] = {}

SCORING_PHASE_HANDLERS: dict[Type[actions.Action], Callable] = {}

BOARD_HANDLERS: dict[Type[actions.Action], Callable] = {}

ACTION_HANDLERS: dict[Type[actions.Action], Callable] = {
    **GAME_HANDLERS,
    **TILE_HANDLERS,
    **ALL_PHASE_HANDLERS,
    **PHASE_ONE_HANDLERS,
    **PHASE_TWO_HANDLERS,
    **PHASE_THREE_HANDLERS,
    **SCORING_PHASE_HANDLERS,
    **BOARD_HANDLERS,
}


def DEFAULT_EVENT_HANDLER(args):
    pprint.pprint(args)


EVENT_HANDLERS = {
    GameStarted: DEFAULT_EVENT_HANDLER,
    GameStateInitialized: DEFAULT_EVENT_HANDLER,
    PlayerScoresInitializedAt5: DEFAULT_EVENT_HANDLER,
    PhaseAdvanced: DEFAULT_EVENT_HANDLER,
    RoundAdvanced: DEFAULT_EVENT_HANDLER,
    WildTileIndexAdvanced: DEFAULT_EVENT_HANDLER,
    PhaseTurnSetToZero: DEFAULT_EVENT_HANDLER,
    PhaseOnePrepared: DEFAULT_EVENT_HANDLER,
    LoadedTilesToSupply: DEFAULT_EVENT_HANDLER,
    LoadedTilesToFactoryDisplay: DEFAULT_EVENT_HANDLER,
    AssignedStartPlayer: DEFAULT_EVENT_HANDLER,
    StartTokenReset: DEFAULT_EVENT_HANDLER,
    BeginningPhaseOnePreparation: DEFAULT_EVENT_HANDLER,
    GameCreatedWithNPlayers: DEFAULT_EVENT_HANDLER,
    BagLoadedWith132Tiles: DEFAULT_EVENT_HANDLER,
    GameCreatedWithNFactoryDisplays: DEFAULT_EVENT_HANDLER,
    TileDrawGenerated: DEFAULT_EVENT_HANDLER,
    TilesMoved: DEFAULT_EVENT_HANDLER,
    RefillBagFromTower: DEFAULT_EVENT_HANDLER,
    TilesDrawnFromBag: DEFAULT_EVENT_HANDLER,
    CurrentPlayerSet: DEFAULT_EVENT_HANDLER,
    StartPlayerTokenWasReset: DEFAULT_EVENT_HANDLER,
    PhaseOneDrawsGenerated: DEFAULT_EVENT_HANDLER,
    PlayerSelectedTilesToAcquire: DEFAULT_EVENT_HANDLER,
    StartPlayerTokenWasSet: DEFAULT_EVENT_HANDLER,
    DecrementedPlayerScore: DEFAULT_EVENT_HANDLER,
    PlayerIsFirstToDrawFromTableCenter: DEFAULT_EVENT_HANDLER,
    DiscardTilesFromFactoryDisplayToTableCenter: DEFAULT_EVENT_HANDLER,
    TurnIncremented: DEFAULT_EVENT_HANDLER,
    PhaseTurnIncremented: DEFAULT_EVENT_HANDLER,
    CurrentPlayerIndexAdvanced: DEFAULT_EVENT_HANDLER,
    PhaseOneEndCriteriaHaveBeenMet: DEFAULT_EVENT_HANDLER,
    BeginningTurn: DEFAULT_EVENT_HANDLER,
}
