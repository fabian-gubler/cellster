# test_ast_comparison.py
import pytest
from parser.parser import parse
from crdt.ast_comparison import compare_asts

def test_no_change():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    assert len(changes) == 0

def test_detect_modifications():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A9)")
    changes = compare_asts(original_ast, modified_ast)
    assert any(change['type'] == 'modification' for change in changes)

def test_detect_additions():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("SUM(A1:A10) + 1")
    changes = compare_asts(original_ast, modified_ast)
    assert any(change['type'] == 'addition' for change in changes)

def test_detect_deletions():
    original_ast = parse("SUM(A1:A10) + 1")
    modified_ast = parse("SUM(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    assert any(change['type'] == 'deletion' for change in changes)

def test_detect_structural_changes():
    original_ast = parse("SUM(A1:A10)")
    modified_ast = parse("AVERAGE(A1:A10)")
    changes = compare_asts(original_ast, modified_ast)
    assert any(change['type'] == 'modification' for change in changes)
