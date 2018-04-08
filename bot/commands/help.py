#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import Bot, Update, ParseMode
from telegram.ext import Dispatcher, CommandHandler
from emoji import emojize

from bot import logger
from bot.helpers import Chat
from bot.stickers import Quirquincho
from bot.events import BotEvents


class Messages(object):

    @staticmethod
    def help():
        response = '''
Hola soy *Quirquincho* <')))~ :thumbs_up:

Estoy encargado de administrar tus direcciones de Chaucha.

Ésta es mi lista de comandos:

- /balance : Entrega el balance para tu chauchera
- /ayuda : Muestra *este* texto
       
        '''

        return emojize(response)


class Command(object):

    @staticmethod
    def run(bot: Bot, update: Update):
        """
        Runs the command
        :param bot: Entregado por dispatcher
        :param update: Entregado por dispatcher
        :return:
        """

        BotEvents.instance().message_received(bot, update)

        if Chat.is_private(update):
            update.message.reply_text(Messages.help(), parse_mode=ParseMode.MARKDOWN)
            BotEvents.instance().reply(bot, update, Messages.help())
            bot.send_sticker(update.message.chat.id, Quirquincho.ok)

    @classmethod
    def init(cls, dispatcher: Dispatcher):
        """
        Inits the command
        :param dispatcher:
        :return:
        """
        dispatcher.add_handler(CommandHandler('help', cls.run))
        dispatcher.add_handler(CommandHandler('ayuda', cls.run))

        logger.log.debug('Help Command Initiated')

        return dispatcher
