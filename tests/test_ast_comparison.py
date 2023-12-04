import pytest
from parser.parser import parse
from crdt.ast_comparison import compare_asts


# Test for no change
def test_no_change():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A10)")
    assert compare_asts(original_ast, modified_ast) == []


# Test for simple modification
def test_simple_modification():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A9)")
    changes = compare_asts(original_ast, modified_ast)
    assert len(changes) == 1
    assert changes[0]["type"] == "modification"


# Test for addition
def test_addition():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A10, A12)")
    changes = compare_asts(original_ast, modified_ast)
    assert any(change["type"] == "addition" for change in changes)


# Test for deletion
def test_deletion():
    original_ast = parse("SUM(A1:A10, A12)")
    modified_ast = parse("SUM(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    assert any(change["type"] == "deletion" for change in changes)


# Test for modifications in nested structures
def test_nested_modification():
    original_ast = parse("SUM(AVERAGE(A1:A5), A10)")
    modified_ast = parse("SUM(AVERAGE(A1:A6), A10)")
    changes = compare_asts(original_ast, modified_ast)
    assert any(change["type"] == "modification" for change in changes)


# Test for root-level modification (change in function)
def test_root_level_modification():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("AVERAGE(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    assert len(changes) == 1
    assert changes[0]['type'] == 'modification'


# Test for root-level addition (adding a unary operation)
def test_root_level_addition():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A10) + 1")
    changes = compare_asts(original_ast, modified_ast)
    assert len(changes) == 2
    assert changes[0]["type"] == "root_change"


# Test for root-level deletion (removing a unary operation)
def test_root_level_deletion():
    original_ast = parse("SUM(A1:A10) + 1")
    modified_ast = parse("SUM(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    assert len(changes) == 1
    assert changes[0]["type"] == "root_change"
