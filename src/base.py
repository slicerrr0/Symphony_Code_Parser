'''
Contains the base implementation of classes used
throughout the parser.
'''

import re

class BaseConditionalStatement:
    '''
    Base class for rendering string representations
    of conditional statements.
    '''
    def __init__(
            self, 
            comparator: str, 
            lhs_ticker: str, 
            lhs_indicator: str, 
            lhs_period=None,
            rhs_period=None,
            rhs_ticker=None, 
            rhs_indicator=None, 
            rhs_value=None
        ) -> None:
        self.comparator = comparator
        self.lhs_ticker = lhs_ticker
        self.lhs_indicator = lhs_indicator
        self.lhs_period = lhs_period
        self.rhs_value = rhs_value
        
        # Validate constructor arguments
        self._validate_constructor_arguments(rhs_indicator, rhs_period, rhs_ticker)

        self.rhs_ticker = rhs_ticker
        self.rhs_indicator = rhs_indicator
        self.rhs_period = rhs_period

    def __str__(self) -> str:
        # Replace string representation of falsy boolean values with an empty string since
        # those properties are not used in the comparison of the left-hand-side and right-hand-side
        # of the conditional
        return re.sub('False|None', '', f'''
            if {self.lhs_period} {self.lhs_indicator} value of {self.lhs_ticker} is
            {self.comparator} {self.rhs_period} {self.rhs_indicator} value of {self.rhs_ticker}
            {self.rhs_value}
        ''')
    def _validate_constructor_arguments(self, *args):
        '''
        Private method for validating constructor arguments to ensure this class
        instance does not have an improper syntactic structure.

        Validation is achieved by first evaluating a boolean statement that checks
        if the identity of property `self.rhs_value` is `None`. 
        
        If this statement is evaluated as `True`, then all arguments in parameter
        `*args` must be falsy boolean values.

        Conversely, if this statement is evaluated as `False`, then all arguments
        in parameter `*args` must be truthy boolean values.
        '''
        if self.rhs_value is not None and any(*args):
            raise ValueError('''
                If constructor argument `rhs_value` is not set to `None`,
                arguments `rhs_period`, `rhs_ticker`, and 'rhs_indicator` must be None.
            ''')
        elif self.rhs_value is None and not all(*args):
            raise ValueError('''
                If constructor argument `rhs_value` is set to `None`,
                arguments `rhs_period`, `rhs_ticker`, and 'rhs_indicator` must not be None.
            ''')
    def render(self) -> str:
        '''
        Public method for returning the formatted version of
        this conditional statement as a string.
        '''
        return self.__str__()