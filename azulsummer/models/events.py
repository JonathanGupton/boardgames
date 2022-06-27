"""Module containing the game events"""
from dataclasses import dataclass


class Event:
    pass


@dataclass
class AdvancedPhase(Event):
    game_id: str


@dataclass
class AdvancedCurrentPlayerIndex(Event):
    game_id: str


@dataclass
class AdvancedRound(Event):
    game_id: str


@dataclass
class AdvancedTurn(Event):
    game_id: str


@dataclass
class AdvancedWildTileIndex(Event):
    game_id: str


@dataclass
class AssignedStartPlayer(Event):
    game_id: str


@dataclass
class ScoredGame(Event):
    game_id: str


@dataclass
class IncrementedPlayerScore(Event):
    game_id: str


@dataclass
class DecrementedPlayerScore(Event):
    game_id: str


@dataclass
class LoadBagFromTower(Event):
    game_id: str


@dataclass
class LoadedTilesToCenter(Event):
    game_id: str


@dataclass
class LoadedTilesToFactoryDisplay(Event):
    game_id: str


@dataclass
class LoadedTilesToSupply(Event):
    game_id: str


@dataclass
class LoadedTilesToTower(Event):
    game_id: str


@dataclass
class UnAssignedStartPlayer(Event):
    game_id: str


@dataclass
class DrewFromFactoryDisplay(Event):
    game_id: str


@dataclass
class DrewFromSupply(Event):
    game_id: str


@dataclass
class DrewFromMiddle(Event):
    game_id: str


@dataclass
class PlayedTileToPlayerBoard(Event):
    game_id: str


@dataclass
class DiscardedExcessTiles(Event):
    game_id: str


@dataclass
class PassedTurn(Event):
    pass
