import pytest
from crdt.ast_modification import ASTModificationTracker
from crdt.crdt_core import CRDTCore
from crdt.formula_parser_wrapper import FormulaParserWrapper

@pytest.fixture
def setup_ast_modification():
    parser = FormulaParserWrapper()
    tracker = ASTModificationTracker()
    crdt_core = CRDTCore()
    return parser, tracker, crdt_core

def test_formula_modification(setup_ast_modification):
    parser, tracker, crdt_core = setup_ast_modification

    # Initial formula
    original_formula = "SUM(A1:A10)"
    ast_original = parser.parse_formula(original_formula)

    # User one modification
    formula_user_one = "SUM(A1:A08)"
    ast_user_one = parser.parse_formula(formula_user_one)

    # User two modification
    formula_user_two = "SUM(A1:A10) + 5"
    ast_user_two = parser.parse_formula(formula_user_two)

    # Track and merge changes
    tracker.track_changes(ast_original, ast_user_one)
    tracker.track_changes(ast_original, ast_user_two)
    merged_ast = crdt_core.merge_asts(ast_user_one, ast_user_two)

    # Convert merged AST to formula string and assert
    merged_formula = merged_ast_to_formula(merged_ast)  # This requires an implementation
    assert merged_formula == "SUM(A1:A08) + 5"
