import pytest

from utils.reconstruct_formula import reconstruct_formula
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

def test_reconstruct_simple_number():
    node = Number(42, "user1")
    formula = reconstruct_formula(node)
    assert formula == "42"


def test_reconstruct_function():
    node = Function("SUM", [Number(1, "user1"), Cell("A", 1, "user1")], "user1")
    formula = reconstruct_formula(node)
    assert formula == "SUM(1, A1)"


def test_reconstruct_binary_operation():
    node = Binary(Number(2, "user1"), "+", Number(3, "user1"), "user1")
    formula = reconstruct_formula(node)
    assert formula == "(2 + 3)"
