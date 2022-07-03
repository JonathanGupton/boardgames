"""Module containing the Action interface classes"""

import uuid

from dataclasses import dataclass


class Action:
    pass


@dataclass
class AdvancePhase(Action):
    game_id: uuid.UUID


@dataclass
class AdvanceCurrentPlayerIndex(Action):
    game_id: uuid.UUID


@dataclass
class AdvanceRound(Action):
    game_id: uuid.UUID


@dataclass
class AdvanceTurn(Action):
    game_id: uuid.UUID


@dataclass
class AdvanceWildTileIndex(Action):
    game_id: uuid.UUID


@dataclass
class AssignStartPlayer(Action):
    game_id: uuid.UUID
    player: uuid.UUID


@dataclass
class CreateGame(Action):
    pass


@dataclass
class AssignPlayer(Action):
    player: uuid.UUID


@dataclass
class ScoreGame(Action):
    game_id: uuid.UUID


@dataclass
class IncrementPlayerScore(Action):
    game_id: uuid.UUID
    player: uuid.UUID
    delta: int


@dataclass
class DecrementPlayerScore(Action):
    game_id: uuid.UUID
    player: uuid.UUID
    delta: int


@dataclass
class LoadBagFromTower(Action):
    game_id: uuid.UUID


@dataclass
class LoadTilesToCenter(Action):
    game_id: uuid.UUID


@dataclass
class LoadTilesToFactoryDisplay(Action):
    game_id: uuid.UUID


@dataclass
class LoadTilesToSupply(Action):
    game_id: uuid.UUID


@dataclass
class LoadTilesToTower(Action):
    game_id: uuid.UUID


@dataclass
class UnAssignStartPlayer(Action):
    game_id: uuid.UUID


@dataclass
class DrawFromFactoryDisplay(Action):
    game_id: uuid.UUID


@dataclass
class DrawFromSupply(Action):
    game_id: uuid.UUID


@dataclass
class DrawFromMiddle(Action):
    game_id: uuid.UUID


@dataclass
class PlayTileToPlayerBoard(Action):
    game_id: uuid.UUID


@dataclass
class DiscardExcessTiles(Action):
    game_id: uuid.UUID


@dataclass
class PassTurn(Action):
    game_id: uuid.UUID
    player: uuid.UUID
