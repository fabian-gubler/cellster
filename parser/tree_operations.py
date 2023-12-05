import uuid

# Assuming that BaseNode and its derived classes are defined in ast_nodes.py
from parser.ast_nodes import BaseNode, Function, Binary, Unary


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

    # Extend this logic to other composite node types if necessary

    return None



def find_parent_and_child(root, child_history, parent=None):
    if isinstance(root, BaseNode):
        if root.id_history == child_history:
            return (parent, root)

    if isinstance(root, Function):
        for arg in root.arguments:
            result = find_parent_and_child(arg, child_history, root)
            if result[1]:
                return result

    if isinstance(root, Binary):
        left_result = find_parent_and_child(root.left, child_history, root)
        if left_result[1]:
            return left_result
        right_result = find_parent_and_child(root.right, child_history, root)
        if right_result[1]:
            return right_result

    if isinstance(root, Unary):
        return find_parent_and_child(root.expr, child_history, root)

    return (None, None)


from copy import deepcopy


def replace_node(root, target_history, new_node):

    node_to_edit = find_node(root, target_history)

    if isinstance(node_to_edit, Binary):
        node_to_edit.op = new_node.op

    node_to_edit.id_history += [str(uuid.uuid4())]

    return False

def delete_node(root, target_history):
    parent, child_to_delete = find_parent_and_child(root, target_history)
    if parent and child_to_delete:
        if isinstance(parent, Function):
            parent.arguments.remove(child_to_delete)
        elif isinstance(parent, Binary):
            if parent.left is child_to_delete:
                parent.left = None
            elif parent.right is child_to_delete:
                parent.right = None
        elif isinstance(parent, Unary):
            if parent.expr is child_to_delete:
                parent.expr = None
        return True
    return False

def add_node(parent, new_node, position=None, child_side=None):
    if isinstance(parent, Function):
        if position is not None:
            parent.arguments.insert(position, new_node)
        else:
            parent.arguments.append(new_node)

    elif isinstance(parent, Binary):
        if child_side == "left":
            parent.left = new_node
        elif child_side == "right":
            parent.right = new_node

    elif isinstance(parent, Unary):
        parent.expr = new_node

    new_node.parent = parent
    return {'node': new_node, 'type': 'addition'}

