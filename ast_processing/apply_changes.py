from ast_utils.operations import (
    add_child_node,
    add_root_node,
    find_node,
    modify_node,
    remove_child_node,
    remove_root_node,
    replace_root_node,
)


class StructuralChangeException(Exception):
    pass


def apply_changes_to_ast(original_ast, changes, user_id):
    updated_nodes = []
    for change in changes:
        # print("Change detected:", change)  # Debugging statement
        if change["type"] == "modification":
            new_node_data = change["modification"]
            node_to_modify = find_node(original_ast, change["original"].id_history)

            updated_node = modify_node(
                node_to_modify, new_node_data, user_id, return_node=True
            )
            updated_nodes.append(updated_node)

        elif change["type"] == "add_child":
            parent_node = find_node(original_ast, change["parent"].id_history)
            child_node = change["child"]

            updated_node = add_child_node(
                parent_node, child_node, user_id, return_node=True
            )
            updated_nodes.append(updated_node)

        elif change["type"] == "del_child":
            parent_node = find_node(original_ast, change["parent"].id_history)
            child_node = change["child"]
            if parent_node is None:
                raise Exception("Parent node not found in original AST")

            updated_node = remove_child_node(parent_node, child_node, return_node=True)
            updated_nodes.append(updated_node)

        elif change["type"] == "add_root":
            child_node = find_node(original_ast, change["child"].id_history)
            new_root_node = change["parent"]
            direction = change["direction"]

            original_ast, updated_node = add_root_node(
                original_ast,
                new_root_node,
                child_node,
                direction,
                user_id,
                return_node=True,
            )
            updated_nodes.append(updated_node)

        elif change["type"] == "del_root":
            new_root_node = find_node(original_ast, change["child"].id_history)

            original_ast, updated_node = remove_root_node(
                original_ast, new_root_node, return_node=True
            )
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
