from parser.ast_nodes import (
    Cell,
    CellRange,
    Name,
    Function,
    Number,
    Logical,
    Binary,
    Unary,
)

# utils/reconstruct_formula.py
def reconstruct_formula(node):
    if isinstance(node, Number):
        return str(node.value)

    if isinstance(node, Logical):
        return str(node.value)

    if isinstance(node, Cell):
        return f"{node.col}{node.row}"

    if isinstance(node, CellRange):
        return f"{reconstruct_formula(node.start)}:{reconstruct_formula(node.end)}"

    if isinstance(node, Name):
        return node.name

    if isinstance(node, Function):
        args = ', '.join([reconstruct_formula(arg) for arg in node.arguments])
        return f"{node.func_name}({args})"

    if isinstance(node, Binary):
        left = reconstruct_formula(node.left)
        right = reconstruct_formula(node.right)
        return f"({left} {node.op} {right})"

    if isinstance(node, Unary):
        expr = reconstruct_formula(node.expr)
        return f"({node.op}{expr})"

    return ""
