#!/usr/bin/env python
# -*- coding: utf-8 -*-

from events import Events
from telegram import Bot, Update


class BaseEvent(Events):
    __singleton__ = None

    @classmethod
    def instance(cls):
        if cls.__singleton__ is None:
            cls.__singleton__ = cls()

        return cls.__singleton__


class SystemEvents(BaseEvent):
    __events__ = ('on_ready', 'on_done')

    def ready(self, **kwargs):
        self.on_ready(**kwargs)

    def done(self, **kwargs):
        self.on_done(**kwargs)


class BotEvents(BaseEvent):
    __events__ = ('on_message_received', 'on_reply')

    def message_received(self, bot: Bot, update: Update):
        self.on_message_received(bot, update)

    def reply(self,  bot: Bot, update: Update, message: str):
        self.on_reply(bot, update, message)
