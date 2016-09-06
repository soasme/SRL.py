# -*- coding: utf-8 -*-

import lex
import yacc

# List of token names.
tokens = (
    # Symbols
    'LEFT_PARENTHESIS',
    'RIGHT_PARENTHESIS',
    'COMMA',
    'NUMBER',
    'CHARACTER',
    'STRING',

    # Keywords
    'K_LITERALLY',
    'K_ONE',
    'K_OF',
    'K_LETTER',
    'K_FROM',
    'K_TO',
    'K_UPPERCASE',
    'K_ANY',
    'K_NO',
    'K_DIGIT',
    'K_ANYTHING',
    'K_NEW',
    'K_LINE',
    'K_WHITESPACE',
    'K_TAB',
    'K_RAW',
    'K_EXACTLY',
    'K_TIMES',
    'K_BETWEEN',
    'K_AND',
    'K_OPTIONAL',
    'K_ONCE',
    'K_NEVER',
    'K_OR',
    'K_MORE',
    'K_AT',
    'K_LEAST',
    'K_AS',
    'K_UNTIL',
    'K_CAPTURE',
    'K_IF',
    'K_FOLLOWED',
    'K_BY',
    'K_ALREADY',
    'K_HAD',
    'K_CASE',
    'K_SENSITIVE',
    'K_MULTI',
    'K_ALL',
    'K_LAZY',
    'K_BEGIN',
    'K_STARTS',
    'K_WITH',
    'K_MUST',
    'K_END',
    'K_CHARACTER',

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
t_K_LITERALLY = r'literally'
t_K_ONE = r'one'
t_K_OF = r'of'
t_K_LETTER = r'letter'
t_K_FROM = r'from'
t_K_TO = r'to'
t_K_UPPERCASE = r'uppercase'
t_K_ANY = r'any'
t_K_NO = r'no'
t_K_DIGIT = r'digit'
t_K_ANYTHING = r'anything'
t_K_NEW = r'new'
t_K_LINE = r'line'
t_K_WHITESPACE = r'whitespace'
t_K_TAB = r'tab'
t_K_RAW = r'raw'
t_K_EXACTLY = r'exactly'
t_K_TIMES = r'times'
t_K_BETWEEN = r'between'
t_K_AND = r'and'
t_K_OPTIONAL = r'optional'
t_K_ONCE = r'once'
t_K_NEVER = r'never'
t_K_OR = r'or'
t_K_MORE = r'more'
t_K_AT = r'at'
t_K_LEAST = r'least'
t_K_AS = r'as'
t_K_UNTIL = r'until'
t_K_CAPTURE = r'capture'
t_K_IF = r'if'
t_K_FOLLOWED = r'followed'
t_K_BY = r'by'
t_K_ALREADY = r'already'
t_K_HAD = r'had'
t_K_CASE = r'case'
t_K_SENSITIVE = r'sensitive'
t_K_MULTI = r'multi'
t_K_ALL = r'all'
t_K_LAZY = r'lazy'
t_K_BEGIN = r'begin'
t_K_STARTS = r'starts'
t_K_WITH = r'with'
t_K_MUST = r'must'
t_K_END = r'end'
t_K_CHARACTER = r'character'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' ,\t'

t_CHARACTER = r'.'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def p_expression_literally(p):
    'expression : K_LITERALLY STRING'
    p[0] = p[0] or []
    p[0].append(('literally', (p[2][1:-1], )))

def p_expression_one_of(p):
    'expression : K_ONE K_OF STRING'
    p[0] = p[0] or []
    p[0].append(('oneOf', (p[3][1:-1], )))

def p_expression_letter(p):
    '''expression : K_LETTER
                  | K_LETTER K_FROM CHARACTER K_TO CHARACTER
    '''
    p[0] = p[0] or []
    if len(p) == 6:
        char_from = p[3]
        char_to = p[5]
    else:
        char_from = 'a'
        char_to = 'z'
    p[0].append(('letter', (char_from, char_to, ), ))

def p_expression_uppercase_letter(p):
    '''expression : K_UPPERCASE K_LETTER
                  | K_UPPERCASE K_LETTER K_FROM CHARACTER K_TO CHARACTER
    '''
    p[0] = p[0] or []
    if len(p) == 7:
        char_from = p[4]
        char_to = p[6]
    else:
        char_from = 'A'
        char_to = 'Z'
    p[0].append(('letter', (char_from, char_to, ), ))

def p_expression_any_character(p):
    'expression : K_ANY K_CHARACTER'
    p[0] = p[0] or []
    p[0].append(('anyCharacter', ()))

def p_expression_no_character(p):
    'expression : K_NO K_CHARACTER'
    p[0] = p[0] or []
    p[0].append(('noCharacter', ()))

def p_expression_digit(p):
    '''expression : K_DIGIT
                  | K_DIGIT K_FROM NUMBER K_TO NUMBER
    '''
    p[0] = p[0] or []
    if len(p) == 6:
        num_from = p[3]
        num_to= p[5]
    else:
        num_from = 0
        num_to = 9
    p[0].append(('digit', (num_from, num_to, ), ))

def p_expression_anything(p):
    'expression : K_ANYTHING'
    p[0] = p[0] or []
    p[0].append(('anything', ()))


def p_expression_new_line(p):
    'expression : K_NEW K_LINE'
    p[0] = p[0] or []
    p[0].append(('newLine', ()))

def p_expression_whitespace(p):
    '''expression : K_WHITESPACE
                  | K_NO K_WHITESPACE
    '''
    p[0] = p[0] or []
    if len(p) == 3:
        p[0].append(('noWhitespace', ()))
    else:
        p[0].append(('whitespace', ()))

def p_expression_tab(p):
    'expression : K_TAB'
    p[0] = p[0] or []
    p[0].append(('tab', ()))

def p_expression_raw(p):
    'expression : K_RAW STRING'
    p[0] = p[0] or []
    p[0].append(('raw', (p[2][1:-1], )))

def p_expression_exactly_x_times(p):
    'expression : expression K_EXACTLY NUMBER K_TIMES'
    p[0] = p[0] or []
    p[0] += p[1]
    p[0].append(('exactly', (p[3], )))

def p_expression_between_x_and_y_times(p):
    '''expression : expression K_BETWEEN NUMBER K_AND NUMBER K_TIMES
                  | expression K_BETWEEN NUMBER K_AND NUMBER
    '''
    p[0] = p[0] or []
    p[0] += p[1]
    p[0].append(('between', (p[3], p[5], )))


def parse(string):
    parser = yacc.yacc(debug=True)
    return parser.parse(string, lexer=lexer)
