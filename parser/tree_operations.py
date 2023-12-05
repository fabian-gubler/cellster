import uuid

# Assuming that BaseNode and its derived classes are defined in ast_nodes.py
from parser.ast_nodes import BaseNode, Function, Binary, Unary


def find_node(root, target_history):
    # Check for the longest common prefix in the history
    common_length = min(len(root.id_history), len(target_history))
    if root.id_history[:common_length] == target_history[:common_length]:
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
    parent, child_to_replace = find_parent_and_child(root, target_history)

    if parent is None and child_to_replace is root:
        # Handle the root node replacement
        if isinstance(root, Function) and isinstance(new_node, Function):
            # Preserve unchanged children for Function nodes
            new_node.arguments = [
                child if child.compare_content(new_arg) else new_arg
                for child, new_arg in zip_longest(root.arguments, new_node.arguments)
            ]
        elif isinstance(root, Binary) and isinstance(new_node, Binary):
            # Preserve unchanged children for Binary nodes
            new_node.left = root.left if root.left.compare_content(new_node.left) else new_node.left
            new_node.right = root.right if root.right.compare_content(new_node.right) else new_node.right
        elif isinstance(root, Unary) and isinstance(new_node, Unary):
            # Preserve unchanged child for Unary node
            new_node.expr = root.expr if root.expr.compare_content(new_node.expr) else new_node.expr
        new_node.id_history = root.id_history + [str(uuid.uuid4())]

        return {'node': new_node, 'type': 'modification'}

    if parent and child_to_replace:
        if isinstance(parent, Function):
            parent.arguments = [
                new_node if child is child_to_replace else child
                for child in parent.arguments
            ]
        elif isinstance(parent, Binary):
            if parent.left is child_to_replace:
                parent.left = new_node
            elif parent.right is child_to_replace:
                parent.right = new_node
        elif isinstance(parent, Unary):
            if parent.expr is child_to_replace:
                parent.expr = new_node
        new_node.id_history = child_to_replace.id_history + [str(uuid.uuid4())]

        return {'node': new_node, 'type': 'modification'}

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

