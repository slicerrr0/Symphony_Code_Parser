from .node import Node

class Comparator(Node):
    '''
    Base class for encapsulating comparator terminals
    such as 'GTE', 'LTE', 'GT', and 'LT'.
    '''
    def __init__(self, comparator: str) -> None:
        '''
        Constructor method for `Comparator` class.

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