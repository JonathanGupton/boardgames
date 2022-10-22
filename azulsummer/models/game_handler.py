import logging
from collections import deque
from typing import Optional

from azulsummer.models import actions
from azulsummer.models import events
from azulsummer.models import logic_handler
from azulsummer.models.game import Game

logger = logging.getLogger(__name__)

Message = actions.Action | events.Event


class GameHandler:
    def __init__(self, game: Optional[Game] = None) -> None:
        self.game: Optional[Game] = game
        self.action_queue = deque()
        self.event_queue = deque()
        self.action_handlers = logic_handler.ACTION_HANDLERS
        self.event_handlers = logic_handler.EVENT_HANDLERS

    def play(self):
        self.action_queue.append(actions.StartGame(game=self.game))
        while self.action_queue:
            action = self.action_queue.popleft()
            self.handle_action(action)
            self.transfer_actions()
            self.transfer_events()
            if self.event_queue:
                self.handle_events()

    def transfer_actions(self):
        """Transfer actions from game.action_queue to GameHandler.action_queue"""
        self.action_queue.extend(self.game.action_queue)
        self.game.action_queue.clear()

    def transfer_events(self):
        """Transfer events from game.event_queue to GameHandler.event_queue"""
        self.event_queue.extend(self.game.event_queue)
        self.game.event_queue.clear()

    def handle_action(self, action: actions.Action):
        logger.debug("handle action %s", action)
        try:
            handler = self.action_handlers[type(action)]
            handler(action)
        except Exception:
            logger.exception("Exception handling action %s", action)
            raise

    def handle_events(self):
        while self.event_queue:
            event = self.event_queue.popleft()
            logger.debug("handle event %s with handler %s", event)
            try:
                handler = self.event_handlers[type(event)]
                handler(event)
            except Exception:
                logger.exception("Exception handle event %s", event)
                raise
