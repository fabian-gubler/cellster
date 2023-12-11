from parser.parser import parse

import pytest  # noqa: F401

from crdt.apply_changes import apply_changes_to_ast
from crdt.ast_comparison import compare_asts
from tests.integration.test_utils import print_detected_changes

######################
# Modification tests #
######################


def test_cell_range_modifications():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A9)")
    changes = compare_asts(original_ast, modified_ast)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes, user_id="test")
    assert str(modified_ast) == "SUM(A1:A9)"
    assert str(new_ast) == "SUM(A1:A9)"


def test_function_modifications():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("AVERAGE(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes, user_id="test")
    assert str(new_ast) == "AVERAGE(A1:A10)"


def test_binary_operator_modification():
    original_ast = parse("A1 + A3")
    modified_ast = parse("A1 - A2")
    changes = compare_asts(original_ast, modified_ast)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes, user_id="test")
    assert str(new_ast) == "A1 - A2"


def test_unary_operator_modification():
    original_ast = parse("-A1")
    modified_ast = parse("+A1")
    changes = compare_asts(original_ast, modified_ast)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes, user_id="test")
    assert str(new_ast) == "+A1"


def test_apply_outer_modification():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("AVERAGE(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    print_detected_changes(changes)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes, user_id="test")
    assert str(new_ast) == "AVERAGE(A1:A10)"


def test_function_outer_inner_modification():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("AVERAGE(A2:A9)")
    changes = compare_asts(original_ast, modified_ast)
    print_detected_changes(changes)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes, user_id="test")
    assert str(new_ast) == "AVERAGE(A2:A9)"


def test_function_long_modification():
    original_ast = parse("SUM(A1:A10) + AVERAGE(B1:B10)")
    modified_ast = parse("SUM(A1:A9) + AVERAGE(B2:B9)")
    changes = compare_asts(original_ast, modified_ast)
    # print_detected_changes(changes)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes, user_id="test")
    assert str(new_ast) == "SUM(A1:A9) + AVERAGE(B2:B9)"


####################
# SIMPLE ADDITIONS #
####################

# def test_binary_right_addition():
#     original_ast = parse("A1 + A2")
#     modified_ast = parse("A1 + A2 + A3")
#
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#
#     assert str(new_ast) == "A1 + A2 + A3"

# def test_binary_left_addition():
#     original_ast = parse("A1 + A2")
#     modified_ast = parse("A3 + A1 + A2")
#
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#
#     assert str(new_ast) == "A1 + A2 + A3"


#########################
# COMPLEX MODIFICATIONS #
#########################


# def test_nested_composite_modifications():
#     original_ast = parse("SUM(AVERAGE(A1:A5), A10)")
#     modified_ast = parse("SUM(AVERAGE(A2:A6), A11)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "SUM(AVERAGE(A2:A6), A11)"


# def test_nested_structural_changes():
#     original_ast = parse("SUM(AVERAGE(A1:A5), A10)")
#     modified_ast = parse("AVERAGE(SUM(A1:A5), A10)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "AVERAGE(SUM(A1:A5), A10)"


# def test_mixed_modifications_and_structural_changes():
#     original_ast = parse("SUM(A1:A10, AVERAGE(B1:B5))")
#     modified_ast = parse("SUM(A2:A9, MAX(B2:B6))")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "SUM(A2:A9, MAX(B2:B6))"


# def test_root_level_composite_changes():
#     original_ast = parse("SUM(A1:A10, B1:B10)")
#     modified_ast = parse("SUM(A2:A9, B2:B9)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "SUM(A2:A9, B2:B9)"


#######################
# Addition / Deletion #
#######################


# def test_apply_additions():
#     original_ast = parse("SUM(A1:A10)")
#     modified_ast = parse("SUM(A1:A10, 5)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "SUM(A1:A10, 5)"
#
#
# def test_apply_deletions():
#     original_ast = parse("SUM(A1:A10, 5)")
#     modified_ast = parse("SUM(A1:A10)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "SUM(A1:A10)"


# def test_complex_structural_change():
#     original_ast = parse("SUM(A1:A10)")
#     modified_ast = parse("A1 + A2 + A3 + A4 + A5 + A6 + A7 + A8 + A9 + A10")
#     changes = compare_asts(original_ast, modified_ast)
#     with pytest.raises(StructuralChangeException):
#         new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#     # assert str(new_ast) == "A1 + A2 + A3 + A4 + A5 + A6 + A7 + A8 + A9 + A10"

#
# def test_apply_complex_modifications():
#     original_ast = parse("SUM(A1:A10, 5)")
#     modified_ast = parse("SUM(A2:A9, 6)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "SUM(A2:A9, 6)"
#
#
# def test_nested_modification():
#     original_ast = parse("SUM(AVERAGE(A1:A5), A10)")
#     modified_ast = parse("SUM(AVERAGE(A1:A6), A10)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "SUM(AVERAGE(A1:A6), A10)"

######################
# ROOT LEVEL
######################


# def test_apply_root_additions():
#     original_ast = parse("SUM(A1:A10)")
#     modified_ast = parse("SUM(A1:A10) + 1")
#     changes = compare_asts(original_ast, modified_ast)
#     # assert whether exception is raised
#     with pytest.raises(StructuralChangeException):
#         new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#
#     # assert str(new_ast) == "SUM(A1:A10 + 1)"
#
#
# def test_apply_root_deletions():
#     original_ast = parse("SUM(A1:A10) + 1")
#     modified_ast = parse("SUM(A1:A10)")
#     changes = compare_asts(original_ast, modified_ast)
#     with pytest.raises(StructuralChangeException):
#         new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
#     # assert str(new_ast) == "SUM(A1:A10)"
