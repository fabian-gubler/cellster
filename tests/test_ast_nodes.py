# test_ast_nodes.py
import pytest
from parser.ast_nodes import BaseNode, Function, Number

@pytest.fixture
def sample_ast_nodes():
    number_node = Number(5, "user1")
    function_node = Function("SUM", [number_node], "user1")
    return number_node, function_node

def test_node_parent_reference(sample_ast_nodes):
    number_node, function_node = sample_ast_nodes
    assert number_node.parent == function_node

def test_node_type_information(sample_ast_nodes):
    number_node, _ = sample_ast_nodes
    assert number_node.node_type == 'Number'
#
def test_content_comparison_method(sample_ast_nodes):
    number_node, _ = sample_ast_nodes
    another_number_node = Number(5, "user1")
    assert number_node.compare_content(another_number_node)
#
def test_node_position_information(sample_ast_nodes):
    _, function_node = sample_ast_nodes
    for i, child in enumerate(function_node.arguments):
        assert child.position == i
