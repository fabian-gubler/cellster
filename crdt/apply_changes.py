from parser.ast_nodes import CellRange  # Number,; Logical,
from parser.ast_nodes import Binary, Cell, Function, Name, Unary


class StructuralChangeException(Exception):
    pass


def apply_changes_to_ast(original_ast, changes, user_id):
    updated_nodes = []
    for change in changes:
        # print("Change detected:", change)  # Debugging statement
        if change["type"] == "modification":
            node_to_change = find_node(original_ast, change["original"].id_history)

            if node_to_change is None:
                raise StructuralChangeException("Node not found in original AST")

            updated_node = replace_node(node_to_change, change["modification"], user_id)

            updated_nodes.append(updated_node)

        elif change["type"] == "addition_arg":
            node_to_add = find_node(original_ast, change["parent"].id_history)
            child_node = change["child"]
            if node_to_add is None:
                raise Exception("Parent node not found in original AST")
            updated_node = add_child(node_to_add, child_node, user_id)
            updated_nodes.append(updated_node)

        elif change["type"] == "deletion_arg":
            node_to_remove = find_node(original_ast, change["parent"].id_history)
            child_node = change["child"]
            if node_to_remove is None:
                raise Exception("Parent node not found in original AST")
            updated_node = remove_child(node_to_remove, child_node)
            updated_nodes.append(updated_node)

        else:
            raise StructuralChangeException("Change type not found")

    return original_ast, updated_nodes


def add_child(node_to_add, child_node, user_id):
    if isinstance(node_to_add, Function):
        node_to_add.arguments.append(child_node)
        child_node.refresh_node(user_id)
    elif isinstance(node_to_add, Binary):
        if node_to_add.left is None:
            node_to_add.left = child_node
            child_node.refresh_node(user_id)
        elif node_to_add.right is None:
            node_to_add.right = child_node
            child_node.refresh_node(user_id)
        else:
            raise Exception("Binary node already has two children")
    else:
        # Handle other types if needed
        raise Exception("Node type to add not found")

    updated_node = {"node": node_to_add, "type": "addition_arg"}
    return updated_node


def remove_child(node_to_remove, child_node):
    if isinstance(node_to_remove, Function):
        node_to_remove.arguments.remove(child_node)
    elif isinstance(node_to_remove, Binary):
        if node_to_remove.left == child_node:
            node_to_remove.left = None
        elif node_to_remove.right == child_node:
            node_to_remove.right = None
    else:
        # Handle other types if needed
        raise Exception("Node type to remove not found")

    updated_node = {"node": node_to_remove, "type": "deletion_arg"}
    return updated_node


def replace_node(node_to_change, changed_node, user_id):
    if isinstance(node_to_change, Binary):
        node_to_change.op = changed_node.op
        node_to_change.refresh_node(user_id)

    elif isinstance(node_to_change, CellRange):
        node_to_change.start = changed_node.start
        node_to_change.end = changed_node.end
        node_to_change.refresh_node(user_id)

    elif isinstance(node_to_change, Function):
        node_to_change.func_name = changed_node.func_name
        node_to_change.refresh_node(user_id)

    elif isinstance(node_to_change, Unary):
        node_to_change.op = changed_node.op
        node_to_change.refresh_node(user_id)

    elif isinstance(node_to_change, Cell):
        node_to_change.col = changed_node.col
        node_to_change.row = changed_node.row
        node_to_change.refresh_node(user_id)

    elif isinstance(node_to_change, Name):
        node_to_change.name = changed_node.name
        node_to_change.refresh_node(user_id)

    # TODO: Add other node types

    else:
        raise StructuralChangeException(type(node_to_change))

    updated_node = {"node": node_to_change, "type": "modification"}
    return updated_node


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
