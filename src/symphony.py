from .node import Node
from .group import Group
from .asset import Asset
from .conditional import Conditional
from .filter import Filter
from .weight import Weight


class Symphony:
    '''
    Base class for encapsulating Symphonies and their nodes.
    '''
    def __init__(self, name=None) -> None:
        self.name = name
        self.nodes = list()
        self.active_groups = set()
        self.completed_conditionals = list()
        self.branch_just_completed = False
        self.next_weight = None
        self.consecutive_asset_nodes = 1
    def setRebalanceThreshold(self, threshold: float) -> None:
        '''
        Sets the rebalance threshold for this Symphony.
        '''
        self.rebalance_threshold = threshold
    def setRebalanceFrequency(self, frequency: str) -> None:
        '''
        Sets the rebalance frequency for this Symphony.
        '''
        self.rebalance_frequency = frequency
    def addActiveGroup(self, group: Group) -> None:
        '''
        Adds an instance of `Group` to the container
        storing all currently active groups at this point
        in the parsing process.

        :param group: New active group.
        '''
        self.active_groups.add(group)
    def getActiveGroups(self) -> set[Group]:
        '''
        Returns all currently active groups at this point in
        the parsing process.
        '''
        return self.active_groups
    def updateActiveGroups(self, current_layer: int) -> None:
        '''
        Prunes all inactive groups from `self.active_groups`
        whose `layer` attribute is greater than the layer
        the parser is currently at (specified by `current_layer`).

        This process of determining which groups are active and which
        are not is inherently amnesiac since all descendant nodes of
        any singular node are processed serially and prior to the
        processing of a sibling node. Thus, if the parser backtracks
        to a shallower level within the Abstract Syntax Tree (AST), all
        members of that group will already have been processed and appropiately
        assigned and that particular group will be permanently pruned.
        
        This ensures that groups are processed to their fullest extent,
        with no members left behind, and that asset nodes located on
        different branches, but at an equivalent or deepler layer to a
        group, are not incorrectly assigned to that group. 
        '''
        self.active_groups = {group for group in self.active_groups if group.layer > current_layer}

    def addNode(self, node: Node) -> None:
        '''
        Adds parameter `node` to the internal attribute that
        stores all nodes that belong to this Symphony as a 
        linear series.
        '''
        if issubclass(self.getPreviousNode(), Asset) and issubclass(node, Asset):
            self.consecutive_asset_nodes += 1
        elif self.consecutive_asset_nodes != 1:
            for node in self.nodes[::-1]:
                if issubclass(node, Asset):
                    self.updateAssetNode(node)
                else:
                    break
            self.consecutive_asset_nodes = 1
        
        if self.getPreviousNode().layer > node.layer: # If layer decreases, update active groups 
            self.updateActiveGroups()
        if self.branch_just_completed: # Reset attribute
            self.branch_just_completed = False
        self.nodes.append(node)
        previous_node = self.getPreviousNode()
        # If we reach the terminal point of an else branch
        # on the Symphony tree, we mark that layer as "completed"
        if isinstance(node, (Asset, Filter)) and \
            isinstance(previous_node, Conditional) and \
            previous_node.is_else:
                self.completed_conditionals.append(node.layer)
                self.branch_just_completed = True

    def updateFilterNode(self, asset: Asset) -> None:
        '''
        Adds the ticker associated with parameter `asset` to the 
        `self.tickers` property of the previous node added to the
        Symphony, as long as it was an instance of `Filter`.
        '''
        previous_node = self.getPreviousNode()
        assert isinstance(previous_node, Filter)
        previous_node.addTicker(asset.getTicker())
    def updateAssetNode(self, node: Asset) -> None:
        '''
        Appropriately updates the raw weighting of the specified
        asset node according to how many consecutive asset nodes
        were grouped together.

        :param node: Asset node to be updated.
        '''
        assert issubclass(node, Asset)
        node.raw_weight /= self.consecutive_asset_nodes
    def getPreviousNode(self) -> Node:
        '''
        Returns the last object within the `self.nodes` property,
        which will be the last node to have been added to the 
        Symphony.
        '''
        return self.nodes[-1]
        
    def getNextLayer(self, next_node=Node) -> int:
        '''
        Returns the appropriate layer for the next node that
        is added to the Symphony through the `addNode` method.
        '''
        assert issubclass(next_node, Node)
        
        if self.branch_just_completed:
            next_layer = self.completed_conditionals[-1] - 1
            # Next layer should be equivalent to the shallowest completed layer - 1
            assert next_layer == sorted(self.completed_conditionals)[0] - 1
            return next_layer
        
        try:
            previous_node = self.getPreviousNode()
            if isinstance(previous_node, Conditional) or next_node is Conditional:
                return previous_node.getLayer() + 1
        except IndexError: # self.nodes is an empty list
            return 0
    def getNextWeight(self, layer: int) -> float:
        '''
        Returns the appropriate raw weighting for the next node
        that is added to the Symphony through the `addNode` method.

        :param layer: Layer of the "next" node that has yet to be added
        to the Symphony.
        '''
        previous_node = self.getPreviousNode()
        if issubclass(previous_node, Weight, Filter):
            return previous_node.raw_weight
        # Key error should not happen since we should always have our root weights to
        # fall back on (root weights defined at beginning of symphony) Also need to 
        # find a way to correctly process those root weights in case there are multiple
        # with unequal weights (like in failsafe)
        return Weight.getWeight(layer-1) 