# -*- coding: utf-8 -*-

class AMQPClientError(BaseException):
    pass

class InvalidArgumentValueError(AMQPClientError):
    pass

class UnsupportedCommandError(AMQPClientError):
    pass
