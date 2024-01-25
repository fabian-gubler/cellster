from parser.nodes import CellRange

from ast_utils.change_classes import ChildAddition, ChildDeletion, NodeModification, RootAddition
from ast_utils.custom_exceptions import NodeNotFoundError
from ast_utils.operations import find_node
from crdt.utils import calculate_depth, conflict_resolution, merge_cell_ranges


def merge_changes(original_ast, changes):
    merged_changes = []

    for change in changes:
        match change:
            case NodeModification():
                new_node = change.new_node
                try:
                    original_node = find_node(original_ast, new_node)
                except NodeNotFoundError as e:
                    print(f" Error: {e}")
                    continue

                # Special Case: CellRange
                if isinstance(original_node, CellRange) and isinstance(
                    new_node, CellRange
                ):
                    merged_range = merge_cell_ranges(original_node, new_node)
                    modification = NodeModification(original_node, merged_range)
                    merged_changes.append(modification)
                    continue  # No further action needed

                if handle_node_modification(original_node, new_node):
                    change.original_node = original_node
                    merged_changes.append(change)
                else:
                    continue  # No further action needed

            case ChildAddition():
                child_node = change.child_node
                try:
                    parent_node = find_node(original_ast, change.parent_node)
                except NodeNotFoundError as e:
                    print(f" Error: {e}")
                    continue
                addition = ChildAddition(parent_node, child_node)
                merged_changes.append(addition)

            case ChildDeletion():
                child_node = change.child_node
                try:
                    parent_node = find_node(original_ast, change.parent_node)
                except NodeNotFoundError as e:
                    print(f" Error: {e}")
                    continue
                deletion = ChildDeletion(parent_node, child_node)
                merged_changes.append(deletion)

            case RootAddition():
                try:
                    child_node = find_node(original_ast, change.child_node)
                except NodeNotFoundError as e:
                    print(f" Error: {e}")
                    continue

                new_root = change.parent_node
                direction = change.direction
                addition = RootAddition(new_root, child_node, direction)
                merged_changes.append(addition)

            case _:
                raise Exception(f"Unhandled change type: {type(change)}")

    # TODO: Handle root addition and deletion
    return merged_changes


def handle_node_modification(original_node, new_node) -> bool:
    depth = calculate_depth(original_node.id_history, new_node.id_history)

    # Conflict detected at the same level
    if depth == 0:
        if conflict_resolution(original_node, new_node):
            return True
        else:
            return False

    # No conflict, modify node
    if depth > 0:
        return True

    # Negative depth indicates no action needed
    return False
