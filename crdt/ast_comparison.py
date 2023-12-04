from parser.ast_nodes import Function, Unary, Binary
from itertools import zip_longest


def compare_asts(original_node, modified_node):
    changes = []

    def traverse_and_compare(node1, node2):
        if type(node1) != type(node2):
            # Root level change detected
            changes.append(
                {"type": "root_change", "original": node1, "modified": node2}
            )
            # If the new root is a Unary or Binary node, compare its children
            if isinstance(node2, (Unary, Binary)):
                traverse_and_compare(node1, get_child(node2))
            return

        if not node1.compare_content(node2):
            # Content modification detected
            change_type = "modification"
            if node1.parent is None:  # if this is the root node
                change_type = "modification"
            changes.append({"type": change_type, "original": node1, "modified": node2})
        if isinstance(node1, (Function, Binary, Unary)):
            compare_children(get_children(node1), get_children(node2), node1, node2)

    def compare_children(children1, children2, parent1, parent2):
        for index, (child1, child2) in enumerate(zip_longest(children1, children2)):
            if child1 is None or child2 is None:
                change_type = "addition" if child1 is None else "deletion"
                child_side = None
                if isinstance(parent2, Binary):
                    child_side = "left" if index == 0 else "right"
                changes.append({
                    "type": change_type,
                    "node": child2 if child1 is None else child1,
                    # parent_id history must be from the original node
                    "parent_id_history": parent1.id_history,
                    "child_side": child_side  # New field
                })
                # print(f"Detected change: {changes[-1]}")  # Print the last change detected
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

    def get_child(node):
        return node.expr if isinstance(node, Unary) else (node.left, node.right)

    traverse_and_compare(original_node, modified_node)
    return changes
