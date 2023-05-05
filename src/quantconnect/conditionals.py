'''
Contains classes that represent the syntactic structure of conditional statements.
'''
from ..node import BaseConditional

class QuantConnectConditional(BaseConditional):
    '''
    Renders string representations of conditional statements
    for use in QuantConnect python algorithms.
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
        super().__init__(
            comparator, 
            lhs_ticker, 
            lhs_indicator, 
            lhs_period, 
            rhs_period, 
            rhs_ticker, 
            rhs_indicator, 
            rhs_value)
    def __str__(self) -> str:
        if self.rhs_value is None:
            return f"""
                elif {self._format_conditional_expression('L')} {self.comparator} {self._format_conditional_expression('R')}
            """
        return f"""
            elif {self._format_conditional_expression('L')} {self.comparator} {self.rhs_value}
        """
    def _format_conditional_expression(self, side: str) -> str:
        '''
        Private method for formatting the left or right hand side of a QuantConnect 
        style conditional statement according to whether or not the `self.lhs_indicator`
        property is the "Current Price".

        :param side: 'L' for left-hand-side and 'R' for right-hand-side.
        '''   
        # Validate parameter `side`
        try:
             side = side.upper()
        except ValueError:
             raise ValueError(f'''
                Parameter side must be either `"L"` or `"R"`.
                Function received {side} instead
             ''')
        if side != 'L' and side != 'R':
             raise ValueError(f'''
                Parameter `side` must be either `"L"` or `"R"`.
                Function received {side} instead
             ''')
        
        if side == 'L' and self.lhs_indicator == 'CP':
            return f"""
                self.Securities['{self.lhs_ticker}'].Close
            """
        elif side == 'R' and self.rhs_indicator == 'CP':
            return f"""
                self.Securities['{self.rhs_ticker}'].Close
            """
        elif side == 'R':
                return f"""
                    self.indicators['{self.rhs_ticker}']['{self.rhs_indicator}']['Period-{self.rhs_period}'].Current.Value
                """
        return f"""
            self.indicators['{self.lhs_ticker}']['{self.lhs_indicator}']['Period-{self.lhs_period}'].Current.Value
        """