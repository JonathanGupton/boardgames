from __future__ import annotations

from collections import deque
from typing import Sequence, Optional
from uuid import uuid4

from azulsummer.actions.action_base_class import Action
from azulsummer.models.model import Model
from azulsummer.states.state_mutator import StateMutator

from azulsummer.players.player import Player


class Game:
    """Class to interface actions between the state and the players."""

    def __init__(self, players: Sequence[Player], seed: Optional[int] = None) -> None:
        """Initiate a game

        Args:
            players:  A sequence of class Player.  Player at index 0 will be
                the starting player.
            seed:  Optional int for the random seed
        """
        self.id = str(uuid4())
        self.players = players
        self.model = Model()
        self.mutator = StateMutator()
        self.action_queue: deque[Action] = deque()
        self.complete_actions: deque[Action] = deque()
        self.action_log: deque[str] = deque()
        self.model_history: deque[Model] = deque()

        # TODO:  Add a random module somehow
        self.seed = seed

    def play(self) -> int:
        """Play the game.  Return the integer index of the winning player."""
        while self.action_queue:
            action = self.action_queue.popleft()
            action.execute()
            self.complete_actions.append(action)
            self.action_log.append(str(action))
            self.model_history.append(self.model.copy())
        return self.model.winner


# Ply - One turn taken by one of the players