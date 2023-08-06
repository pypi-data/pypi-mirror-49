# -*- coding: utf-8 -*-

import six

line_counter = 0

class UserInterface(object):
    @staticmethod  # return the user's input in string
    def read():
        global line_counter
        line_counter += 1
        tips = "[%d]:> " % line_counter
        if six.PY2:
            return raw_input(tips)
        else:
            return input(tips)

    @staticmethod  # print the result
    def output(result):
        print(result)
