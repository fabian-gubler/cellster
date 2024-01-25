from parser.nodes import BaseNode
from typing import Union

# Python type hinting shenanigans
class Change:
    def __init__(self):
        pass

class NodeModification(Change):
    def __init__(self, original_node: BaseNode, new_node: BaseNode):
        self.original_node = original_node
        self.new_node = new_node

    def __repr__(self):
        return f"NodeModification(original_node={self.original_node}, new_node={self.new_node})"


class ChildAddition(Change):
    def __init__(self, parent_node: BaseNode, child_node: BaseNode):
        self.parent_node = parent_node
        self.child_node = child_node


class ChildDeletion(Change):
    def __init__(self, parent_node: BaseNode, child_node: BaseNode):
        self.parent_node = parent_node
        self.child_node = child_node


class RootAddition(Change):
    def __init__(
        self, parent_node: BaseNode, child_node: BaseNode, direction: Union[None, str]
    ):
        self.parent_node = parent_node
        self.child_node = child_node
        self.direction = direction


class RootDeletion(Change):
    def __init__(self, parent_node: BaseNode, child_node: BaseNode):
        self.parent_node = parent_node
        self.child_node = child_node


class RootNodeModification(Change):
    def __init__(self, original_root_node: BaseNode, new_root_node: BaseNode):
        self.original_root_node = original_root_node
        self.new_root_node = new_root_node


class StructuralChange(Change):
    def __init__(self, original_node: BaseNode, new_node: BaseNode):
        self.original_node = original_node
        self.new_node = new_node
