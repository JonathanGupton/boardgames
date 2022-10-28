"""Module containing the Action interface classes"""

import uuid
from dataclasses import dataclass
from typing import Optional

from azulsummer.models.enums import TileTarget
from azulsummer.models.game import Game
from azulsummer.models.position import BoardPosition
from azulsummer.models.position import DrawPosition
from azulsummer.models.tile_array import TileArray


class Action:
    pass


@dataclass()
class SetAllPlayersActive(Action):
    game: Game


@dataclass(slots=True)
class BoardPlacement(Action):
    game: Game
    board_position: BoardPosition
    tile_cost: TileArray

    def __str__(self):
        return f"{str(self.board_position.star.name)}-{self.board_position.tile_value} - {str(self.tile_cost)}"


@dataclass(slots=True)
class SelectTilePlacement(Action):
    game: Game
    available_actions: list[BoardPlacement]


@dataclass
class ResolvePhaseOneTurn(Action):
    game: Game


@dataclass
class PlayPhaseOneTurn(Action):
    game: Game


@dataclass
class PhaseTwoPreparationComplete(Action):
    game: Game


@dataclass
class PlayPhaseTwoTurn(Action):
    game: Game


@dataclass
class HandlePhaseOneTileDraw(Action):
    game: Game
    draw_position: DrawPosition


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
class AssessPhaseOneTileDrawAction(Action):
    game: Game
    available_actions: list[DrawPosition]


@dataclass
class AdvancePhase(Action):
    game: Game


@dataclass
class PreparePhaseTwo(Action):
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
class PhaseOnePreparationComplete(Action):
    game: Game


@dataclass
class PreparePhaseOne(Action):
    game: Game


@dataclass
class PreparePhaseOneTurn(Action):
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
