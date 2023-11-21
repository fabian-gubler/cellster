import pytest
from utils.ast_comparison import compare_ast_nodes
from parser.formula_parser import Cell, Number, Logical, Binary, Unary, Function, CellRange

class TestASTComparison:
    def test_compare_simple_nodes(self):
        assert compare_ast_nodes(Number(5), Number(5)), "Same numbers should be equal"
        assert not compare_ast_nodes(Number(5), Number(10)), "Different numbers should not be equal"

    def test_compare_cell_range_nodes(self):
        range1 = CellRange(Cell('A', 1), Cell('A', 10))
        range2 = CellRange(Cell('A', 1), Cell('A', 10))
        range3 = CellRange(Cell('A', 1), Cell('B', 10))
        assert compare_ast_nodes(range1, range2), "Identical ranges should be equal"
        assert not compare_ast_nodes(range1, range3), "Different ranges should not be equal"

    def test_compare_function_nodes(self):
        func1 = Function("SUM", [Number(1), Number(2)])
        func2 = Function("SUM", [Number(1), Number(2)])
        func3 = Function("SUM", [Number(3), Number(4)])
        func4 = Function("AVERAGE", [Number(1), Number(2)])
        assert compare_ast_nodes(func1, func2), "Identical functions should be equal"
        assert not compare_ast_nodes(func1, func3), "Functions with different arguments should not be equal"
        assert not compare_ast_nodes(func1, func4), "Functions with different names should not be equal"

    def test_compare_binary_nodes(self):
        binary1 = Binary(Number(1), "+", Number(2))
        binary2 = Binary(Number(1), "+", Number(2))
        binary3 = Binary(Number(1), "-", Number(2))
        assert compare_ast_nodes(binary1, binary2), "Identical binary nodes should be equal"
        assert not compare_ast_nodes(binary1, binary3), "Binary nodes with different operators should not be equal"

    def test_compare_unary_nodes(self):
        unary1 = Unary("-", Number(5))
        unary2 = Unary("-", Number(5))
        unary3 = Unary("+", Number(5))
        assert compare_ast_nodes(unary1, unary2), "Identical unary nodes should be equal"
        assert not compare_ast_nodes(unary1, unary3), "Unary nodes with different operators should not be equal"
