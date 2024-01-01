from parser.nodes import Binary, Cell, CellRange, Function, Name, Number, Unary


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


def modify_node(node_to_modify, new_node_data, user_id, return_node=False):
    # Logic to modify a node
    # This function updates the node_to_modify based on new_node_data and user_id
    if isinstance(node_to_modify, Binary):
        node_to_modify.op = new_node_data.op

    elif isinstance(node_to_modify, CellRange):
        node_to_modify.start = new_node_data.start
        node_to_modify.end = new_node_data.end

    elif isinstance(node_to_modify, Function):
        node_to_modify.func_name = new_node_data.func_name

    elif isinstance(node_to_modify, Unary):
        node_to_modify.op = new_node_data.op

    elif isinstance(node_to_modify, Cell):
        node_to_modify.col = new_node_data.col
        node_to_modify.row = new_node_data.row

    elif isinstance(node_to_modify, Name):
        node_to_modify.name = new_node_data.name

    elif isinstance(node_to_modify, Number):
        node_to_modify.value = new_node_data.value

    # TODO: Add other node types

    else:
        raise Exception("Node type to modify not found")

    node_to_modify.refresh_node(user_id)

    if return_node:
        updated_node = {"node": node_to_modify, "type": "modification"}
        return updated_node


def add_child_node(parent_node, child_node, user_id, return_node=False):
    # Logic to add a child node to a parent node
    # This function appends child_node to the children of parent_node
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

    # optionally return the updated node
    if return_node:
        updated_node = {
            "node": child_node,
            "parent": parent_node,
            "type": "add_child",
        }
        return updated_node


def remove_child_node(parent_node, child_node, return_node=False):
    # Logic to remove a child node from a parent node
    # This function removes child_node from parent_node's children
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


def add_root_node(
    original_ast, new_root_node, child_node, direction, user_id, return_node=False
):
    # Logic to add a new root node to the AST
    # This function sets new_root_node as the new root of the AST
    if isinstance(new_root_node, Unary):
        new_root_node.expr = child_node
    elif isinstance(new_root_node, Binary):
        if direction == "left":
            new_root_node.left = child_node
        elif direction == "right":
            new_root_node.right = child_node
        else:
            raise Exception("Invalid side specified for Binary node addition")
    elif isinstance(new_root_node, Function):
        # replace arguments of new_root_node with child_node
        new_root_node.arguments = [child_node]
    else:
        raise Exception("Change not supported")

    original_ast = new_root_node
    new_root_node.refresh_node(user_id)

    if return_node:
        updated_node = {
            "node": new_root_node,
            "child": child_node,
            "type": "add_root",
        }
        return (original_ast, updated_node)
    else:
        return original_ast


def remove_root_node(original_ast, new_root_node, return_node=False):
    # Logic to remove the root node from the AST
    # This function removes the root node of the AST
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
