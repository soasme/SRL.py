# -*- coding: utf-8 -*-

import re
import copy

class Builder(object):

    def __init__(self, regex=None, flags=0, group='%s'):
        self.regex = regex or []
        self.flags = flags or 0
        self.compiled = None
        self.group = group or '%s'

    def literally(self, char):
        if char in {'+', '\\'}:
            char = '\\' + char
        self.regex.append(r'(?:%s)' % char)
        return self

    def digit(self, start='0', end='9'):
        self.regex.append(r'[%s-%s]' % (start, end))
        return self

    number = digit

    def letter(self, start='a', end='z'):
        self.regex.append(r'[%s-%s]' % (start, end))
        return self

    def noCharacter(self):
        self.regex.append(r'\W')
        return self

    def uppercaseLetter(self):
        self.regex.append(r'[A-Z]')
        return self

    def anyCharacter(self):
        self.regex.append(r'\w')
        return self

    def anything(self):
        self.regex.append(r'.')
        return self

    def newLine(self):
        self.regex.append(r'\n')
        return self

    def whitespace(self):
        self.regex.append(r'\s')
        return self

    def noWhitespace(self):
        self.regex.append(r'\S')
        return self

    def tab(self):
        self.regex.append(r'\t')
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

    def neverOrMore(self):
        self.regex.append(r'*')
        return self

    def optional(self):
        self.regex.append(r'?')
        return self

    def firstMatch(self):
        self.regex.append(r'?')
        return self

    lazy = firstMatch

    def exactly(self, count):
        self.regex.append(r'{%d}' % count)
        return self

    def once(self):
        return self.exactly(1)

    def twice(self):
        return self.exactly(2)

    def atLeast(self, number):
        self.regex.append(r'{%d,}' % number)
        return self

    def addClosure(self, builder, conditions, exploder=''):
        if isinstance(conditions, basestring):
            subquery = builder.literally(conditions)
        elif callable(conditions):
            subquery = conditions(builder)
        else:
            subquery = builder.raw(conditions.get())

        self.regex.append(subquery.get(exploder))
        return self

    def capture(self, conditions, name=None):
        builder = Builder()
        if name:
            builder.group = '(?P<%s>%%s)' % name
        else:
            builder.group = '(%s)'
        return self.addClosure(builder, conditions)

    def anyOf(self, conditions):
        builder = Builder()
        builder.group = '(?:%s)'
        return self.addClosure(builder, conditions, r'|')

    eitherOf = anyOf

    def until(self, char):
        self.regex.append(r'(?:%s)' % char)
        return self

    def oneOf(self, chars):
        self.regex.append(r'[%s]' % chars)
        return self

    def ifFollowedBy(self, conditions):
        self.regex.append(r'(?%s)' % conditions)
        return self

    def ifNotFollowedBy(self, conditions):
        self.regex.append(r'(?!%s)' % conditions)
        return self

    def ifAlreadyHad(self, conditions):
        self.regex.append(r'(?<=%s)' % conditions)
        return self

    def ifNotAlreadyHad(self, conditions):
        self.regex.append(r'(?<!%s)' % conditions)
        return self

    def beginWith(self):
        self.regex.append(r'^') # FIXME: assert
        return self

    startWith = beginWith

    def mustEnd(self):
        self.regex.append(r'$')
        return self

    def caseInsensitive(self):
        self.flags = self.flags | re.IGNORECASE
        return self

    def multiLine(self):
        self.flags = self.flags | re.MULTILINE
        return self

    def allLazy(self):
        self.regex.append(r'?') # FIXME: assert
        return self

    def revertLast(self):
        self.regex.pop()
        return self

    def __and__(self, conditions):
        builder = Builder(group=self.group)
        return self.addClosure(builder, conditions)

    def get(self, implode=r''):
        return self.group % implode.join(self.regex)

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
        return bool(self.compiled.match(string, self.flags))

    def match(self, string):
        if not self.compiled:
            self.compile()
        return self.compiled.match(string, self.flags)

    def getMatches(self, string):
        if not self.compiled:
            self.compile()
        match = self.compiled.search(string)
        if match:
            return list(match.groups())

    def findall(self, string):
        if not self.compiled:
            self.compile()
        return self.compiled.findall(string, self.flags)

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
