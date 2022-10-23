"""Module containing the game events"""
from dataclasses import dataclass

from azulsummer.models.game import Game
from azulsummer.models.tile_array import TileArray


class Event:
    pass


@dataclass
class PhaseOneEndCriteriaHaveBeenMet(Event):
    game: Game


@dataclass
class BeginningTurn(Event):
    game: Game
    turn: int
    phase_turn: int
    current_player: int


@dataclass
class PlayerSelectedTilesToAcquire(Event):
    game: Game
    player: int
    tiles_drawn: str


@dataclass
class PhaseOneDrawsGenerated(Event):
    game: Game
    draws: list[str]


@dataclass
class CurrentPlayerSet(Event):
    game: Game
    player_index: int


@dataclass
class StartPlayerTokenWasReset(Event):
    game: Game


@dataclass
class StartPlayerTokenWasSet(Event):
    game: Game
    player: int


@dataclass
class TilesDrawnFromBag(Event):
    game: Game
    tiles: TileArray


@dataclass
class TilesMoved(Event):
    game: Game
    source: str
    destination: str
    tiles: str


@dataclass
class BeginningPhaseOnePreparation(Event):
    game: Game


@dataclass
class GameCreatedWithNPlayers(Event):
    game: Game
    n_players: int


@dataclass
class GameCreatedWithNFactoryDisplays(Event):
    game: Game
    n_factory_displays: int


@dataclass
class TileDrawGenerated(Event):
    game: Game
    tiles: str


@dataclass
class BagLoadedWith132Tiles(Event):
    game: Game


@dataclass
class StartTokenReset(Event):
    game: Game


@dataclass
class GameStateInitialized(Event):
    game: Game


@dataclass
class GameStarted(Event):
    game: Game


@dataclass
class PlayerScoresInitializedAt5(Event):
    game: Game


@dataclass
class PhaseOnePrepared(Event):
    game: Game


@dataclass
class PhaseAdvanced(Event):
    game: Game
    phase: str


@dataclass
class PhaseTurnSetToZero(Event):
    game: Game


@dataclass
class CurrentPlayerIndexAdvanced(Event):
    game: Game
    next_player: int


@dataclass
class RoundAdvanced(Event):
    game: Game
    round: int


@dataclass
class TurnIncremented(Event):
    game: Game


@dataclass
class PhaseTurnIncremented(Event):
    game: Game


@dataclass
class WildTileIndexAdvanced(Event):
    game: Game
    wild_tile: str


@dataclass
class PlayerIsFirstToDrawFromTableCenter(Event):
    game: Game
    player: int


@dataclass
class AssignedStartPlayer(Event):
    game: Game


@dataclass
class ScoredGame(Event):
    game: Game


@dataclass
class IncrementedPlayerScore(Event):
    game: Game


@dataclass
class DecrementedPlayerScore(Event):
    game: Game
    decreased_by: int
    original_score: int
    new_score: int


@dataclass
class DiscardTilesFromFactoryDisplayToTableCenter(Event):
    game: Game
    factory_display: int
    tiles_moved: str


@dataclass
class RefillBagFromTower(Event):
    game: Game
    tiles: TileArray


@dataclass
class LoadedTilesToCenter(Event):
    game: Game


@dataclass
class LoadedTilesToFactoryDisplay(Event):
    game: Game


@dataclass
class LoadedTilesToSupply(Event):
    game: Game


@dataclass
class LoadedTilesToTower(Event):
    game: Game


@dataclass
class UnAssignedStartPlayer(Event):
    game: Game


@dataclass
class DrewFromFactoryDisplay(Event):
    game: Game


@dataclass
class DrewFromSupply(Event):
    game: Game


@dataclass
class DrewFromMiddle(Event):
    game: Game


@dataclass
class PlayedTileToPlayerBoard(Event):
    game: Game


@dataclass
class DiscardedExcessTiles(Event):
    game: Game


@dataclass
class PassedTurn(Event):
    pass
