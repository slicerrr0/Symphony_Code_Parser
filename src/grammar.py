'''
Contains function-based grammar rules used to parse input text.
'''

### Grammar rules ###

# Identifies 'symphony' terminals
def p_symphony_expr(p):
    'symphony : LPAREN SYMPHONY'
    p[0] = p[2]

# Identifies 'group' terminals
def p_group_expr(p):
    'group : LPAREN GROUP'
    p[0] = p[2]

# Identifies 'weight specified' terminals
def p_weight_specified_expr(p):
    'weight_specified : LBRACKET LPAREN WEIGHT_SPECIFIED'
    p[0] = p[3]

# Identifies 'weight equal' terminals
def p_weight_equal_expr(p):
    'weight_equal : LBRACKET LPAREN WEIGHT_EQUAL'
    p[0] = p[3]

# Identifies 'rebalance' terminals
def p_rebal_expr(p):
    'rebal : LBRACE COLON REBALANCE'
    p[0] = p[3]

# Identifies 'filter' terminals
def p_filter_expr(p):
    'filter : LBRACKET LPAREN FILTER'
    p[0] = p[3]

# Identifies 'select bottom' terminals
def p_select_bottom_expr(p):
    'select_bottom : LBRACKET LPAREN SELECT_BOTTOM'
    p[0] = p[3]

# Identifies 'select top' terminals
def p_select_top_expr(p):
    'select_top : LBRACKET LPAREN SELECT_TOP'
    p[0] = 0[3]

# Identifies 'asset' terminals
def p_asset_expr(p):
    'asset : LBRACKET LPAREN ASSET'
    p[0] = p[3]

# Identifies 'if' terminals
def p_conditional_expr(p):
    'conditional : LBRACKET LPAREN IF'
    p[0] = p[3]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")