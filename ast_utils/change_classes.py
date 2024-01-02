from typing import TypeVar, Union
from parser.nodes import BaseNode


class NodeModification:
    def __init__(self, original_node: BaseNode, new_node: BaseNode):
        self.original_node = original_node
        self.new_node = new_node


class ChildAddition:
    def __init__(self, parent_node: BaseNode, child_node: BaseNode):
        self.parent_node = parent_node
        self.child_node = child_node


class ChildDeletion:
    def __init__(self, parent_node: BaseNode, child_node: BaseNode):
        self.parent_node = parent_node
        self.child_node = child_node


class RootAddition:
    def __init__(self, parent_node: BaseNode, child_node: BaseNode, direction: Union[None, str]):
        self.parent_node = parent_node
        self.child_node = child_node
        self.direction = direction


class RootDeletion:
    def __init__(self, parent_node: BaseNode, child_node: BaseNode):
        self.parent_node = parent_node
        self.child_node = child_node


class RootNodeModification:
    def __init__(self, original_root_node: BaseNode, new_root_node: BaseNode):
        self.original_root_node = original_root_node
        self.new_root_node = new_root_node


class StructuralChange:
    def __init__(self, original_node: BaseNode, new_node: BaseNode):
        self.original_node = original_node
        self.new_node = new_node
