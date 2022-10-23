"""Module containing the State class"""
from __future__ import annotations

from typing import Optional

from azulsummer.models.board import Board
from azulsummer.models.bonus_spaces import BonusSpace
from azulsummer.models.enums import Phase
from azulsummer.models.score import Score
from azulsummer.models.tiles import Tiles


class State:
    """The State class manages the state for an Azul Summer Pavilion game.  All
    actions that affect the game state are applied via the State class's methods.
    """

    def __init__(
        self,
        n_players: int,
        tiles: Tiles,
        score: Score,
        boards: list[Board],
        bonus_spaces: list[BonusSpace],
        wild_tile: Optional[int],
        turn: int,
        phase: Optional[Phase],
        phase_turn: Optional[int],
        ply: Optional[int],
        game_round: Optional[int],
        start_player_index: Optional[int],
        current_player_index: Optional[int],
        winner: Optional[int],
    ) -> None:
        self.n_players = n_players
        self.tiles = tiles
        self.score = score
        self.boards = boards
        self.bonus_spaces = bonus_spaces
        self.wild_tile = wild_tile

        # Phase, order, turn values
        self.ply = ply
        self.turn = turn
        self.phase = phase
        self.phase_turn = phase_turn
        self.game_round = game_round
        self.start_player_index = start_player_index
        self.current_player_index = current_player_index

        self.winner = winner

    @classmethod
    def new(cls, n_players: int) -> State:
        tiles = Tiles.new(n_players)
        score = Score(n_players)
        board = [Board.new() for _ in range(n_players)]
        bonus_spaces = [BonusSpace() for _ in range(n_players)]
        wild_tile = None

        turn = 1
        phase = None
        phase_turn = 1
        ply = 0
        game_round = None
        start_player_index = None
        current_player_index = None
        winner = None
        return cls(
            n_players,
            tiles,
            score,
            board,
            bonus_spaces,
            wild_tile,
            turn,
            phase,
            phase_turn,
            ply,
            game_round,
            start_player_index,
            current_player_index,
            winner,
        )

    def phase_one_end_criteria_are_met(self) -> bool:
        """Check if the end phase 1 criteria are met.  Returns True if all
        criteria are met, otherwise returns False.

        The factory display and center of table must both be empty and
        the phase must be AcquireTile.
        """
        return all(
            [
                self.phase == Phase.acquire_tile,
                self.tiles.get_factory_displays_quantity() == 0,
                self.tiles.get_table_center_quantity() == 0,
            ]
        )

    def phase_two_end_criteria_are_met(self) -> bool:
        """Check if the end phase 2 criteria are met.  This occurs when all
        players have passed during Phase.PlayTiles.
        """
        pass

    def advance_round(self):
        """Increment the round.

        The State has a default round of -1, which is incremented as part of
        the game initialization process.  Each round from 0 to 5 (6 rounds
        total) is associated with a Wild Tile color.

        Returns:
            None
        """
        self.game_round += 1

    def increment_current_player(self):
        """Increment the player index by one and loop back to player 0 when
        the last player is reached.
        """
        self.current_player_index = (self.current_player_index + 1) % self.n_players

    def fill_supply(self):
        """Fill the supply with tiles."""
        self.tiles.fill_supply()

    def fill_factory_displays(self):
        """Fill the factory displays with tiles."""
        self.tiles.fill_factory_displays()

    def generate_actions(self):
        """Generate all available actions given the current state."""
        pass

    def assign_winner(self) -> None:
        """Assign the player index with the winning score to the winner property"""
        pass

    def get_current_player(self) -> int:
        """Get the current player.

        Returns:
            The integer index of the current player.
        """
        return self.current_player_index
