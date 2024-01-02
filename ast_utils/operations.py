from parser.nodes import Binary, Cell, CellRange, Function, Name, Number, Unary

from ast_utils.change_classes import (
    ChildAddition,
    ChildDeletion,
    NodeModification,
    RootAddition,
    RootDeletion,
)


def find_node(root, target_history):
    def id_history_matches(node_history, target_history):
        # Function to check if any part of target_history matches with node_history
        for i in range(1, len(target_history) + 1):
            if node_history[:i] == target_history[:i]:
                return True
        return False

    if id_history_matches(root.id_history, target_history):
        return root

    # Recursive search in composite nodes
    if isinstance(root, Function):
        for arg in root.arguments:
            result = find_node(arg, target_history)
            if result:
                return result

    if isinstance(root, Binary):
        left_result = find_node(root.left, target_history)
        if left_result:
            return left_result

        right_result = find_node(root.right, target_history)
        if right_result:
            return right_result

    if isinstance(root, Unary):
        return find_node(root.expr, target_history)




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

    if return_node:
        updated_node = {
            "node": child_node,
            "parent": parent_node,
            "type": "del_child",
        }
        return updated_node


def add_root(original_ast, change: RootAddition, user_id):

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

    original_ast = parent_node
    parent_node.refresh_node(user_id)

    if return_node:
        updated_node = {
            "node": parent_node,
            "child": child_node,
            "type": "add_root",
        }
        return (original_ast, updated_node)
    else:
        return original_ast


def remove_root(original_ast, change: RootDeletion, return_node=False):
    # Logic to remove the root node from the AST
    # This function removes the root node of the AST

    new_root_node = change.parent_node
    original_ast = new_root_node

    if return_node:
        updated_node = {"node": new_root_node, "type": "del_root"}
        return (original_ast, updated_node if return_node else original_ast)


def replace_root_node(original_ast, new_root_node, return_node=False):
    # Logic to replace the root node of the AST
    # This function sets new_root_node as the new root of the AST

    original_ast = new_root_node

    if return_node:
        updated_node = {"node": new_root_node, "type": "root_modification"}
        return (original_ast, updated_node if return_node else original_ast)
    else:
        return original_ast
