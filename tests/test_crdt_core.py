import pytest
from crdt.crdt_core import CRDTCore
from crdt.formula_parser_wrapper import FormulaParserWrapper


@pytest.fixture
def crdt_core():
    return CRDTCore()


def create_test_ast(formula, user_id):
    # Parse the formula
    parser = FormulaParserWrapper()
    ast = parser.parse_formula(formula)

    return ast

def test_basic_merging_same_as_original(crdt_core):
    # Original and modified formulas are the same
    original_formula = "SUM(A1:A10)"
    modified_formula_user1 = "SUM(A1:A10)"  # User 1's modification
    modified_formula_user2 = "SUM(A1:A10)"  # User 2's modification

    # Parse the formulas into ASTs
    ast_original = create_test_ast(original_formula, user_id="user_original")
    ast_modified_1 = create_test_ast(modified_formula_user1, user_id="user1")
    ast_modified_2 = create_test_ast(modified_formula_user2, user_id="user2")

    # Merge the ASTs using CRDT core logic
    merged_ast = crdt_core.merge_asts(ast_original, ast_modified_1, ast_modified_2)

    # Assert that the merged result is the same as the original
    assert merged_ast.is_equal_to(ast_original), "Merged AST should be same as the original when no actual changes are made"

def test_basic_merging_same_changes(crdt_core):
    # Original formula and the modifications made by both users are the same
    original_formula = "SUM(A1:A10)"
    modified_formula = "SUM(A1:A5)"  # Identical modification by both users

    # Parse the formulas into ASTs
    ast_original = create_test_ast(original_formula, "user_original")
    ast_modified_user1 = create_test_ast(modified_formula, "user1")
    ast_modified_user2 = create_test_ast(modified_formula, "user2")

    # Merge the ASTs using CRDT core logic
    merged_ast = crdt_core.merge_asts(ast_original, ast_modified_user1, ast_modified_user2)

    # Assert that the merged result is the same as the modified ASTs
    # assert merged_ast == ast_modified_user1, "Merged AST should reflect the identical changes made by both users"
    assert  merged_ast.is_equal_to(ast_modified_user1), "Merged AST should reflect the identical changes made by both users"

def test_outer_function_change_by_one_user(crdt_core):
    original_ast = create_test_ast("SUM(A1:A10)", "user_original")
    modified_ast1 = create_test_ast("SUM(A1:A10)", "user1")  # No change by user 1
    modified_ast2 = create_test_ast("MIN(A1:A10)", "user2")  # Change by user 2

    merged_ast = crdt_core.merge_asts(original_ast, modified_ast1, modified_ast2)
    assert merged_ast.is_equal_to(modified_ast2), "Merged AST should reflect the outer function change by user 2"


def test_conflicting_outer_function_changes(crdt_core):
    original_ast = create_test_ast("SUM(A1:A10)", "user_original")
    modified_ast1 = create_test_ast("MIN(A1:A10)", "user1")
    modified_ast2 = create_test_ast("MAX(A1:A10)", "user2")  # Later change by user 2

    merged_ast = crdt_core.merge_asts(original_ast, modified_ast1, modified_ast2)
    assert merged_ast.is_equal_to(modified_ast2), "Merged AST should reflect the later outer function change by user 2"


def test_inner_function_change_by_one_user(crdt_core):
    original_ast = create_test_ast("SUM(A1:A10)", "user_original")
    modified_ast1 = create_test_ast("SUM(A1:A10)", "user1") # No change by user 1
    modified_ast2 = create_test_ast("SUM(A1:A20)", "user2")  # Change by user 2

    merged_ast = crdt_core.merge_asts(original_ast, modified_ast1, modified_ast2)
    assert merged_ast.is_equal_to(modified_ast2), "Merged AST should reflect the inner function change by user 2"


def test_conflicting_inner_function_changes(crdt_core):
    original_ast = create_test_ast("SUM(A1:A10)", "user_original")
    modified_ast1 = create_test_ast("SUM(A2:A10)", "user1")
    modified_ast2 = create_test_ast("SUM(A3:A10)", "user2")  # Later change by user 2

    merged_ast = crdt_core.merge_asts(original_ast, modified_ast1, modified_ast2)
    assert merged_ast.is_equal_to(modified_ast2), "Merged AST should reflect the later inner function change by user 2"

def test_node_addition(crdt_core):
    # Define and parse formulas with additional nodes
    # Add metadata with timestamps
    # Call crdt_core.merge_asts and assert the result
    pass

