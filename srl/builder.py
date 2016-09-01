# -*- coding: utf-8 -*-

import re
import copy

class Builder(object):

    def __init__(self):
        self.regex = []
        self.flags = 0
        self.compiled = None

    def literally(self, char):
        if char in {'+', '\\'}:
            char = '\\' + char
        self.regex.append(r'%s' % char)
        return self

    def digit(self):
        self.regex.append(r'[0-9]')
        return self

    number = digit

    def letter(self):
        self.regex.append(r'[a-z]')
        return self

    def uppercaseLetter(self):
        self.regex.append(r'[A-Z]')
        return self

    def anyCharacter(self):
        self.regex.append(r'[a-zA-Z0-9_]')
        return self

    def whitespace(self):
        self.regex.append(r' ')
        return self

    def raw(self, string):
        self.regex.append(string)
        return self

    def between(self, start, end):
        self.regex.append(r'{%d,%d}' % (start, end))
        return self

    def onceOrMore(self):
        self.regex.append(r'+')
        return self

    def optional(self):
        self.regex.append(r'?')
        return self

    def firstMatch(self):
        self.regex.append(r'?')
        return self

    lazy = firstMatch

    def twice(self):
        self.regex.append(r'{2}')
        return self

    def atLeast(self, number):
        self.regex.append(r'{%d,}?' % number)
        return self

    def anyOf(self, conditions):
        builder = Builder()
        subquery = conditions(builder)
        regex = subquery.get(r'|')
        self.regex.append(r'(?:%s)' % regex)
        return self

    def capture(self, conditions):
        builder = Builder()
        subquery = conditions(builder)
        regex = subquery.get()
        self.regex.append(r'(%s)' % regex)
        return self

    eitherOf = anyOf

    def oneOf(self, chars):
        self.regex.append(r'[%s]' % chars)
        return self

    def mustEnd(self):
        self.regex.append(r'$')
        return self

    def caseInsensitive(self):
        self.flags = self.flags | re.IGNORECASE
        return self

    def get(self, implode=r''):
        return implode.join(self.regex)

    def compile(self):
        self.compiled = re.compile(self.get(), self.flags)
        return self

    def is_valid(self):
        try:
            self.compile()
            return True
        except re.error:
            return False

    def is_matching(self, string):
        if not self.compiled:
            self.compile()
        return self.compiled.match(string, self.flags)

    def split(self, string):
        if not self.compiled:
            self.compile()
        return self.compiled.split(string, self.flags)

    def sub(self, repl, string):
        if not self.compiled:
            self.compile()
        return self.compiled.sub(repl, string, self.flags)

    replace = sub

    def subn(self, repl, string):
        if not self.compiled:
            self.compile()
        return self.compiled.subn(repl, string, self.flags)

    filter = subn
