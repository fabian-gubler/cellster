from parser.ast_nodes import Function, Unary, Binary
from itertools import zip_longest

def compare_asts(original_node, modified_node):
    changes = []

    def traverse_and_compare(node1, node2):
        if node1 is None and node2 is not None:
            changes.append({'type': 'addition', 'node': node2})
            return
        elif node2 is None and node1 is not None:
            changes.append({'type': 'deletion', 'node': node1})
            return
        elif not node1.compare_content(node2):
            changes.append({'type': 'modification', 'original': node1, 'modified': node2})

        # Extend the comparison to different types of nodes
        if isinstance(node1, Function) and isinstance(node2, Function):
            compare_children(node1.arguments, node2.arguments)

        elif isinstance(node1, Binary) and isinstance(node2, Binary):
            traverse_and_compare(node1.left, node2.left)
            traverse_and_compare(node1.right, node2.right)

        elif isinstance(node1, Unary) and isinstance(node2, Unary):
            traverse_and_compare(node1.expr, node2.expr)

    def compare_children(children1, children2):
        for child1, child2 in zip_longest(children1, children2):
            traverse_and_compare(child1, child2)

    traverse_and_compare(original_node, modified_node)
    print(changes)
    return changes

