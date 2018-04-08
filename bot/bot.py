#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib

from bot import config
from bot import logger
from unipath import Path
from telegram.ext import Updater

commands = []


def error(bot, update, err):
    logger.log.warning('Update: "%s" - Error: "%s"' % (update, err))


def init():

    # Telegram Bot
    updater = Updater(config.telegram_key)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register Commands
    global commands

    disabled = []

    # Traverse commands directory
    # and append any command to the list like this
    # commands = ['help']

    files = Path('{0}/commands'.format(
        Path(__file__).absolute().ancestor(1)
    )).walk(pattern='*.py')

    for file in files:

        # Get the filename
        name = Path(file).components()[-1]

        # Remove extension
        command = name[:-3]

        if command != '__init__':
            if command not in disabled:
                commands.append(command)

    for command in commands:

        # Import the module
        module = importlib.import_module('bot.commands.%s' % command)

        # Get class and call init method
        cls = getattr(module, 'Command')
        cls().init(dispatcher)

    # Log all errors
    dispatcher.add_error_handler(error)

    logger.log.info("Started Listening Updates")
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

