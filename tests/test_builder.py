 # -*- coding: utf-8 -*-

import re
from srl.builder import Builder

def test_simple_phone_number_format():
    regex = Builder().literally('+').digit().between(1, 3) \
            .literally(' ').number().between(3, 4) \
            .literally('-').digit().onceOrMore() \
            .mustEnd().get()
    assert re.match(regex, '+49 123-45')
    assert re.match(regex, '+492 1235-45')
    assert not re.match(regex, '+49 123 45')
    assert not re.match(regex, '49 123-45')
    assert not re.match(regex, 'a+49 123-45')
    assert not re.match(regex, '+49 123-45b')

def test_simple_email_format():
    reg = Builder().anyOf(
        lambda q: q.digit().letter().oneOf('._%+-')
    ).onceOrMore().literally('@').eitherOf(
        lambda q: q.digit().letter().oneOf('.-')
    ).onceOrMore().literally('.').letter().atLeast(2) \
    .mustEnd().caseInsensitive()
    regex = reg.get()

    assert reg.is_valid()
    assert reg.is_matching('super-He4vy.add+ress@top-Le.ve1.domains')
    assert not reg.is_matching('sample.example.com')
    assert re.match(regex, 'sample@example.com')
    assert re.match(regex, 'super-He4vy.add+ress@top-Le.ve1.domains', reg.flags)
    assert not re.match(regex, 'sample.example.com')
    assert not re.match(regex, 'missing@tld')
    assert not re.match(regex, 'hav ing@spac.es')
    assert not re.match(regex, 'no@pe.123')
    assert not re.match(regex, 'invalid@email.com123')

def test_capture_group():
    raise NotImplementedError

def test_replace():
    query = Builder().capture(lambda q: q.anyCharacter().onceOrMore()) \
            .whitespace().capture(lambda q: q.digit().onceOrMore()) \
            .literally(', ').capture(lambda q: q.digit().onceOrMore()) \
            .caseInsensitive()
    assert query.replace(r'\1 1, \3', 'April 15, 2003') == 'April 1, 2003'

def test_filter():
    query = Builder().capture(lambda q: q.uppercaseLetter())
    assert query.filter(r'A:\g<0>', 'a1AB') == ('a1A:AA:B', 2)

def test_replace_callback():
    query = Builder().capture(lambda q: q.anyCharacter().onceOrMore()) \
            .whitespace().capture(lambda q: q.digit().onceOrMore()) \
            .literally(', ').capture(lambda q: q.digit().onceOrMore()) \
            .caseInsensitive()
    assert query.replace(lambda params: 'invoked', 'April 15, 2003') == 'invoked'

def test_laziness():
    regex = Builder().literally(',').twice().whitespace().optional().firstMatch()
    assert regex.split('sample,one,, two,,three') == ['sample,one', ' two', 'three']

def test_raw():
    assert Builder().literally('foo').raw('b[a-z]r').is_valid()

def test_parse():
    assert Builder.parse('literally "abc"').match('abc')
