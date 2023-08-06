# -*- coding: utf-8 -*-
from amqp import VERSION
from amqp.connection import Connection, Channel

from lib.banner import banner
from lib.error import UnsupportedCommandError, InvalidArgumentValueError
from lib.user_interface import UserInterface

class App(object):
    handlers = []

    @classmethod  # register single or multiple handlers to the application
    def register_handlers(cls, *handlers):
        cls.handlers = list(handlers)

    def __init__(self, host, userid, password, virtual_host):
        self.connection_meta = {}
        if host:
            self.connection_meta['host'] = host
        if userid:
            self.connection_meta['userid'] = userid
        if password:
            self.connection_meta['password'] = password
        if virtual_host:
            self.connection_meta['virtual_host'] = virtual_host

        self.terminated = False
        self.connection = None
        self.channel = None
        self.setup_conn()

    def setup_conn(self):
        self.connection = Connection(**self.connection_meta)
        self.channel = Channel(self.connection)

        # Since amqp v2.0, you should explicitly call Connection.connect() and Channel.open()
        if VERSION[0] >= 2:
            self.connection.connect()
            self.channel.open()


    @staticmethod
    def welcome():
        UserInterface.output(banner.lstrip() + "Connected to the channel.\n"
                             "Type `help` to see the help document.\n"
                             "Type `exit` or `Ctrl+C` whenever to exit this shell.")

    @staticmethod
    def help():
        for handler in App.handlers:
            command = handler.group + "." + handler.name
            for meta_argument in handler.meta_arguments:
                command += ' ' + str(meta_argument)
            UserInterface.output(command)

    def terminate(self):
        UserInterface.output("Oops! Please don't go... /(ㄒoㄒ)/~~")
        self.terminated = True

    def event_loop(self):
        self.terminated = False

        try:
            # event_loop starts a event loop to "read - parse - handle - output"
            while not self.terminated:
                cmd = UserInterface.read()
                try:
                    if len(cmd) == 0:
                        UserInterface.output("Nothing entered, please type any command")
                        continue

                    if cmd.split()[0] == "exit":
                        self.terminate()
                        continue

                    if cmd.split()[0] == "help":
                        App.help()
                        continue

                    self.dispatch(cmd)
                except UnsupportedCommandError:
                    UserInterface.output("Unsupported Command: {}".format(cmd))
                except InvalidArgumentValueError as e:
                    UserInterface.output(e.message)
        except KeyboardInterrupt:
            self.terminate()

    def dispatch(self, cmd):
        # dispatch forwards the cmd and its arguments to corresponding handler
        cmd, arguments = cmd.split()[0], cmd.split()[1:]
        for handler in App.handlers:
            if cmd == handler.group + "." + handler.name:
                return handler(channel=self.channel, arguments=arguments).perform()
        raise UnsupportedCommandError
