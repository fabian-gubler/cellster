from my_parser import Function, CellRange, Cell, Name, Number, Logical, Binary, Unary

# Function that converts Abstract Syntax Tree (AST) back to String.
def ast_to_string(node, parent=None):

    if isinstance(node, Function):
        # If node is a Function, iterate through all arguments and convert them to a string. Joins these strings with commas.
        # The function name is then combined with these arguments enclosed in parentheses.
        args_string = ', '.join(ast_to_string(arg, node) for arg in node.arguments)
        return f"{node.func_name}({args_string})"

    elif isinstance(node, CellRange):
        # If the node is a CellRange, it converts the start and end cells of the range to their string representations and joins them with a colon like "A1:B2".
        return f"{ast_to_string(node.start, node)}:{ast_to_string(node.end, node)}"

    elif isinstance(node, Cell):
        # If the node is a Cell, it converts the cell to its string representation like "A1".
        return f"{node.col}{node.row}"

    elif isinstance(node, Name):
        # If the node is a Name/Identifier (like a named range or variable), it converts the Name/Identifier to a string.
        return node.name

    elif isinstance(node, Number):
        # If the node is a Number, it converts the number to a string.
        return str(node.value)

    elif isinstance(node, Logical):
        # If the node is a Logical (boolean value), it converts it to a string ("TRUE" or "FALSE").
        return "TRUE" if node.value else "FALSE"

    elif isinstance(node, Binary):
        # If the node is a Binary operation (like addition, subtraction), it converts both the left and right operands to strings and joins them with the operator (e.g., "A1 + B1").
        # If this binary operation is not the top-level operation (has a parent), it encloses the operation in parentheses.
        left = ast_to_string(node.left, node)
        right = ast_to_string(node.right, node)
        operation = f"{left}{node.op}{right}"
        if parent is None:
            return operation
        else:
            return f"({operation})"

    elif isinstance(node, Unary):
        # If the node is a Unary operation, it converts the operand to a string and precedes it with the unary operator (e.g., "-A1").
        return f"{node.op}{ast_to_string(node.expr, node)}"

    else:
        # If the node type is not recognized, it raises an error.
        raise ValueError(f"Unsupported AST node type: {type(node)}")