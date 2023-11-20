# test_parser.py
import pytest
from parser.formula_parser import parse, FormulaParseError

def test_parse_valid_formula():
    # Test parsing a valid formula
    formula = "=SUM(A1:A10)"
    ast = parse(formula)
    # TODO: Validate the structure of the AST
    assert ast is not None  # Basic check

def test_parse_invalid_formula():
    # Test parsing an invalid formula
    formula = "=SUM("
    with pytest.raises(FormulaParseError):
        parse(formula)
