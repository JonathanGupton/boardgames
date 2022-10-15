"""Module containing the State class"""
from typing import Optional

from azulsummer.models.enums import Phase
from azulsummer.models.score import Score
from azulsummer.models.tiles import Tiles


class State:
    """The State class manages the state for an Azul Summer Pavilion game.  All
    actions that affect the game state are applied via the State class's methods.
    """

    def __init__(self, n_players: int, seed: Optional[int] = None) -> None:
        self.n_players = n_players
        self.tiles = Tiles(n_players, seed=seed)
        self.score = Score(n_players)

        # Phase, order, turn values
        self.turn: int = 0
        self.phase: Phase = Phase.acquire_tile
        self.round: Optional[int] = None
        self.start_player_index: Optional[int] = None
        self.current_player_index: Optional[int] = None

        self.winner = None

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
        self.round += 1

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
