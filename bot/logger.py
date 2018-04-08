#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from bot.config import debug, logger_level
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler


log: logging.Logger = None


def log_format(x):

    return ['%({0:s})'.format(i) for i in x]


def init():
    """
    Call this once in the __main__.py
    """

    supported_keys = [
        'asctime',
        'created',
        'filename',
        'funcName',
        'levelname',
        'levelno',
        'lineno',
        'module',
        'msecs',
        'message',
        'name',
        'pathname',
        'process',
        'processName',
        'relativeCreated',
        'thread',
        'threadName'
    ]

    custom_format = ' '.join(log_format(supported_keys))

    formatter = jsonlogger.JsonFormatter(custom_format)

    handler = RotatingFileHandler('logs/bot.log', maxBytes=10000000, backupCount=1)

    handler.setFormatter(formatter)

    level = logging.INFO

    if logger_level == 'error':
        level = logging.ERROR

    if logger_level == 'warning':
        level = logging.WARNING

    if debug or logger_level == 'debug':
        level = logging.DEBUG

    handler.setLevel(level)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=level)

    global log
    log = logging.getLogger(__name__)

    log.addHandler(handler)

    log.debug('Logger Initialized')

    return log
