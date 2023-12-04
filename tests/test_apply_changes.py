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
    new_ast = apply_changes_to_ast(original_ast, changes)
    assert str(new_ast) == "SUM(A1:A9)"


def test_apply_complex_modifications():
    original_ast = parse("SUM(A1:A10, 5)")
    modified_ast = parse("SUM(A2:A9, 6)")
    changes = compare_asts(original_ast, modified_ast)
    new_ast = apply_changes_to_ast(original_ast, changes)
    assert str(new_ast) == "SUM(A2:A9, 6)"


def test_nested_modification():
    original_ast = parse("SUM(AVERAGE(A1:A5), A10)")
    modified_ast = parse("SUM(AVERAGE(A1:A6), A10)")
    changes = compare_asts(original_ast, modified_ast)
    new_ast = apply_changes_to_ast(original_ast, changes)
    assert str(new_ast) == "SUM(AVERAGE(A1:A6), A10)"


# def test_apply_structural_changes():
#     original_ast = parse("SUM(A1:A10)")
#     modified_ast = parse("AVERAGE(A1:A10)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "AVERAGE(A1:A10)"
#
#
# def test_nested_structural_changes():
#     original_ast = "SUM(AVERAGE(A1:A5), A10)"
#     modified_ast = "AVERAGE(SUM(A1:A5), A10)"
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "AVERAGE(SUM(A1:A5), A10)"


#######################
# Addition / Deletion #
#######################


def test_apply_additions():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A10, 5)")
    changes = compare_asts(original_ast, modified_ast)
    new_ast = apply_changes_to_ast(original_ast, changes)
    assert str(new_ast) == "SUM(A1:A10, 5)"


def test_apply_deletions():
    original_ast = parse("SUM(A1:A10, 5)")
    modified_ast = parse("SUM(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    new_ast = apply_changes_to_ast(original_ast, changes)
    assert str(new_ast) == "SUM(A1:A10)"


######################
# ROOT LEVEL
######################


def test_apply_root_additions():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A10) + 1")
    changes = compare_asts(original_ast, modified_ast)
    # assert whether exception is raised
    with pytest.raises(StructuralChangeException):
        new_ast = apply_changes_to_ast(original_ast, changes)

    # assert str(new_ast) == "SUM(A1:A10 + 1)"


def test_apply_root_deletions():
    original_ast = parse("SUM(A1:A10) + 1")
    modified_ast = parse("SUM(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    with pytest.raises(StructuralChangeException):
        new_ast = apply_changes_to_ast(original_ast, changes)
    # assert str(new_ast) == "SUM(A1:A10)"
