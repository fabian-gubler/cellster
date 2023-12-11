# test_ast_nodes.py
from parser.ast_nodes import (Binary, Cell, CellRange, Function, Logical, Name,
                              Number, Unary)

import pytest  # noqa: F401

# Test AST node enhancements


@pytest.fixture
def sample_ast_nodes():
    number_node = Number(5, "user1")
    function_node = Function("SUM", [number_node], "user1")
    return number_node, function_node


def test_node_parent_reference(sample_ast_nodes):
    number_node, function_node = sample_ast_nodes
    assert number_node.parent == function_node


def test_node_type_information(sample_ast_nodes):
    number_node, _ = sample_ast_nodes
    assert number_node.node_type == "Number"


#
def test_node_position_information(sample_ast_nodes):
    _, function_node = sample_ast_nodes
    for i, child in enumerate(function_node.arguments):
        assert child.position == i


# Test comparison method for AST nodes


@pytest.mark.parametrize("col, row", [("A", 1), ("B", 2)])
def test_cell_content_comparison(col, row):
    cell1 = Cell(col, row, "user1")
    cell2 = Cell(col, row, "user1")
    assert cell1.compare_content(cell2)


@pytest.mark.parametrize("start, end", [(("A", 1), ("B", 2)), (("C", 3), ("D", 4))])
def test_cell_range_content_comparison(start, end):
    range1 = CellRange(
        Cell(start[0], start[1], "user1"), Cell(end[0], end[1], "user1"), "user1"
    )
    range2 = CellRange(
        Cell(start[0], start[1], "user2"), Cell(end[0], end[1], "user2"), "user2"
    )
    assert range1.compare_content(range2)


def test_name_content_comparison():
    name1 = Name("MyRange", "user1")
    name2 = Name("MyRange", "user1")
    assert name1.compare_content(name2)


def test_function_content_comparison():
    func1 = Function("SUM", [Number(1, "user1"), Number(2, "user1")], "user1")
    func2 = Function("SUM", [Number(1, "user1"), Number(2, "user1")], "user1")
    assert func1.compare_content(func2)


def test_number_content_comparison():
    number1 = Number(5, "user1")
    number2 = Number(5, "user1")
    assert number1.compare_content(number2)


def test_logical_content_comparison():
    logical1 = Logical(True, "user1")
    logical2 = Logical(True, "user1")
    assert logical1.compare_content(logical2)


def test_binary_content_comparison():
    binary1 = Binary(Number(1, "user1"), "+", Number(2, "user1"), "user1")
    binary2 = Binary(Number(1, "user1"), "+", Number(2, "user1"), "user1")
    assert binary1.compare_content(binary2)


def test_unary_content_comparison():
    unary1 = Unary("-", Number(1, "user1"), "user1")
    unary2 = Unary("-", Number(1, "user1"), "user1")
    assert unary1.compare_content(unary2)
