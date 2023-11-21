import pytest
from crdt.formula_parser_wrapper import FormulaParserWrapper

class TestFormulaParserWrapper:
    @pytest.fixture
    def parser(self):
        return FormulaParserWrapper()

    def test_parsing_valid_formula(self, parser):
        formula = "SUM(A1:A3)"
        ast = parser.parse_formula(formula)
        assert ast is not None, "AST should be created for a valid formula"

    def test_parsing_invalid_formula(self, parser):
        formula = "SUM(A1:A3"
        with pytest.raises(Exception):
            parser.parse_formula(formula)

    def test_ast_equality_for_same_formulas(self, parser):
        formula1 = "SUM(A1:A3)"
        formula2 = "SUM(A1:A3)"
        ast1 = parser.parse_formula(formula1)
        ast2 = parser.parse_formula(formula2)

        assert ast1.is_equal_to(ast2), "ASTs should be equal for the same formula"

    def test_ast_equality_for_different_formulas(self, parser):
        formula1 = "SUM(A1:A3)"
        formula2 = "SUM(B1:B3)"
        ast1 = parser.parse_formula(formula1)
        ast2 = parser.parse_formula(formula2)
        assert not ast1.is_equal_to(ast2), "ASTs should not be equal for different formulas"
