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

from envparse import env


if __name__ == '__main__':

    env.read_envfile()

    # Env Vars were loaded so we must reload config module
    importlib.reload(bot.config)

    bot.logger.init()

    bot.logger.log.info('Bot Initialized {0} {1}'.format(bot.config.name, bot.config.version))

    bot.bot.init()


