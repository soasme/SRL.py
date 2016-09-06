# -*- coding: utf-8 -*-

import lex
import yacc

# List of token names.

tokens = (
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS'
    'COMMA',
    'NUMBER',
    'STRING',
)

# Regular expression rules for tokens
t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_COMMA = r','

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_STRING = r'\"([^\\\n]|(\\.))*?\"'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces, comma and tabs)
t_ignore  = ' ,\t'

class IllegalCharacter(Exception): pass

# Error handling rule
def t_error(t):
    raise IllegalCharacter(t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
