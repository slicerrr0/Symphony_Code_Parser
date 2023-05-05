from .node import BaseNode

class Weight(BaseNode):
    '''
    Base class for encapsulating 'weight' terminals.
    '''
    # Class attribute
    all_weights = dict() # Maps if and else blocks by layer to weights

    # Static methods
    @staticmethod
    def getWeight(layer: int, relative=False) -> float:
        '''
        Returns the weighting at a specified layer in the
        hierarchical structure of the Symphony.

        :param layer: "Layer" within the Symphony to extract the weight from.

        :param relative: Return the "relative weight" at `layer`.
        '''
        # Return raw weight
        if not relative:
            return Weight.all_weights[layer]['raw_weight']
        # Return relative weight
        return Weight.all_weights[layer]['relative_weight']
    @staticmethod
    def determineRawWeight(layer: int, relative_weight: float) -> float:
        '''
        Returns the appropriate raw weighting for the next weight node
        to be added to the class attribute `Weight.all_weights`.

        :param layer: Layer of the "next" weight node that is yet to be
        added to `Weight.all_weights`.

        :param relative_weight: Relative weighting of the "next" weight node,
        as a percentage of the raw weighting of the previous weight node, expressed
        in decimal format.
        '''
        try:
            return Weight.all_weights[layer - 1]['raw_weight'] * relative_weight
        except KeyError: # No previous weight node exists
            return relative_weight
    
    # Class methods
    def __init__(self, layer: int, relative_weight: float, raw_weight: float) -> None:
        super(Weight, self).__init__(layer)
        self.relative_weight = relative_weight
        self.raw_weight = raw_weight
        self.addWeight()
    def addWeight(self) -> None:
        '''
        Updates `Weight.all_weights` with the raw weight
        and relative weight of this `Weight` instance.
        '''
        # Only the if condition has been completed at this layer 
        if len(Weight.all_weights.get(self.layer, False)) == 1:
            # Add "else" weight to this layer's value
            self.all_weights[self.layer] += {'relative_weight': self.relative_weight, 'raw_weight': self.raw_weight}
        else:
            # Either both the "if" and the "else" conditions have
            # been completed at this layer, or there does not yet
            # exist a key-value pair for this layer. In either 
            # circumstance, we perform the same operation (reset
            # the pair or create a new one, respectively.)
            self.all_weights[self.layer] = {'relative_weight': self.relative_weight, 'raw_weight': self.raw_weight}

class SpecifiedWeight(Weight):
    '''
    Represents weight nodes with specified weighting.
    '''
    pass


class EqualWeight(Weight):
    '''
    Represents weight nodes with equal weighting.
    '''
    pass