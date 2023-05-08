'''
Contains the base implementation of classes used
to represent expressions in an Abstract Syntax Tree.
'''

class Node:
    '''
    Base parent class from which all terminal-encapsulating
    classes inherit.
    '''
    def __init__(self, layer: int) -> None:
        self.layer = layer
    def __str__(self) -> str:
        raise NotImplementedError
    def getLayer(self) -> int:
        '''
        Returns the layer that this node is situated at within
        the hierarchical order of its Symphony.
        '''
        return self.layer
    def render(self) -> str:
        '''
        Public method for returning the formatted version of this syntax
        node.
        '''
        return self.__str__()