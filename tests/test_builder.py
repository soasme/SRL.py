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
    assert Builder.parse('one of "abc"').match('a')
    assert Builder.parse('letter').match('a')
    assert Builder.parse('letter from a to c').match('b')
    assert not Builder.parse('letter from a to c').match('d')
    assert Builder.parse('uppercase letter').match('A')
    assert Builder.parse('letter from A to C').match('B')
    assert not Builder.parse('letter from A to C').match('D')
    assert Builder.parse('any character').match('a')
    assert Builder.parse('no character').match(' ')
    assert Builder.parse('digit').match('0')
    assert not Builder.parse('anything').match('\n')
    assert Builder.parse('anything').match('-')
    assert Builder.parse('new line').match('\n')
    assert Builder.parse('whitespace').match(' ')
    assert Builder.parse('no whitespace').match('a')
    assert Builder.parse('tab').match('\t')
    assert Builder.parse('raw "[a-zA-Z]"').match('a')
    assert not Builder.parse('raw "[a-z]"').match('A')
    assert Builder.parse('digit exactly 2 times').match('00')
    assert Builder.parse('digit exactly 2 times').match('000').group() == '00'
    assert not Builder.parse('digit between 2 and 3 times').match('1')
    assert Builder.parse('digit between 2 and 3 times').match('12')
    assert Builder.parse('digit between 2 and 3').match('12')
    assert Builder.parse('digit optional').match('a')
    assert not Builder.parse('digit once or more').match('a')
    assert Builder.parse('digit once or more').match('1')
    assert Builder.parse('digit once or more').match('12')
