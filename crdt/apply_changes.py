from parser.tree_operations import (
    delete_node,
    find_node,
    replace_node,
    find_parent_and_child,
    add_node,
    delete_node,
)

from parser.ast_nodes import BaseNode, Function, Binary, Unary

from copy import deepcopy


class StructuralChangeException(Exception):
    pass


def apply_changes_to_ast(original_ast, changes):
    updated_nodes = []
    for change in changes:
        if change["type"] == "modification":
            modified_node = change["modification"]
            original_node = find_node(original_ast, change["original"].id_history)

            if original_node is None:
                raise StructuralChangeException("Node not found in original AST")

            new_node = replace_node(
                original_ast, original_node.id_history, change["modification"]
            )

            # print("Original node ID history: ", original_node.id_history)
            # print(
            #     f"Applied change: {change["type"]}, Updated id_history: {change["modification"].id_history}"
            # )

            if new_node:
                updated_nodes.append(new_node)

        else:
            raise StructuralChangeException("Change type not found")

        # elif change["type"] == "addition":
        #     # Logic to add a node to the AST
        #     # This uses add_node() from tree_operations.py
        #     parent_node = find_node(original_ast, change["parent_id_history"])
        #     if parent_node:
        #         new_node = add_node(
        #             parent_node, change["node"], child_side=change["child_side"]
        #         )
        #     else:
        #         raise StructuralChangeException("Parent node not found")
        #
        #     if new_node:
        #         updated_nodes.append(new_node)
        #
        # elif change["type"] == "deletion":
        #     parent, child_to_delete = find_parent_and_child(
        #         original_ast, change["node"].id_history
        #     )
        #     if parent and child_to_delete:
        #         delete_node(parent, child_to_delete.id_history)
        #     else:
        #         raise StructuralChangeException("Parent node not found")


    return original_ast, updated_nodes
