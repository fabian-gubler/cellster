from ast_utils.change_classes import (
    ChildAddition,
    ChildDeletion,
    NodeModification,
    RootAddition,
    RootDeletion,
)
from ast_utils.operations import (
    add_child,
    add_root,
    find_node,
    modify_node,
    remove_child,
    remove_root,
    replace_root_node,
)


class StructuralChangeException(Exception):
    pass


def apply_changes_to_ast(original_ast, changes, user_id):
    updated_nodes: list = []
    for change in changes:
        # TODO: multiple "append" is code duplication
        if isinstance(change, NodeModification):
            # node_to_modify = find_node(original_ast, change["original"].id_history)

            updated_node = modify_node(change, user_id)
            updated_nodes.append(updated_node)

        elif isinstance(change, ChildAddition):
            # parent_node = find_node(original_ast, change["parent"].id_history)

            updated_node = add_child(change, user_id)
            updated_nodes.append(updated_node)

        elif isinstance(change, ChildDeletion):
            # parent_node = find_node(original_ast, change["parent"].id_history)

            updated_node = remove_child(change, user_id)
            updated_nodes.append(updated_node)

        elif isinstance(change, RootAddition):
            # child_node = find_node(original_ast, change["child"].id_history)

            original_ast, updated_nodes = add_root(original_ast, change, user_id)
            updated_nodes.append(updated_node)

        elif isinstance(change, RootDeletion):
            # new_root_node = find_node(original_ast, change["child"].id_history)

            original_ast, updated_node = remove_root(original_ast, change, user_id)
            updated_nodes.append(updated_node)


        elif change["type"] == "root_modification":
            new_root_node = change["modification"]

            original_ast, updated_node = replace_root_node(
                original_ast, new_root_node, user_id, return_node=True
            )
            updated_nodes.append(updated_node)

        else:
            raise StructuralChangeException("Change type not found")

    return original_ast, updated_nodes
