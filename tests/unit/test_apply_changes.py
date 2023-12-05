import pytest
from parser.parser import parse
from crdt.ast_comparison import compare_asts
from crdt.apply_changes import apply_changes_to_ast, StructuralChangeException


######################
# Modification tests #
######################


def test_apply_modifications():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A9)")
    changes = compare_asts(original_ast, modified_ast)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
    assert str(new_ast) == "SUM(A1:A9)"


def test_apply_complex_modifications():
    original_ast = parse("SUM(A1:A10, 5)")
    modified_ast = parse("SUM(A2:A9, 6)")
    changes = compare_asts(original_ast, modified_ast)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
    assert str(new_ast) == "SUM(A2:A9, 6)"


def test_nested_modification():
    original_ast = parse("SUM(AVERAGE(A1:A5), A10)")
    modified_ast = parse("SUM(AVERAGE(A1:A6), A10)")
    changes = compare_asts(original_ast, modified_ast)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
    assert str(new_ast) == "SUM(AVERAGE(A1:A6), A10)"


def test_apply_structural_changes():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("AVERAGE(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    # print("Changes: ", changes)
    new_ast, new_nodes = apply_changes_to_ast(original_ast, changes)
    # print("New AST: ", new_ast)
    assert str(new_ast) == "AVERAGE(A1:A10)"


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
