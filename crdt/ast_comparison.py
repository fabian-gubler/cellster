from itertools import zip_longest
from parser.ast_nodes import Binary, Cell, CellRange, Function, Name, Number, Unary


def compare_asts(original_node, modified_node):
    changes = []

    def traverse_and_compare(node1, node2, comparison_context="standard"):
        # Modify the behavior based on the comparison context

        if comparison_context == "deletion_check":
            # Return True/False instead of appending to 'changes'
            return node1.compare_content(node2) if node1 and node2 else False

        if comparison_context == "addition_check":
            # Special handling for addition checks
            # Return True/False instead of appending to 'changes'
            if type(node1) == type(node2):
                return node1.compare_content(
                    node2
                )  # TODO: This should be done iteratively
            else:
                return False

        if type(node1) != type(node2):
            if node1.is_root() and node2.is_root():
                # Exclude composite types (Function, Binary, Unary)
                if not isinstance(node1, (Function, Binary, Unary)) and not isinstance(
                    node2, (Function, Binary, Unary)
                ):
                    changes.append(
                        {
                            "type": "root_modification",
                            "original": node1,
                            "modification": node2,
                        }
                    )
            if not check_for_addition_or_structural_change(node1, node2):
                return  # No further traversal needed

        if isinstance(node1, Binary) and isinstance(node2, Binary):
            # Check for changes in operator
            if not node1.compare_content(node2):
                changes.append(
                    {"type": "modification", "original": node1, "modification": node2}
                )

            # Check for changes in operands
            if not isinstance(node1.left, type(node2.left)):
                changes.append(
                    {"type": "del_child", "parent": node1, "child": node1.left}
                )
                changes.append(
                    {"type": "add_child", "parent": node1, "child": node2.left}
                )
            else:
                traverse_and_compare(node1.left, node2.left)

            if not isinstance(node1.right, type(node2.right)):
                changes.append(
                    {"type": "del_child", "parent": node1, "child": node1.right}
                )
                changes.append(
                    {"type": "add_child", "parent": node1, "child": node2.right}
                )
            else:
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
                if arg1 is None:
                    # New argument added in modified_node
                    changes.append(
                        {"type": "add_child", "parent": node1, "child": arg2}
                    )
                elif arg2 is None:
                    # Argument removed in modified_node (if you want to handle deletions)
                    changes.append(
                        {"type": "del_child", "parent": node1, "child": arg1}
                    )
                elif type(arg1) != type(arg2):
                    # Different type of argument found, treat as deletion and addition
                    changes.append(
                        {"type": "del_child", "parent": node1, "child": arg1}
                    )
                    changes.append(
                        {"type": "add_child", "parent": node1, "child": arg2}
                    )
                else:
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

        elif isinstance(node1, Number) and isinstance(node2, Number):
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
            left_match = traverse_and_compare(
                node2.left, node1, comparison_context="addition_check"
            )
            right_match = traverse_and_compare(
                node2.right, node1, comparison_context="addition_check"
            )

            if left_match or right_match:
                # Determine which subtree matches and include this information
                matching_subtree = "left" if left_match else "right"
                changes.append(
                    {
                        "type": "add_root",
                        "direction": matching_subtree,
                        "child": node1,
                        "parent": node2,
                    }
                )
                return False
            else:
                # Structural change other than a simple addition
                changes.append(
                    {
                        "type": "structural_change",
                        "original": node1,
                        "modification": node2,
                    }
                )
        elif isinstance(node1, Binary):
            if traverse_and_compare(
                node1.left, node2, comparison_context="deletion_check"
            ) or traverse_and_compare(
                node1.right, node2, comparison_context="deletion_check"
            ):
                changes.append(
                    {
                        "type": "del_root",
                        "child": node1.left
                        if traverse_and_compare(
                            node1.left, node2, comparison_context="deletion_check"
                        )
                        else node1.right,
                        "parent": node2,
                    }
                )
                return False

            else:
                raise Exception("Node type not found for change of type", type(node1))
        # deletion check
        elif isinstance(node1, Unary):
            if traverse_and_compare(
                node1.expr, node2, comparison_context="deletion_check"
            ):
                changes.append(
                    {
                        "type": "del_root",
                        "child": node1.expr,
                        "parent": node1,
                    }
                )
                return False
        # addition check
        elif isinstance(node2, Unary):
            if traverse_and_compare(
                node2.expr, node1, comparison_context="addition_check"
            ):
                changes.append(
                    {
                        "type": "add_root",
                        "direction": None,
                        "child": node1,
                        "parent": node2,
                    }
                )
                return False
            else:
                changes.append(
                    {
                        "type": "structural_change",
                        "original": node1,
                        "direction": None,
                        "modification": node2,
                    }
                )
                return False

        elif isinstance(node2, Function):
            for arg in node2.arguments:
                if traverse_and_compare(
                    arg, node1, comparison_context="addition_check"
                ):
                    changes.append(
                        {
                            "type": "add_root",
                            "direction": None,
                            "child": node1,
                            "parent": node2,
                        }
                    )
                    return False

        elif isinstance(node1, Function):
            for arg in node1.arguments:
                if traverse_and_compare(
                    arg, node2, comparison_context="deletion_check"
                ):
                    changes.append(
                        {
                            "type": "del_root",
                            "child": arg,
                            "parent": node2,
                        }
                    )
                    return False

    traverse_and_compare(original_node, modified_node)
    return changes
