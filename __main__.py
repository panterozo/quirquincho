#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quirquincho Enables Chaucha Wallet
administration and operations.
"""
import importlib

import bot.config
import bot.logger
import bot.bot

from bot.events import SystemEvents

from envparse import env


def ready():
    bot.logger.log.info('Bot Initialized {0} {1}'.format(bot.config.name, bot.config.version))


if __name__ == '__main__':

    env.read_envfile()

    # Env Vars were loaded so we must reload config module
    importlib.reload(bot.config)

    bot.logger.init()

    events = SystemEvents.instance()
    events.on_ready += ready

    bot.bot.init()

    events.done()


