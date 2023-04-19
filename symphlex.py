import ply.lex as lex

# Identifier matching for reserved words
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'filter': 'FILTER',
    'asset': 'ASSET',
}

# Required list of token names
tokens = (
    'NAME',
    'REBALANCE',
    'TICKER',
    'NUMBER',
    'GTE',
    'LTE',
    'GT',
    'LT',
    'INDICATOR',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'QUOTATION',
) + tuple(reserved.values())

# Regular expression rules for simple tokens
t_GTE = r'>='
t_LTE = r'<='
t_GT = r'>'
t_LT = r'<'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_QUOTATION = r'"'

# Regular expression for numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    return

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()