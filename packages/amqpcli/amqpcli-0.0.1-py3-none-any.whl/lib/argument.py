# -*- coding: utf-8 -*-
import six

from amqp.basic_message import Message

from lib.error import InvalidArgumentValueError

class Argument(object):
    default = None

    def __init__(self, name, desc, default=None):
        self.name = name
        self.desc = desc  # reserved design
        if default is not None:
            self.default = default
        else:
            self.default = self.__class__.default

    def __str__(self):
        return "{}:{}".format(self.name, self.default)

    def parse(self, value):
        raise NotImplementedError("Not implemented")


class BoolArgument(Argument):
    default = False

    def parse(self, value):
        if value.lower() == "true":
            return True

        if value.lower() == "false":
            return False
        raise InvalidArgumentValueError("Not recognized value {} for {}".format(value, self.name))

class LongArgument(Argument):
    default = 0

    def parse(self, value):
        if six.PY2:
            return long(float(value))
        else:
            return int(float(value))

class StringArgument(Argument):
    default = ""

    def parse(self, value):
        return value

    def __str__(self):
        return self.name

class MessageArgument(Argument):
    default = ""

    def parse(self, value):
        return Message(body=value)

    def __str__(self):
        return self.name
