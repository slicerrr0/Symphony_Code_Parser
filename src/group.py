from .node import Node

class Group(Node):
    '''
    Base class for encapsulating 'group' terminals.
    '''
    def __init__(self, name: str, layer: int) -> None:
        super(Group, self).__init__(layer)
        self.name = name
    def getName(self) -> str:
        '''
        Returns the name of this group.
        '''
        return self.name