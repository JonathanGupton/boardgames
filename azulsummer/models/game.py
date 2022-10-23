from __future__ import annotations

from collections import deque
from typing import Optional
from typing import Sequence
from uuid import uuid4

from azulsummer.models.random import RandomTileDraw
from azulsummer.models.state import State
from azulsummer.models.tile_array import TileArray
from azulsummer.players.player import Player


class Game:
    def __init__(
        self, game_id: str, players: Sequence[Optional[Player]], seed: Optional[int]
    ) -> None:
        """Initiate a game

        Args:
            players:  A sequence of class Player.  Player at index 0 will be
                the starting player.
            seed:  Optional int for the random seed
        """
        self.game_id = game_id
        self.players = players
        self.seed = seed
        self.random = RandomTileDraw(seed)
        self.action_history = []
        self.action_queue = deque()
        self.event_queue = deque()

        # state must be created with Game.make_state() after assigning players
        # to the game
        self.state = None

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    @classmethod
    def new(
        cls, players: Optional[Sequence[Player]] = None, seed: Optional[int] = None
    ):
        """Instantiate a game without player information"""
        players = players if players else []
        seed = seed if seed else None
        return cls(str(uuid4()), players, seed)

    def make_state(self):
        """Create the initial game state for the game"""
        self.state = State.new(len(self.players))

    def enqueue_action(self, action: "Action") -> None:
        self.action_queue.append(action)

    def enqueue_event(self, event: "Event") -> None:
        self.event_queue.append(event)

    @property
    def factory_display_tile_max(self):
        return self.state.tiles.factory_display_tile_max

    @property
    def bag_quantity(self) -> int:
        return self.state.tiles.get_bag_quantity()

    @property
    def bag_index(self):
        return self.state.tiles.bag_index

    @property
    def bag_tiles(self):
        return self.state.tiles.view_bag()

    @property
    def tower_index(self):
        return self.state.tiles.tower_index

    @property
    def tower_quantity(self):
        return self.state.tiles.get_tower_quantity()

    @property
    def tower_tiles(self):
        return self.state.tiles.view_tower()

    @property
    def table_center_index(self):
        return self.state.tiles.table_center_index

    @property
    def factory_display_index(self):
        return self.state.tiles.factory_display_index

    @property
    def player_board_row_count(self):
        return self.state.tiles.player_board_row_count

    @property
    def supply_index(self):
        return self.state.tiles.supply_index

    @property
    def player_board_index(self):
        return self.state.tiles.player_board_index

    @property
    def player_reserve_index(self):
        return self.state.tiles.player_reserve_index

    @property
    def phase(self):
        return self.state.phase

    @phase.setter
    def phase(self, value):
        self.state.phase = value

    @property
    def n_factory_displays(self):
        return self.state.tiles.n_factory_displays

    @property
    def supply_deficit(self):
        return self.state.tiles.supply_deficit

    def move_tiles(
        self, source_index: int, destination_index: int, tiles: TileArray
    ) -> None:
        self.state.tiles.move_tiles(
            source_index=source_index, destination_index=destination_index, tiles=tiles
        )

    @property
    def start_player_index(self):
        return self.state.start_player_index

    @start_player_index.setter
    def start_player_index(self, value: int):
        self.state.start_player_index = value

    @property
    def current_player_index(self):
        return self.state.current_player_index

    @current_player_index.setter
    def current_player_index(self, value: int):
        self.state.current_player_index = value

    @property
    def tiles(self):
        return self.state.tiles

    @property
    def wild_tile(self):
        return self.state.wild_tile

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def reduce_score(self, player_index: int, amount: int):
        self.state.score[player_index] -= amount

    @property
    def score(self):
        return self.state.score

    def discard_from_factory_display_to_center(self, factory_display: int) -> None:
        self.tiles.discard_from_factory_display_to_center(factory_display)

    def factory_display_tile_distribution(self, factory_display_n: int):
        return self.state.tiles.view_factory_display_n(
            factory_display_n=factory_display_n
        )

    @property
    def turn(self):
        return self.state.turn

    @turn.setter
    def turn(self, value):
        self.state.turn = value

    @property
    def phase_turn(self):
        return self.state.phase_turn

    @phase_turn.setter
    def phase_turn(self, value):
        self.state.phase_turn = value

    @property
    def n_players(self):
        return len(self.players)

    def phase_one_end_criteria_are_met(self) -> bool:
        return self.state.phase_one_end_criteria_are_met()
