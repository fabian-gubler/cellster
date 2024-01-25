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
                modify_node(change, user_id)

            case ChildAddition():
                add_child(change, user_id)

            case ChildDeletion():
                remove_child(change, user_id)

            case RootAddition():
                original_ast = add_root(change, user_id)

            case RootDeletion():
                original_ast = remove_root(original_ast, change, user_id)

            case _:
                raise StructuralChangeException("Change type not found")
