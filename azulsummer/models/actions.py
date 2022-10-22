"""Module containing the Action interface classes"""

import uuid
from dataclasses import dataclass
from typing import Optional

from azulsummer.models.enums import TileTarget
from azulsummer.models.game import Game


class Action:
    pass


@dataclass
class PlayPhaseOneTurn(Action):
    game: Game


@dataclass
class DrawFromBag(Action):
    game: Game
    n_tiles_to_draw: int
    destination: TileTarget
    nth_position: Optional[int] = None


@dataclass
class StartGame(Action):
    game: Game


@dataclass
class InitializeGameState(Action):
    game: Game


@dataclass
class AdvancePhase(Action):
    game: Game


@dataclass
class AdvanceToNextPlayer(Action):
    game: Game


@dataclass
class AdvanceRound(Action):
    game: Game


@dataclass
class ResetPhaseTurn(Action):
    game: Game


@dataclass
class AdvanceTurn(Action):
    game: Game


@dataclass
class AdvanceWildTileIndex(Action):
    game: Game


@dataclass
class GenerateTileDraw(Action):
    game: Game
    tile_count: int


@dataclass
class AssignStartPlayer(Action):
    game: Game


@dataclass
class CreateGame(Action):
    pass


@dataclass
class PhaseOneComplete(Action):
    game: Game


@dataclass
class PreparePhaseOne(Action):
    game: Game


@dataclass
class RegisterPlayer(Action):
    game: uuid.UUID
    player: uuid.UUID


@dataclass
class ScoreGame(Action):
    game: Game


@dataclass
class IncrementPlayerScore(Action):
    game: Game
    player: uuid.UUID
    delta: int


@dataclass
class DecrementPlayerScore(Action):
    game: Game
    player: uuid.UUID
    delta: int


@dataclass
class LoadBagFromTower(Action):
    game: Game


@dataclass
class LoadTilesToCenter(Action):
    game: Game


@dataclass
class AssignCurrentPlayerToStartPlayer(Action):
    game: Game


@dataclass
class ResetStartPlayerToken(Action):
    game: Game


@dataclass
class FillFactoryDisplays(Action):
    game: Game


@dataclass
class FillSupply(Action):
    game: Game


@dataclass
class LoadTilesToTower(Action):
    game: Game


@dataclass
class ResetStartToken(Action):
    game: Game


@dataclass
class DrawFromFactoryDisplay(Action):
    game: Game


@dataclass
class DrawFromSupply(Action):
    game: Game


@dataclass
class DrawFromMiddle(Action):
    game: Game


@dataclass
class PlayTileToPlayerBoard(Action):
    game: Game


@dataclass
class DiscardExcessTiles(Action):
    game: Game


@dataclass
class PassTurn(Action):
    game: Game
    player: uuid.UUID
