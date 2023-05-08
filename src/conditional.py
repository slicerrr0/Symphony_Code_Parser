
import re
from .node import Node
from .asset import Asset
from .indicator import Indicator
from .comparator import Comparator

class LeftConditional:
    '''
    Base class for representing the left-hand-side 
    portion of 'if' terminals.
    '''
    def __init__(self, ticker: Asset, indicator: Indicator) -> None:
        self.ticker = ticker
        self.indicator = indicator

class RightConditional:
    '''
    Base class for representing the right-hand-side 
    portion of 'if' terminals.
    '''
    def __init__(self, value=None, ticker=None, indicator=None) -> None:
        assert value is None or type(value) == int
        self.value = value
        if self.value is None:
            assert type(ticker) == Asset and type(indicator) == Indicator
            self.ticker = ticker
            self.indicator = indicator
    def isFixed(self) -> bool:
        '''
        Returns `True` if this instance represents
        a fixed-side condition with no ticker 
        or indicator properties.
        '''
        return self.value is not None
    def getValue(self) -> None|int:
        '''
        Basic getter method for this instance's
        `self.value` property.
        '''
        return self.value
    

class Conditional(Node):
    '''
    Base class for encapsulating 'if' terminals.
    '''
    def __init__(
            self, 
            comparator: Comparator, 
            lhs: LeftConditional,
            rhs: RightConditional,
            layer=None,
            is_else=False
        ) -> None:
        super(Conditional, self).__init__(layer)
        self.comparator = comparator.getComparator()
        
        self.lhs_ticker = lhs.ticker.getTicker()
        self.lhs_indicator = lhs.indicator.getIndicator()
        self.lhs_period = lhs.indicator.getPeriod()
        
        self.rhs_value = rhs.getValue()
        self.is_else = is_else
        if not rhs.isFixed():
            self.rhs_ticker = rhs.ticker.getTicker()
            self.rhs_indicator = rhs.indicator.getIndicator()
            self.rhs_period = rhs.indicator.getPeriod()
        else:
            self.rhs_ticker = None
            self.rhs_indicator = None
            self.rhs_period = None
    def __str__(self) -> str:
        # Replace string representation of falsy boolean values with an empty string since
        # those properties are not used in the comparison of the left-hand-side and right-hand-side
        # of the conditional
        return re.sub('False|None', '', f'''
            if {self.lhs_period} {self.lhs_indicator} value of {self.lhs_ticker} is \
            {self.comparator} {self.rhs_period} {self.rhs_indicator} value of {self.rhs_ticker} \
            {self.rhs_value}
        ''')