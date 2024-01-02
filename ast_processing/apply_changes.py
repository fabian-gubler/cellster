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
    for change in changes:
        match change:
            case NodeModification():
                # node_to_modify = find_node(original_ast, change["original"].id_history)
                modify_node(change, user_id)

            case ChildAddition():
                # parent_node = find_node(original_ast, change["parent"].id_history)
                add_child(change, user_id)

            case ChildDeletion():
                # parent_node = find_node(original_ast, change["parent"].id_history)
                remove_child(change, user_id)

            case RootAddition():
                # child_node = find_node(original_ast, change["child"].id_history)
                add_root(original_ast, change, user_id)

            case RootDeletion():
                # new_root_node = find_node(original_ast, change["child"].id_history)
                remove_root(original_ast, change, user_id)

            case _:
                raise StructuralChangeException("Change type not found")

    return original_ast
