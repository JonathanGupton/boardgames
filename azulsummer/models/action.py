"""Module containing the Action interface classes"""
from dataclasses import dataclass


class Action:
    pass


@dataclass
class AdvancePhase(Action):
    game_id: str


@dataclass
class AdvanceCurrentPlayerIndex(Action):
    game_id: str


@dataclass
class AdvanceRound(Action):
    game_id: str


@dataclass
class AdvanceTurn(Action):
    game_id: str


@dataclass
class AdvanceWildTileIndex(Action):
    game_id: str


@dataclass
class AssignStartPlayer(Action):
    game_id: str
    player: str


@dataclass
class CreateGame(Action):
    players: list[str]


@dataclass
class ScoreGame(Action):
    game_id: str


@dataclass
class IncrementPlayerScore(Action):
    game_id: str
    player: str
    score: int


@dataclass
class DecrementPlayerScore(Action):
    game_id: str
    player: str
    score: int


@dataclass
class LoadBagFromTower(Action):
    game_id: str


@dataclass
class LoadTilesToCenter(Action):
    game_id: str


@dataclass
class LoadTilesToFactoryDisplay(Action):
    game_id: str


@dataclass
class LoadTilesToSupply(Action):
    game_id: str


@dataclass
class LoadTilesToTower(Action):
    game_id: str


@dataclass
class UnAssignStartPlayer(Action):
    game_id: str


@dataclass
class DrawFromFactoryDisplay(Action):
    game_id: str


@dataclass
class DrawFromSupply(Action):
    game_id: str


@dataclass
class DrawFromMiddle(Action):
    game_id: str


@dataclass
class PlayTileToPlayerBoard(Action):
    game_id: str


@dataclass
class DiscardExcessTiles(Action):
    game_id: str


@dataclass
class PassTurn(Action):
    pass
