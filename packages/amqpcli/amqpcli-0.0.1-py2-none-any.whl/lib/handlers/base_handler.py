# -*- coding: utf-8 -*-
from lib.user_interface import UserInterface

class Handler(object):
    group = None
    name = None
    meta_arguments = tuple()

    def __init__(self, channel, arguments):
        self.channel = channel
        self.parsed_arguments = {}
        self.parse_arguments(arguments)

    def parse_arguments(self, arguments):
        if len(arguments) == 0:
            return

        index = 0
        for meta_argument in self.meta_arguments:
            if index >= len(arguments):
                self.parsed_arguments[meta_argument.name] = meta_argument.default
            else:
                self.parsed_arguments[meta_argument.name] = meta_argument.parse(arguments[index])
            index += 1

    def perform(self):
        try:
            self.run()
            UserInterface.output('done.')
        except BaseException as e:
            UserInterface.output(e.message)

    def run(self):
        raise NotImplementedError
