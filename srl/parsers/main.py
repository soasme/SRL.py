# -*- coding: utf-8 -*-

import lex
import yacc

# List of token names.

tokens = (
    'SINGLE_QUOTE',
    'DOUBLE_QUOTE',
    'WHITESPACE',
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS'
    'COMMA',
    'NUMBER',
)

# Regular expression rules for tokens

t_SINGLE_QUOTE = r"'"
t_DOUBLE_QUOTE = r'"'
t_WHITESPACE = r' '
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_COMMA = r','

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

class IllegalCharacter(Exception): pass

# Error handling rule
def t_error(t):
    raise IllegalCharacter(t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
