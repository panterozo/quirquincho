#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from bot import logger
from telegram import Update


class Chat(object):

    @staticmethod
    def is_private(update: Update):
        """
        Tells if the message is private or not
        :param update: telegram bot update object
        :return: true if is private
        """
        if update.message.chat.type == 'private':
            return True
        else:
            logger.log.debug("Chat is not private")

        return False


class Message(object):

    @staticmethod
    def escape_markdown(text):

        """Helper function to escape telegram markup symbols"""
        escape_chars = '\*_`\['
        return re.sub(r'([%s])' % escape_chars, r'\\\1', text)
