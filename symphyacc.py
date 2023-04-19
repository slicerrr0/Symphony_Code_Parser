import ply.yacc as yacc

from .symphlex import tokens

# Grammar rules


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

