#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib

from bot import config
from bot import logger
from bot.events import BotEvents, SystemEvents

from unipath import Path
from telegram import Bot, Update
from telegram.ext import Updater

commands = []


def on_message_received(bot: Bot, update:Update):
    logger.log.debug('Message Received %s' % update.message.text)


def on_reply(bot: Bot, update:Update, message):
    logger.log.debug('Bot sent reply %s' % message)


def error(bot:Bot, update:Update, err):
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

    # TODO: Implement autoloading
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
        module = importlib.import_module('bot.commands.%s.controller' % command)

        # Get class and call init method
        cls = getattr(module, 'Controller')
        cls().init(dispatcher)

    # Log all errors
    dispatcher.add_error_handler(error)

    logger.log.info("Started Listening Updates")

    bot_events = BotEvents.instance()
    bot_events.on_message_received += on_message_received
    bot_events.on_reply += on_reply

    events = SystemEvents.instance()
    events.ready()

    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

