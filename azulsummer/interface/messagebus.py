from __future__ import annotations

import logging
from collections import deque
from typing import Type, Callable

from azulsummer.interface import unit_of_work
from azulsummer.models.action import Action
from azulsummer.models.events import Event

logger = logging.getLogger(__name__)

Message = Action | Event


class MessageBus:
    def __init__(
        self,
        uow: unit_of_work.AbstractUnitOfWork,
        event_handlers: dict[Type[Event], list[Callable]],
        action_handlers: dict[Type[Action], Callable],
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.action_handlers = action_handlers

    def handle(self, message: Message):
        self.queue = deque([message])
        while self.queue:
            message = self.queue.popleft()
            if isinstance(message, Event):
                self.handle_event(message)
            elif isinstance(message, Action):
                self.handle_action(message)
            else:
                raise Exception(f"{message} was not an Event or Action")

    def handle_event(self, event: Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug("handle event %s with handler %s", event, handler)
                handler(event)
                self.queue.extend(self.uow.collect_new_events())
            except Exception:
                logger.exception("Exception handle event %s", event)

    def handle_action(self, action: Action):
        logger.debug("handle action %s", action)
        try:
            handler = self.action_handlers[type(action)]
            handler(action)
            self.queue.extend(self.uow.collect_new_events())
        except Exception:
            logger.exception("Exception handling action %s", action)
            raise
