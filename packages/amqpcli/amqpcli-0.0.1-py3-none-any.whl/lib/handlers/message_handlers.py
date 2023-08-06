# -*- coding: utf-8 -*-
from lib.argument import StringArgument, BoolArgument, MessageArgument, LongArgument
from lib.user_interface import UserInterface
from lib.handlers.base_handler import Handler

class BasicPublishHandler(Handler):
    group = 'basic'
    name = 'publish'

    meta_arguments = (
        MessageArgument('msg', 'message'),
        StringArgument('exchange', 'Specifies the name of the exchange to publish to'),
        StringArgument('routing_key', 'Message routing key'),
        BoolArgument('mandatory', 'indicate mandatory routing'),
        BoolArgument('immediate', 'request immediate delivery'),
    )

    def run(self):
        self.channel.basic_publish(**self.parsed_arguments)

class BasicAckHandler(Handler):
    group = 'basic'
    name = 'ack'

    meta_arguments = (
        LongArgument('delivery_tag', 'server-assigned delivery tag'),
    )

    def run(self):
        self.channel.basic_ack(**self.parsed_arguments)

class BasicGetHandler(Handler):
    group = 'basic'
    name = 'get'

    meta_arguments = (
        StringArgument('queue', 'the name of the queue to directly access to'),
        BoolArgument('no_ack', 'no acknowledgment needed'),
    )

    def run(self):
        reply = self.channel.basic_get(**self.parsed_arguments)
        if reply:
            UserInterface.output(reply.body)
            UserInterface.output(reply.delivery_info)
        else:
            UserInterface.output("no msg.")
