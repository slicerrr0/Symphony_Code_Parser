import ply.lex as lex

# Identifier matching for reserved words
reserved = {
    'if': 'IF',
    'filter': 'FILTER',
    'select-top': 'SELECT_TOP',
    'select-bottom': 'SELECT_BOTTOM',
    'asset': 'ASSET',
    'rebalance-threshold': 'REBALANCE',
    'weight-equal': 'WEIGHT_EQUAL',
    'weight-specified': 'WEIGHT_SPECIFIED',
    'group': 'GROUP',
    'defsymphony': 'SYMPHONY',
}

# Required list of token names
tokens = (
    'INDICATOR',
    'TICKER',
    'INTEGER',
    'FLOAT',
    'GTE',
    'LTE',
    'GT',
    'LT',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'QUOTATION',
    'COLON',
    'SPACE',
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
t_SPACE = r' '



# Regular expression for integers
def t_INTEGER(t):
    r'\d+|"\d+"'
    # try and except block is used to catch the specific integer 
    # period for filter statements, which are enclosed in double quotes
    try:
        t.value = int(t.value)
    except ValueError:
        t.value = int(t.value[1:len(t.value)-1])
    return t

# Regular expression for floats
def t_FLOAT(t):
    r'[0-9.]+'
    t.value = float(t.value)
    return t

# Regular expression for indicator strings
def t_INDICATOR(t):
    r'[a-z\-]+'
    t.type = reserved.get(t.value,'INDICATOR')  # Check for reserved words
    return t

# Regular expression for ticker strings
def t_TICKER(t):
    r'[A-Z]+'
    t.type = reserved.get(t.value, 'TICKER')    # Check for reserved words
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (tabs)
t_ignore  = '\t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
(defsymphony
 "Copy of Holy Grail simplified"
 {:rebalance-threshold 0.03}
 (weight-equal
  [(if
    (> (current-price "TQQQ") (moving-average-price "TQQQ" 200))
    [(weight-equal
      [(if (> (rsi "QQQ" 10) 80) [(asset "UVXY")] [(asset "TQQQ")])])]
    [(weight-equal
      [(if
        (< (rsi "TQQQ" 10) 31)
        [(asset "TECL")]
        [(weight-equal
          [(if
            (< (rsi "UPRO" 10) 31)
            [(asset "UPRO")]
            [(weight-equal
              [(if
                (>
                 (current-price "TQQQ")
                 (moving-average-price "TQQQ" 20))
                [(asset "TQQQ")]
                [(weight-equal
                  [(filter
                    (rsi "10")
                    (select-top 1)
                    [(asset "TLT") (asset "SQQQ")])])])])])])])])])]))
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)