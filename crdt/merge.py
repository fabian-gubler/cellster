from parser.tree_operations import find_node, find_parent_and_child, add_node, delete_node
from parser.ast_nodes import CellRange, Cell
from crdt.apply_changes import replace_node

class NodeNotFoundError(Exception):
    pass

def merge_ast(original_ast, changes):
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

    for change in changes:
        # Handle modifications

        if change['type'] == 'modification':
            modified_node = change['node']
            original_node = find_node(original_ast, modified_node.id_history)

            # print("Modified node ID history: ", modified_node.id_history)
            # print("Original node ID history: ", original_node.id_history)

            if not original_node:
                raise NodeNotFoundError("Node not found in original AST")

            # Enhanced conflict resolution for CellRange nodes
            if isinstance(original_node, CellRange) and isinstance(modified_node, CellRange):
                merged_range = merge_cell_ranges(original_node, modified_node)
                replace_node(original_node, merged_range)


            depth = calculate_depth(original_node.id_history, modified_node.id_history)

            if depth > 0:
                replace_node(original_node, modified_node)
            elif depth == 0:
                conflict_resolution(original_node, modified_node)  # Placeholder for conflict resolution logic

        # # Handle additions
        # elif change['type'] == 'addition':
        #     parent_node = find_node(original_ast, change["parent_id_history"])
        #     add_node(parent_node, change["node"], child_side=change["child_side"])
        #
        # # Handle deletions
        # elif change['type'] == 'deletion':
        #     parent, child_to_delete = find_parent_and_child(original_ast, change["node"].id_history)
        #     if parent and child_to_delete:
        #         delete_node(parent, child_to_delete.id_history)
        
        else: 
            raise Exception("Invalid change type")

    return original_ast


def merge_cell_ranges(node1, node2):
    print("Merging:", node1, "with", node2)  # Debug input CellRanges
    start_row = min(node1.start.row, node2.start.row)
    end_row = max(node1.end.row, node2.end.row)
    start_col = min(node1.start.col, node2.start.col, key=lambda x: col_name_to_number(x))
    end_col = max(node1.end.col, node2.end.col, key=lambda x: col_name_to_number(x))

    # Creating the merged range
    merged_range = CellRange(Cell(start_col, start_row, user_id="merged"), Cell(end_col, end_row, user_id="merged"), user_id="merged")

    print("Merged range:", merged_range)  # Debug output

    return merged_range


def col_name_to_number(col):
  """Converts an Excel column name to a number (e.g., 'A' -> 1, 'Z' -> 26, 'AA' -> 27)."""
  number = 0
  for char in col:
      number = number * 26 + (ord(char.upper()) - ord('A') + 1)
  return number

def conflict_resolution(original_node, updated_node):
    # Placeholder function for conflict resolution
    # Implement conflict resolution logic here
    raise NotImplementedError
