# -*- coding: utf-8 -*-

from operator import itemgetter
import copy

class Builder(object):

    def __init__(self, name=None, parent=None, **kwargs):
        self._name = name
        self._parent = parent

    def _spawn(self, name):
        child = copy.copy(self)
        child._name = name
        child._parent = self
        return child

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError(name)
        return self._spawn(name)

    def __iter__(self):
        current = self
        while current:
            if current._name:
                yield current
            current = current._parent

    def _chain(self, *args):
        chain = self
        for arg in args:
            chain = chain._spawn(str(arg))
        return chain

    def __call__(self, *args):
        return self._chain(*args)

    def _re(self, *args):
        return ''.join(reversed(map(lambda i: i._name, self._chain(*args))))

    def __repr__(self):
        return str(self._re())

    def __str__(self):
        return str(self._re())

if __name__ == '__main__':
    builder = Builder()
    print str(builder.hello.world) == 'helloworld'
    print str(builder.hello('world')) == 'helloworld'
