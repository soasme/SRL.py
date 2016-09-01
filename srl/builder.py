# -*- coding: utf-8 -*-

import copy

class Builder(object):

    def __init__(self):
        self.regex = []

    def literally(self, char):
        if char in {'+', '\\'}:
            char = '\\' + char
        self.regex.append(r'%s' % char)
        return self

    def digit(self):
        self.regex.append(r'\d')
        return self

    number = digit

    def between(self, start, end):
        self.regex.append(r'{%d,%d}' % (start, end))
        return self

    def onceOrMore(self):
        self.regex.append(r'+')
        return self

    def mustEnd(self):
        self.regex.append(r'$')
        return self

    def get(self):
        return r''.join(self.regex)

