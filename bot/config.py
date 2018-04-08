#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import environ
from sys import exit
from envparse import env

environment = env.str('BOT_ENV', default='').strip()

# Optional Keys

debug = env.bool('BOT_DEBUG_MODE', default=False)
logger_level = env.str('BOT_LOGGER_LEVEL', default='debug')

name = env.str('BOT_NAME', default='bot')
version = env.str('BOT_VERSION', default='0.0.0')

# Required Keys

if environment != '':
    try:
        environ['BOT_TELEGRAM_KEY']
        telegram_key = env.str('BOT_TELEGRAM_KEY', default='')
        if telegram_key.strip() == '':
            raise KeyError

    except KeyError:
        print('ERROR: BOT_TELEGRAM_KEY Must Exist')
        exit(-1)

