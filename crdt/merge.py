from parser.ast_nodes import Cell, CellRange

from crdt.ast_operations import (add_child_node, add_root_node, find_node,
                                 modify_node, remove_child_node,
                                 remove_root_node, replace_root_node)


class NodeNotFoundError(Exception):
    pass


def merge_ast(original_ast, changes):
    for change in changes:
        if change["type"] == "modification":
            modified_node = change["node"]
            original_node = find_node(original_ast, modified_node.id_history)
            handle_modification(original_node, modified_node, user_id="merged")

        elif change["type"] == "addition_arg":
            parent_node = find_node(original_ast, change["parent"].id_history)
            child_node = change["node"]
            add_child_node(parent_node, child_node, child_node.user_id)

        elif change["type"] == "deletion_arg":
            parent_node = find_node(original_ast, change["parent"].id_history)
            child_node = change["node"]
            remove_child_node(parent_node, child_node)

        elif change["type"] == "addition_root":
            child_node = find_node(original_ast, change["child"].id_history)
            new_root_node = change["parent"]
            direction = change["direction"]
            original_ast = add_root_node(
                original_ast,
                new_root_node,
                child_node,
                direction,
                user_id="merged",
                return_node=False,
            )

        elif change["type"] == "deletion_root":
            new_root_node = find_node(original_ast, change["child"].id_history)

            original_ast = remove_root_node(
                original_ast, new_root_node, return_node=False
            )

        elif change["type"] == "root_modification":
            new_root_node = change["modification"]

            original_ast, updated_node = replace_root_node(
                original_ast, new_root_node, user_id="merged", return_node=True
            )
        else:
            raise Exception("Invalid change type")

    return original_ast


def handle_modification(original_node, modified_node, user_id):
    # Local function to calculate depth of id_history
    def calculate_depth(original_history, updated_history):
        last_common_index = -1
        for i in range(min(len(original_history), len(updated_history))):
            if original_history[i] == updated_history[i]:
                last_common_index = i
            else:
                break

        # Calculate depth based on lengths after the last common ID
        if last_common_index != -1:
            return len(updated_history) - last_common_index - 1
        return -1  # No common history found

    if not original_node:
        raise NodeNotFoundError("Node not found in original AST")

    # Enhanced conflict resolution for CellRange nodes
    if isinstance(original_node, CellRange) and isinstance(modified_node, CellRange):
        merged_range = merge_cell_ranges(original_node, modified_node)
        modify_node(original_node, merged_range, user_id="merged")
        return

    depth = calculate_depth(original_node.id_history, modified_node.id_history)

    if depth > 0:
        modify_node(original_node, modified_node, user_id="merged")
    elif depth == 0:
        winner = conflict_resolution(original_node, modified_node)
        if winner == modified_node:
            modify_node(original_node, modified_node, user_id="merged")


def merge_cell_ranges(node1, node2):
    # Local function to convert column name to number
    def col_name_to_number(col):
        number = 0
        for char in col:
            number = number * 26 + (ord(char.upper()) - ord("A") + 1)
        return number

    # Calculating the merged range
    start_row = min(node1.start.row, node2.start.row)
    end_row = max(node1.end.row, node2.end.row)
    start_col = min(
        node1.start.col, node2.start.col, key=lambda x: col_name_to_number(x)
    )
    end_col = max(node1.end.col, node2.end.col, key=lambda x: col_name_to_number(x))

    # Creating the merged range
    merged_range = CellRange(
        Cell(start_col, start_row, user_id="merged"),
        Cell(end_col, end_row, user_id="merged"),
        user_id="merged",
    )

    return merged_range


def conflict_resolution(original_node, updated_node):
    # compare timestamps
    if original_node.timestamp > updated_node.timestamp:
        # original_node commited later
        return updated_node
    elif original_node.timestamp < updated_node.timestamp:
        # updated_node is more recent
        return original_node
    # timestamps are equal
    else:
        if original_node.tie_breaker_value() > updated_node.tie_breaker_value():
            return updated_node
