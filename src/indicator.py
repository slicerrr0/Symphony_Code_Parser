from .node import Node

class Indicator(Node):
    '''
    Base class for encapsulating 'indicator` terminals.
    '''
    def __init__(self, indicator: str, layer: int, period=None) -> None:
        '''
        Constructor method for `Indicator` class.

        :param indicator: String representation of the indicator.

        :param period: Integer period of the indicator. Defaults to `None`.
        '''
        assert period is None or type(period) == int
        super(Indicator, self).__init__(layer)
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
