from typing import Optional
from ast_utils.custom_exceptions import NodeNotFoundError
from parser.nodes import BaseNode, Binary, Cell, CellRange, Function, Name, Number, Unary
from copy import deepcopy

from ast_utils.change_classes import (
    ChildAddition,
    ChildDeletion,
    NodeModification,
    RootAddition,
    RootDeletion,
)

def find_node(root: BaseNode, new_node: BaseNode) -> BaseNode:
    target_history = new_node.id_history
    def id_history_matches(node_history: list[str], target_history: list[str]) -> bool:
        # Check if any part of target_history matches with node_history
        return any(node_history[:i] == target_history[:i] for i in range(1, len(target_history) + 1))

    if id_history_matches(root.id_history, target_history):
        return root

    # Recursive search in composite nodes
    if isinstance(root, Function):
        for arg in root.arguments:
            try:
                return find_node(arg, new_node)
            except NodeNotFoundError:
                continue

    elif isinstance(root, Binary):
        try:
            return find_node(root.left, new_node)
        except NodeNotFoundError:
            return find_node(root.right, new_node)

    elif isinstance(root, Unary):
        return find_node(root.expr, new_node)

    # If the node is not found in any of the branches
    raise NodeNotFoundError(f"Node with history {target_history} not found in AST.")


def modify_node(change: NodeModification, user_id: str):
    original_node = change.original_node
    new_node = change.new_node

    match original_node:
        case Binary():
            assert isinstance(new_node, Binary)
            original_node.op = new_node.op

        case CellRange():
            assert isinstance(new_node, CellRange)
            original_node.start = new_node.start
            original_node.end = new_node.end

        case Function():
            assert isinstance(new_node, Function)
            original_node.func_name = new_node.func_name

        case Unary():
            assert isinstance(new_node, Unary)
            original_node.op = new_node.op

        case Cell():
            assert isinstance(new_node, Cell)
            original_node.col = new_node.col
            original_node.row = new_node.row

        case Name():
            assert isinstance(new_node, Name)
            original_node.name = new_node.name

        case Number():
            assert isinstance(new_node, Number)
            original_node.value = new_node.value

        case _:
            raise Exception("Node type to modify not found")

    original_node.refresh_node(user_id)
    change.new_node = original_node # needed to find match in merge.py


def add_child(change: ChildAddition, user_id):
    # Logic to add a child node to a parent node
    # This function appends child_node to the children of parent_node

    child_node = change.child_node
    parent_node = change.parent_node

    if isinstance(parent_node, Function):
        parent_node.arguments.append(child_node)
        child_node.refresh_node(user_id)

    elif isinstance(parent_node, Binary):
        if parent_node.left is None:
            parent_node.left = child_node
            child_node.refresh_node(user_id)
        elif parent_node.right is None:
            parent_node.right = child_node
            child_node.refresh_node(user_id)
        else:
            raise Exception("Binary node already has two children")
    else:
        # Handle other types if needed
        raise Exception("Node type to add child node not found")


def remove_child(change: ChildDeletion, user_id):
    # Logic to remove a child node from a parent node
    # This function removes child_node from parent_node's children

    parent_node = change.parent_node
    child_node = change.child_node

    if isinstance(parent_node, Function):
        # Find and remove the argument with matching id_history
        for i, arg in enumerate(parent_node.arguments):
            if arg.id_history == child_node.id_history:
                parent_node.arguments.pop(i)

    elif isinstance(parent_node, Binary):
        if parent_node.left == child_node:
            parent_node.left = None
        elif parent_node.right == child_node:
            parent_node.right = None

    else:
        # Handle other types if needed
        raise Exception("Node type to remove not found")


def add_root(change: RootAddition, user_id):
    # Logic to add a new root node to the AST
    # This function sets new_root_node as the new root of the AST

    parent_node = change.parent_node
    child_node = change.child_node
    direction = change.direction

    if isinstance(parent_node, Unary):
        parent_node.expr = child_node

    elif isinstance(parent_node, Binary):
        if direction == "left":
            parent_node.left = child_node
        elif direction == "right":
            parent_node.right = child_node
        else:
            raise Exception("Invalid side specified for Binary node addition")
    elif isinstance(parent_node, Function):
        # replace arguments of new_root_node with child_node
        parent_node.arguments = [child_node]
    else:
        raise Exception("Change not supported")

    modified_ast = parent_node
    modified_ast.refresh_node(user_id)

    return modified_ast

def remove_root(original_ast, change: RootDeletion, return_node=False):
    # Logic to remove the root node from the AST
    # This function removes the root node of the AST

    new_root_node = change.child_node
    original_ast = new_root_node
    return original_ast

def replace_root_node(original_ast, new_root_node, return_node=False):
    # Logic to replace the root node of the AST
    # This function sets new_root_node as the new root of the AST

    original_ast = new_root_node
