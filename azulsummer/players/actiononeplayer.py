"""Module containing the ActionOnePlayer class.  This player always plays the
first action in the action list."""

from __future__ import annotations

from azulsummer.players.player import Player


class ActionOnePlayer(Player):
    """Player class that always plays the first available action."""

    def assess(self, action: "Action") -> "Action":
        return action.available_actions[0]
