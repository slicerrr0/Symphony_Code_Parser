from .node import Node
from .group import Group

class Asset(Node):
    '''
    Base class for encapsulating 'asset' terminals.
    '''
    def __init__(self, ticker: str, layer: int, raw_weight: float, group=None) -> None:
        '''
        Constructor method for the `Asset` class.
        
        :param ticker: The ticker this asset terminal holds.

        :param layer: Numerical layer this asset node is located at
        within the hierarchical order of the Symphony.

        :param weight: Decimal weighting assigned to this asset if
        it is traded.

        :param group: The group that this asset node belongs to. Defaults
        to `None`.
        '''
        assert group is None or isinstance(group, Group)
        super(Asset, self).__init__(layer)
        self.ticker = ticker
        self.raw_weight = raw_weight
        self.group = group
    def __str__(self) -> str:
        return str(self.ticker)
    def getTicker(self) -> str:
        '''
        Returns the ticker associated with this instance.
        '''
        return self.ticker
    def getWeight(self) -> float:
        '''
        Returns the decimal point weighting associated
        with this asset node.
        '''
        return self.weight
    def getGroup(self) -> None|Group:
        '''
        Returns the group this asset node belongs to.
        The return type will either be `None` or an 
        instance of `BaseGroup`.
        '''
        return self.group