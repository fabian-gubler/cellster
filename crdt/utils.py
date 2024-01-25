from parser.nodes import Cell, CellRange


def conflict_resolution(original_node, updated_node) -> bool:
    # compare timestamps
    if original_node.timestamp > updated_node.timestamp:
        # original_node commited later
        return True
    elif original_node.timestamp < updated_node.timestamp:
        # updated_node is more recent
        return False
    # timestamps are equal
    else:
        if original_node.tie_breaker_value() > updated_node.tie_breaker_value():
            return True
        else:
            return False


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


def merge_cell_ranges(node1, node2) -> CellRange:
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
