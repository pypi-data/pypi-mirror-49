# -*- coding: utf-8 -*-
from lib.argument import StringArgument, BoolArgument
from lib.handlers.base_handler import Handler

class ExchangeDeclareHandler(Handler):
    group = 'exchange'
    name = 'declare'

    meta_arguments = (
        StringArgument('exchange', 'the name of the exchange'),
        StringArgument('type', 'exchange type'),
        BoolArgument('passive', 'do not create exchange'),
        BoolArgument('durable', 'request a durable exchange'),
        BoolArgument('auto_delete', 'auto-delete when unused'),
    )

    def run(self):
        self.channel.exchange_declare(**self.parsed_arguments)

class ExchangeDeleteHandler(Handler):
    group = 'exchange'
    name = 'delete'

    meta_arguments = (
        StringArgument('exchange', 'the name of the exchange'),
        BoolArgument('if_unused', 'delete only if unused'),
    )

    def run(self):
        self.channel.exchange_delete(**self.parsed_arguments)