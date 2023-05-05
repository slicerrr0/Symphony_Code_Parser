from .node import Node
from .indicator import Indicator
from .select import Select
from .asset import Asset

class Filter(Node):
    '''
    Base class for encapsulating 'filter' terminals.
    '''
    def __init__(self, layer: int, indicator: Indicator, selector: Select, raw_weight: float, *tickers: Asset) -> None:
        '''
        Constructor method for `Filter` class.

        :param indicator: Instance of `Indicator`.

        :param selector: Instance of `Select`.

        :param tickers: Any number of instances of `BaseAsset`.
        '''
        super(Filter, self).__init__(layer)
        self.raw_weight = raw_weight
        
        self.indicator = indicator.getIndicator()
        self.period = indicator.getPeriod()

        self.amount = selector.getAmount()
        self.reverse = selector.getDirection()

        self.tickers = [ticker.getTicker() for ticker in tickers]
    def addTicker(self, ticker: str) -> None:
        '''
        Appends a new Ticker to `self.tickers`.
        '''
        self.tickers.append(ticker)