import ply.yacc as yacc
from symphlex import tokens
from src.asset import Asset
from src.comparator import Comparator
from src.conditional import Conditional, LeftConditional, RightConditional
from src.filter import Filter
from src.group import Group
from src.indicator import Indicator
from src.node import Node
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

previous_expr = list()

# Identifies 'symphony' terminals
def p_symphony_expr(p):
    'symphony : LPAREN SYMPHONY QUOTATION NAME QUOTATION'
    previous_expr.append(Symphony(p[4]))
    pass

# Identifies 'group' terminals
def p_group_expr(p):
    'group : LPAREN GROUP'
    pass

# Identifies 'weight specified' terminals
def p_weight_specified_expr(p):
    'weight_specified : LBRACKET LPAREN WEIGHT_SPECIFIED QUOTATION PERCENT QUOTATION'
    symphony = previous_expr[-1]
    
    layer = symphony.getNextLayer(SpecifiedWeight)
    raw_weight = Weight.determineRawWeight(layer, p[3])
    symphony.addNode(SpecifiedWeight(layer, p[3], raw_weight))
    pass

# Identifies 'weight equal' terminals
def p_weight_equal_expr(p):
    'weight_equal : LBRACKET LPAREN WEIGHT_EQUAL'
    symphony = previous_expr[-1]
    
    layer = symphony.getNextLayer(EqualWeight)
    raw_weight = Weight.determineRawWeight(layer, 1.0)
    symphony.addNode(EqualWeight(layer, 1.0, raw_weight))
    pass

# Identifies 'rebalance theshold' terminals
def p_rebal_threshold_expr(p):
    'rebal_threshold : COLON REBALANCE_THRESHOLD FLOAT'
    previous_expr[-1].setRebalanceThreshold(p[3])
    pass

# Identifies 'rebalance frequency' terminals
def p_rebal_frequency_expr(p):
    'rebal_frequency : COLON REBALANCE_FREQUENCY COLON NAME'
    previous_expr[-1].setRebalanceFrequency(p[4])
    pass

# Identifies 'select bottom' terminals
def p_select_bottom_expr(p):
    '''
    select_bottom : LPAREN FILTER LPAREN INDICATOR INTEGER RPAREN \
    LPAREN SELECT_BOTTOM INTEGER RPAREN
    '''
    symphony = previous_expr[-1]
    layer = symphony.getNextLayer(Filter)
    symphony.addNode(
        Filter(
            layer, 
            Indicator(p[4], layer, p[5]), 
            Select(p[9], layer, True)
        )
    )
    pass

# Identifies 'select top' terminals
def p_select_top_expr(p):
    '''
    select_top : LPAREN FILTER LPAREN INDICATOR INTEGER RPAREN \
    LPAREN SELECT_TOP INTEGER RPAREN
    '''
    symphony = previous_expr[-1]
    layer = symphony.getNextLayer(Filter)
    symphony.addNode(
        Filter(
            layer,
            Indicator(p[4], layer, p[5]),
            Select(p[9], layer)
        )
    )
    pass

# Identifies 'asset' terminals
def p_asset_expr(p):
    'asset : LPAREN ASSET QUOTATION TICKER QUOTATION RPAREN'
    symphony = previous_expr[-1]
    layer = symphony.getNextLayer(Asset)
    asset = Asset(p[4], layer)
    if not isinstance(symphony.getPreviousNode(), Filter):
        symphony.addNode(asset)
    else:
        symphony.updateFilterNode(asset)
    pass

# Identifies conditionals that do not use the current-price indicator
def p_conditional_dynamic_indicator_expr(p):
    '''
    conditional_dynamic : LPAREN IF COMPARATOR LPAREN INDICATOR QUOTATION \
    TICKER QUOTATION INTEGER RPAREN LPAREN INDICATOR QUOTATION TICKER QUOTATION \
    INTEGER RPAREN
    '''
    symphony = previous_expr[-1]
    layer = symphony.getNextLayer(Conditional)
    comparator = Comparator(p[3])
    lhs = constructLeftConditional(p=p)
    rhs = RightConditional(ticker=Asset(p[14]), indicator=Indicator(p[12], p[16]))
    if isElseNode():
        symphony.addNode(Conditional(layer=layer, comparator=comparator, lhs=lhs, rhs=rhs, is_else=True))
    else:
        symphony.addNode(Conditional(layer=layer, comparator=comparator, lhs=lhs, rhs=rhs))
    pass

def p_conditional_fixed_indicator_expr(p):
    '''
    conditional_fixed : LPAREN IF COMPARATOR LPAREN INDICATOR QUOTATION \
    TICKER QUOTATION INTEGER RPAREN INTEGER
    '''
    symphony = previous_expr[-1]
    layer = symphony.getNextLayer(Conditional)
    comparator = Comparator(p[3])
    lhs = constructLeftConditional(p=p)
    rhs = RightConditional(value=p[11])
    if isElseNode():
        symphony.addNode(Conditional(layer=layer, comparator=comparator, lhs=lhs, rhs=rhs, is_else=True))
    else:
        symphony.addNode(Conditional(layer=layer, comparator=comparator, lhs=lhs, rhs=rhs))
    pass


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