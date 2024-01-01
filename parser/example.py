import sys

from formula_parser import *

"""
Traverse the AST recursively and collect all the function names that occur in the tree.
  Arguments: ast = the result of calling formula_parser.parse on the source code
  Returns: a set of strings
"""


def collect_funcs(ast):
    if type(ast) in [Cell, CellRange, Number, Logical, Name]:
        return set()
    elif type(ast) is Function:
        s = set()
        s.add(ast.func_name)
        for arg in ast.arguments:
            s = s.union(collect_funcs(arg))
        return s
    elif type(ast) is Unary:
        return collect_funcs(ast.expr)
    elif type(ast) is Binary:
        return collect_funcs(ast.left).union(collect_funcs(ast.right))


try:
    code = "HELLO(SUM(A1:A3), 1+2*3-ABS(B14-MY_FUNC(C67)), IF(true, false, -10e-5))"
    ast = parse(code)
    print(">", code)
    print("The functions are:", collect_funcs(ast))

    while True:
        code = input("> ")
        ast = parse(code)
        print("The parsed AST is: %s" % ast)
        print("The functions are: %s" % collect_funcs(ast))

except FormulaParseError as error:
    sys.stderr.write("Found an error:\n\t%s\n" % error)

except EOFError:
    print("Bye!")
