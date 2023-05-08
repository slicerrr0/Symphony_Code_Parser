import ply.yacc as yacc
from lex import tokens

from src.asset import Asset
from src.comparator import Comparator
from src.conditional import Conditional, LeftConditional, RightConditional
from src.filter import Filter
from src.group import Group
from src.indicator import Indicator
from src.node import Node
from src.select import Select
from src.symphony import Symphony
from src.weight import Weight, EqualWeight, SpecifiedWeight


### Grammar rules ###

def p_expression_symphony(p):
    'expression : SYMPHONY_NAME expression'
    p[0] = Symphony(p[1])
    for node in p[2]:
        assert issubclass(node, Node)
        p[0].addNode()
        # addNode
        # if node is conditional, check if Symphony.isElseNode()

def p_expression_specified_weight(p):
    'expression : LPAREN WEIGHT_SPECIFIED PERCENT'
    p[0] = SpecifiedWeight(p[3])

def p_expression_equal_weight(p):
    'expression : LPAREN WEIGHT_EQUAL'
    p[0] = EqualWeight(1.0)

def p_expression_full_conditional(p):
    'expression : left_conditional right_conditional'
    assert type(p[1]) == tuple and type(p[2]) == RightConditional
    p[0] = Conditional(
        comparator=p[1][0],
        lhs=p[1][1],
        rhs=p[2]
    )

def p_expression_right_conditional(p):
    '''
    right_conditional : LPAREN expression RPAREN RPAREN
               | INTEGER RPAREN
    '''
    if p[2] != ')':
        assert type(p[2]) == tuple
    if p[1] != '(':
        value = None
        ticker = p[2][1]
        indicator = p[2][0]
    p[0] = RightConditional(value=value, ticker=ticker, indicator=indicator)

def p_expression_left_conditional(p):
    '''
    left_conditional : LPAREN comparator LPAREN expression RPAREN
    '''
    assert type(p[4]) == tuple
    assert type(p[2]) == Comparator
    p[0] = (p[2], LeftConditional(ticker=p[4][1], indicator=p[4][0]))

def p_expression_filter(p):
    '''
    expression : FILTER LPAREN expression INTEGER RPAREN LPAREN expression RPAREN
    '''
    assert len(p[3]) == 1 # indicator
    assert len(p[7]) == 2 # select (select plus period)
    p[0] = Filter(indicator=p[3], selector=p[7])

def p_expression_select(p):
    '''
    expression : SELECT_TOP INTEGER
               | SELECT_BOTTOM INTEGER
    '''
    if p[1] == 'select-top':
        p[0] = Select(p[2])
    else:
        p[0] = Select(p[2], reverse=True)

def p_expression_comparator(p):
    '''
    comparator : GTE
               | LTE
               | GT
               | LT
    '''
    if p[1] == 'GTE':
        p[0] = Comparator('GTE')
    elif p[1] == 'LTE':
        p[0] = Comparator('LTE')
    elif p[1] == 'GT':
        p[0] = Comparator('GT')
    else:
        p[0] = Comparator('LT')

def p_expression_indicator_dynamic(p):
    'expression : INDICATOR expression INTEGER'
    assert type(p[2]) == Asset
    p[0] = (Indicator(p[1], period=p[3]), Asset(p[2]))

def p_expression_indicator_fixed(p):
    'expression : INDICATOR'
    p[0] = Indicator(p[1])

def p_expression_ticker(p):
    'expression :  QUOTATION TICKER QUOTATION '
    p[0] = Asset(ticker=p[2])


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

parser = yacc.yacc()

parser.parse(example_code)