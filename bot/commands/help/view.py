#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implements messages returned as the result
of the command
"""
from telegram import Update
from bot.commands.base import View as BaseView

class View(BaseView):

    @classmethod
    def help_message(cls, context: Update):
        
        content = '''
Hola soy *Quirquincho* <')))~ :thumbs_up:

Estoy encargado de administrar tus direcciones de Chaucha.

Ésta es mi lista de comandos:

- /balance : Entrega el balance para tu chauchera
- /ayuda : Muestra *este* texto
        '''

        return cls(content, context)