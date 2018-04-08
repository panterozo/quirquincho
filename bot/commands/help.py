#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Dispatcher, CommandHandler
from telegram import Bot, Update, ParseMode
from bot import logger
from bot.helpers import Chat
from bot.stickers import Quirquincho
from emoji import emojize


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

        :param bot: Entregado por dispatcher
        :param update: Entregado por dispatcher
        :return:
        """
        if Chat.is_private(update):
            logger.log.debug('Received Message %s' % update.message.text)
            update.message.reply_text(Messages.help(), parse_mode=ParseMode.MARKDOWN)
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
