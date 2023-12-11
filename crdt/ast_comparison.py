from itertools import zip_longest
from parser.ast_nodes import (Binary, Cell,  # Name,; Number,; Logical,
                              CellRange, Function, Name, Unary)


def compare_asts(original_node, modified_node):
    changes = []

    def traverse_and_compare(node1, node2):
        # As far as I know this covers most cases (except for root level changes)
        # TODO: Check for coverage of cases

        # if node1 is None or node2 is None:
        #     # Addition or deletion detected
        #     change_type = "addition" if node1 is None else "deletion"
        #     changes.append({"type": change_type, "original": node1, "modification": node2})
        #     return

        if type(node1) != type(node2):
            # Structural change detected due to different types
            # Potential structural change - deeper comparison needed

            # TODO: Rule-based approach to determine parent level additions / deletions
            # Check if this is an addition or a different type of structural change
            # check_for_addition_or_structural_change(node1, node2)

            changes.append(
                {"type": "structural_change", "original": node1, "modification": node2}
            )
            return

        if isinstance(node1, Binary) and isinstance(node2, Binary):
            # Check for changes in operator
            if not node1.compare_content(node2):
                changes.append(
                    {"type": "modification", "original": node1, "modification": node2}
                )

            # Check for changes in operands
            traverse_and_compare(node1.left, node2.left)
            traverse_and_compare(node1.right, node2.right)

        elif isinstance(node1, CellRange) and isinstance(node2, CellRange):
            # Check for changes in cell range
            if not node1.compare_content(node2):
                changes.append(
                    {"type": "modification", "original": node1, "modification": node2}
                )

        elif isinstance(node1, Function) and isinstance(node2, Function):
            # Check for changes in cell value
            if not node1.compare_content(node2):
                changes.append(
                    {"type": "modification", "original": node1, "modification": node2}
                )

            # Check for changes in operands
            for arg1, arg2 in zip_longest(node1.arguments, node2.arguments):
                traverse_and_compare(arg1, arg2)

        elif isinstance(node1, Unary) and isinstance(node2, Unary):
            # Check for changes in cell value
            if not node1.compare_content(node2):
                changes.append(
                    {"type": "modification", "original": node1, "modification": node2}
                )

            # Check for changes in operands
            traverse_and_compare(node1.expr, node2.expr)

        elif isinstance(node1, Cell) and isinstance(node2, Cell):
            # Check for changes in cell value
            if not node1.compare_content(node2):
                changes.append(
                    {"type": "modification", "original": node1, "modification": node2}
                )

        elif isinstance(node1, Name) and isinstance(node2, Name):
            # Check for changes in cell value
            if not node1.compare_content(node2):
                changes.append(
                    {"type": "modification", "original": node1, "modification": node2}
                )

        else:
            # print the node type
            raise Exception("Node type not found for change of type", type(node1))

    def check_for_addition_or_structural_change(node1, node2):
        # Check for a new Binary root node addition
        if isinstance(node2, Binary):
            left_match = traverse_and_compare(node2.left, node1)
            right_match = traverse_and_compare(node2.right, node1)

            if left_match or right_match:
                # Determine which subtree matches and include this information
                matching_subtree = "left" if left_match else "right"
                changes.append(
                    {
                        "type": "addition",
                        "child": matching_subtree,
                        "modification": node2,
                    }
                )
            else:
                # Structural change other than a simple addition
                changes.append(
                    {
                        "type": "structural_change",
                        "original": node1,
                        "modification": node2,
                    }
                )
        else:
            raise Exception("Node type not found for change of type", type(node1))

    traverse_and_compare(original_node, modified_node)
    return changes
