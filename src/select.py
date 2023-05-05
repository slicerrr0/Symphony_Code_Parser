from .node import Node

    
class Select(Node):
    '''
    Base class for encapsulating 'select' terminals.
    '''
    def __init__(self, layer: int, amount: int, reverse=False) -> None:
        '''
        Constructor method for the `Select` class.

        :param amount: Number of tickers it selects.

        :param reverse: Directionality of the sorting.
        '''
        super(Select, self).__init__(layer)
        self.amount = amount
        self.reverse = reverse
    def getAmount(self) -> int:
        '''
        Returns the number of Tickers this select node chooses.
        '''
        return self.amount
    def getDirection(self) -> bool:
        '''
        Returns `True` if this select node sorts assets in reverse
        order.
        '''
        return self.reverse