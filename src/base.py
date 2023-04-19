'''
Contains the base implementation of classes used
throughout the parser.
'''

import re

class BaseNode:
    '''
    Base parent class from which all terminal-encapsulating
    classes inherit.
    '''
    def __str__(self) -> str:
        return
    def render(self) -> str:
        '''
        Public method for returning the formatted version of this syntax
        node.
        '''
        return self.__str__()

class BaseComparator(BaseNode):
    '''
    Base class for encapsulating comparator terminals
    such as 'GTE', 'LTE', 'GT', and 'LT'.
    '''
    def __init__(self, comparator: str) -> None:
        '''
        Constructor method for `BaseComparator` class.

        :param comparator: String representation of the comparator type.
        '''
        assert comparator in ('GTE', 'LTE', 'GT', 'LT')
        self.comparator = comparator
    def __str__(self) -> str:
        return f'<Comparator object: {self.comparator}>'
    def getComparator(self) -> str:
        '''
        Basic getter method for this instance's
        `self.comparator` property.
        '''
        return self.comparator

class BaseNumber(BaseNode):
    '''
    Base class for encapsulating 'integer' and 'float'
    terminals.
    '''
    def __init__(self, value: int|float) -> None:
        assert type(value) == int or type(value) == float
        self.value = value
    def __str__(self) -> str:
        return str(self.value)
    def getValue(self) -> int|float:
        '''
        Basic getter method for this instance's
        `self.value` property.
        '''
        return self.value
    
class BaseIndicator(BaseNode):
    '''
    Base class for encapsulating 'indicator` terminals.
    '''
    def __init__(self, indicator: str, period=None) -> None:
        '''
        Constructor method for `BaseIndicator` class.

        :param indicator: String representation of the indicator.

        :param period: Integer period of the indicator. Defaults to `None`.
        '''
        assert period is None or type(period) == int
        self.indicator = indicator
        self.period = period
    def __str__(self) -> str:
        if self.period is not None:
            return f'{self.period} day {self.indicator}'
        return f'{self.indicator}'
    def getIndicator(self) -> str:
        '''
        Basic getter method for this instance's
        `self.indicator` property.
        '''
        return self.indicator
    def getPeriod(self) -> int:
        '''
        Basic getter method for this instance's 
        `self.period` property.
        '''
        return self.period
    
class BaseAsset(BaseNode):
    '''
    Base class for encapsulating 'asset' terminals.
    '''
    def __init__(self, ticker: str) -> None:
        '''
        Constructor method for the `BaseAsset` class.
        
        :param ticker: The ticker this asset terminal holds.
        '''
        self.ticker = ticker
    def __str__(self) -> str:
        return str(self.ticker)
    def getTicker(self) -> str:
        '''
        Basic getter method for this instance's
        `self.ticker` property.
        '''
        return self.ticker
    
class BaseSelect(BaseNode):
    '''
    Base class for encapsulating 'select' terminals.
    '''
    def __init__(self, amount: int, reverse=False) -> None:
        '''
        Constructor method for the `BaseSelect` class.

        :param amount: Number of tickers it selects.

        :param reverse: Directionality of the sorting.
        '''
        self.amount = amount
        self.reverse = reverse
    def getAmount(self) -> int:
        '''
        Basic getter method for this instance's
        `self.amount property.
        '''
        return self.amount
    def getDirection(self) -> bool:
        '''
        Basic getter method for this instance's
        `self.reverse` property.
        '''
        return self.reverse
    
class BaseFilter(BaseNode):
    '''
    Base class for encapsulating 'filter' terminals.
    '''
    def __init__(self, indicator: BaseIndicator, selector: BaseSelect, *tickers: BaseAsset) -> None:
        '''
        Constructor method for `BaseFilter` class.

        :param indicator: Instance of `BaseIndicator`.

        :param selector: Instance of `BaseSelect`.

        :param tickers: Any number of instances of `BaseAsset`.
        '''
        self.indicator = indicator.getIndicator()
        self.period = indicator.getPeriod()

        self.amount = selector.getAmount()
        self.reverse = selector.getDirection()

        self.tickers = [ticker.getTicker() for ticker in tickers]

class BaseLeftConditional:
    '''
    Base class for representing the left-hand-side 
    portion of 'if' terminals.
    '''
    def __init__(self, ticker: BaseAsset, indicator: BaseIndicator) -> None:
        self.ticker = ticker
        self.indicator = indicator

class BaseRightConditional:
    '''
    Base class for representing the right-hand-side 
    portion of 'if' terminals.
    '''
    def __init__(self, value=None, ticker=None, indicator=None) -> None:
        assert value is None or type(value) == int
        self.value = value
        if self.value is None:
            assert type(ticker) == BaseAsset and type(indicator) == BaseIndicator
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
    

class BaseConditional(BaseNode):
    '''
    Base class for encapsulating 'if' terminals.
    '''
    def __init__(
            self, 
            comparator: BaseComparator, 
            lhs: BaseLeftConditional,
            rhs: BaseRightConditional
        ) -> None:
        self.comparator = comparator.getComparator()
        
        self.lhs_ticker = lhs.ticker.getTicker()
        self.lhs_indicator = lhs.indicator.getIndicator()
        self.lhs_period = lhs.indicator.getPeriod()
        
        self.rhs_value = rhs.getValue()
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
            if {self.lhs_period} {self.lhs_indicator} value of {self.lhs_ticker} is
            {self.comparator} {self.rhs_period} {self.rhs_indicator} value of {self.rhs_ticker}
            {self.rhs_value}
        ''')