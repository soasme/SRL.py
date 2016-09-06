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
