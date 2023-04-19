import ply.lex as lex

# Identifier matching for reserved words
reserved = {
    'if': 'IF',
    'filter': 'FILTER',
    'asset': 'ASSET',
    'rebalance-threshold': 'REBALANCE',
}

# Required list of token names
tokens = (
    'WORD',
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
    'LBRACE',
    'RBRACE',
    'QUOTATION',
    'COLON',
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
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_QUOTATION = r'"'
t_COLON = r':'

# Regular expression for numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regular expression for word-like strings
def t_WORD(t):
    r'[a-zA-Z\-]+'
    t.type = reserved.get(t.value,'WORD')    # Check for reserved words
    return t

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
