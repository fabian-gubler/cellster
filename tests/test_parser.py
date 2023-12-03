import pytest
from parser.parser import parse, FormulaParseError
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


def test_parse_number():
    ast = parse("123")
    assert isinstance(ast, Number)
    assert ast.value == 123
    assert ast.user_id == "default_user"

    ast = parse("3.14")
    assert isinstance(ast, Number)
    assert ast.value == 3.1


def test_parse_logical():
    ast = parse("TRUE")
    assert isinstance(ast, Logical)
    assert ast.value is True

    ast = parse("FALSE")
    assert isinstance(ast, Logical)
    assert ast.value is False


def test_parse_cell():
    ast = parse("A1")
    assert isinstance(ast, Cell)
    assert ast.col == "A"
    assert ast.row == 1


def test_parse_cell_range():
    ast = parse("A1:B2")
    assert isinstance(ast, CellRange)
    assert isinstance(ast.start, Cell)
    assert isinstance(ast.end, Cell)
    assert ast.start.col == "A"
    assert ast.start.row == 1
    assert ast.end.col == "B"
    assert ast.end.row == 2


def test_parse_function():
    ast = parse("SUM(A1, B2)")
    assert isinstance(ast, Function)
    assert ast.func_name == "SUM"
    assert len(ast.arguments) == 2
    assert isinstance(ast.arguments[0], Cell)
    assert isinstance(ast.arguments[1], Cell)


def test_parse_binary_operation():
    ast = parse("1 + 2")
    assert isinstance(ast, Binary)
    assert ast.op == "+"
    assert isinstance(ast.left, Number)
    assert isinstance(ast.right, Number)
    assert ast.left.value == 1
    assert ast.right.value == 2


def test_parse_unary_operation():
    ast = parse("-1")
    assert isinstance(ast, Unary)
    assert ast.op == "-"
    assert isinstance(ast.expr, Number)
    assert ast.expr.value == 1


def test_parse_complex_expression():
    ast = parse("SUM(A1:B2) * 3")
    assert isinstance(ast, Binary)
    assert ast.op == "*"
    assert isinstance(ast.left, Function)
    assert isinstance(ast.right, Number)

    ast = parse("SUM(A2:A9)+B1-B2*C3")


def test_parse_error_incomplete_function_call():
    with pytest.raises(FormulaParseError):
        parse("SUM(")  # Incomplete function call

def test_parse_error_incomplete_expression():
    with pytest.raises(FormulaParseError):
        parse("A1 + ")  # Incomplete expression
