import ply.yacc as yacc
from .lex import tokens

from src.asset import Asset
from src.comparator import Comparator
from src.conditional import Conditional, LeftConditional, RightConditional
from src.filter import Filter
from src.group import Group
from src.indicator import Indicator
from src.select import Select
from src.symphony import Symphony
from src.weight import EqualWeight, SpecifiedWeight, Weight



def isElseNode() -> bool:
    '''
    Determines if the next node that is to be added
    to the Symphony must be an 'else' node. This function
    should only be called when the yacc parser encounters 
    a conditional.
    '''
    current = previous_expr[-1]
    try:
        previous_node = current.getPreviousNode()
        if isinstance(previous_node, Conditional):
            return False
        return True
    except IndexError: # No nodes have been added to the Symphony yet
        return False
    
def constructLeftConditional(p):
    return LeftConditional(Asset(p[7]), Indicator(p[5], p[9]))

### Grammar rules ###

def p_expression_symphony(p):
    'expression : LPAREN SYMPHONY QUOTATION expression QUOTATION expression'
    p[0] = Symphony(p[4])
    for node in p[6]:
        p[0].addNode()

def p_expression_name(p):
    'expression : NAME'
    p[0] = p[1]





# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

example_code = r"""
(defsymphony
 "Copy of Simple S&P 500"
 {:rebalance-frequency :daily}
 (weight-equal
  [(if
    (>
     (moving-average-price "SPY" 21)
     (moving-average-price "SPY" 210))
    [(asset "QQQ")]
    [(weight-equal
      [(if
        (< (rsi "QQQ" 10) 30)
        [(asset "QQQ")]
        [(weight-equal
          [(if
            (> (current-price "SPY") (moving-average-price "SPY" 31))
            [(asset "QQQ")] 
            [(asset "SHY")])])])])])]))
"""

parser.parse(example_code)