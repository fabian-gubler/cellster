from parser.ast_nodes import Function, Unary, Binary
from itertools import zip_longest


def compare_asts(original_node, modified_node):
    changes = []

    def traverse_and_compare(node1, node2):
        if type(node1) != type(node2):
            changes.append({"type": "structural_change", "original": node1, "modification": node2})
            return

        if not node1.compare_content(node2):
            changes.append({"type": "modification", "original": node1, "modification": node2})

        if isinstance(node1, Binary) or isinstance(node1, Unary):
            print("Comparing nodes:", node1, node2)

        if isinstance(node1, (Function, Binary, Unary)):
            compare_children(get_children(node1), get_children(node2))

    def compare_children(children1, children2):
        for child1, child2 in zip_longest(children1, children2):
            if not child1 or not child2:
                changes.append({"type": "structural_change", "original": child1, "modification": child2})
            else:
                traverse_and_compare(child1, child2)

    def get_children(node):
        if isinstance(node, Function):
            return node.arguments
        elif isinstance(node, Binary):
            return [node.left, node.right]
        elif isinstance(node, Unary):
            return [node.expr]
        return []

    traverse_and_compare(original_node, modified_node)
    return changes
