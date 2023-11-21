# ast_comparison.py

from parser.formula_parser import Cell, Number, Logical, Binary, Unary, Function, CellRange

def compare_ast_nodes(node1, node2):

    # Base case: Check if both nodes are None
    if node1 is None and node2 is None:
        return True
    if node1 is None or node2 is None:
        return False

    if type(node1) != type(node2):
        return False

    if isinstance(node1, (Number, Logical)):
        return node1.value == node2.value

    if isinstance(node1, Cell):
        return node1.col == node2.col and node1.row == node2.row

    if isinstance(node1, CellRange):
        return compare_ast_nodes(node1.start, node2.start) and compare_ast_nodes(node1.end, node2.end)

    if isinstance(node1, Function):
        if node1.func_name != node2.func_name or len(node1.arguments) != len(node2.arguments):
            return False
        return all(compare_ast_nodes(arg1, arg2) for arg1, arg2 in zip(node1.arguments, node2.arguments))

    if isinstance(node1, Binary):
        return node1.op == node2.op and compare_ast_nodes(node1.left, node2.left) and compare_ast_nodes(node1.right, node2.right)

    if isinstance(node1, Unary):
        return node1.op == node2.op and compare_ast_nodes(node1.expr, node2.expr)

    # Extend this comparison to other node types as necessary

    return False
