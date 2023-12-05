from parser.tree_operations import (
    delete_node,
    find_node,
    find_parent_and_child,
    add_node,
    delete_node,
)

from parser.ast_nodes import (
    Cell,
    CellRange,
    Name,
    Function,
    Number,
    Logical,
    Binary,
    Unary,
)

from copy import deepcopy
import uuid


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

        else:
            raise StructuralChangeException("Change type not found")

    return original_ast, updated_nodes

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

            # TODO: Add other node types

            else:
                raise StructuralChangeException(type(node_to_change))

            updated_node={"node": node_to_change, "type": "modification"}
            return updated_node
