# test_parser.py
import pytest
from parser.formula_parser import parse, FormulaParseError


def test_parse_valid_formula():
    # Test parsing a valid formula
    formula1 = "SUM(A1:A10)"

    # Test parsing a complex formula
    formula2 = "HELLO(SUM(A1:A3), 1+2*3-ABS(B14-MY_FUNC(C67)), IF(true, false, -10e-5))"
    ast1 = parse(formula1)
    ast2 = parse(formula2)

    # TODO: Validate the structure of the AST
    assert ast1 is not None  # Basic check
    assert ast2 is not None  # Complex check


def test_parse_invalid_formula():
    # Test parsing an invalid formula
    formula = "=SUM("
    with pytest.raises(FormulaParseError):
        parse(formula)
