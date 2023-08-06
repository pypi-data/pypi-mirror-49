# -*- coding: utf-8 -*-

from lib.argument import StringArgument, BoolArgument
from lib.user_interface import UserInterface
from lib.handlers.base_handler import Handler

class QueueDeleteHandler(Handler):
    group = 'queue'
    name = 'delete'

    meta_arguments = (
        StringArgument('queue', 'queue name'),
        BoolArgument('if_unused', 'delete only if unused'),
        BoolArgument('if_empty', 'delete only if empty'),
    )

    def run(self):
        msg_count = self.channel.queue_delete(**self.parsed_arguments)
        UserInterface.output("{} messages deleted".format(msg_count))

class QueueDeclareHandler(Handler):
    group = "queue"
    name = "declare"

    meta_arguments = (
        StringArgument("queue", "queue name"),
        BoolArgument("passive", "is passive queue", default=True),
        BoolArgument("durable", "is durable queue"),
        BoolArgument("exclusive", "is exclusive queue"),
        BoolArgument("auto_delete", "the queue could be automatically deleted"),
    )

    def run(self):
        queue, msg_count, consumer_count = self.channel.queue_declare(**self.parsed_arguments)
        UserInterface.output("Queue: {}, msg_count: {}, consumer_count: {}".format(queue, msg_count, consumer_count))

class QueueBindHandler(Handler):
    group = 'queue'
    name = 'bind'

    meta_arguments = (
        StringArgument('queue', 'queue name'),
        StringArgument('exchange', 'The name of the exchange to bind to'),
        StringArgument('routing_key', 'message routing key'),
    )

    def run(self):
        self.channel.queue_bind(**self.parsed_arguments)

class QueueUnbindHandler(Handler):
    group = 'queue'
    name = 'unbind'

    meta_arguments = (
        StringArgument('queue', 'queue name'),
        StringArgument('exchange', 'The name of the exchange to bind to'),
        StringArgument('routing_key', 'message routing key'),
    )

    def run(self):
        self.channel.queue_unbind(**self.parsed_arguments)

class QueuePurgeHandler(Handler):
    group = 'queue'
    name = 'purge'

    meta_arguments = (
        StringArgument('queue', 'queue name'),
    )

    def run(self):
        self.channel.queue_purge(**self.parsed_arguments)