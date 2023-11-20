import pytest
from datetime import datetime
from crdt.metadata_management import MetadataManager
from parser.formula_parser import parse, FormulaParseError

@pytest.fixture

# TODO: Replace with formula parser wrapper

def metadata_manager():
    return MetadataManager()

def test_add_metadata(metadata_manager):
    # Create a sample AST node

    formula = "SUM(A1:A10)"
    ast = parse(formula)

    user_id = "user123"
    timestamp_before = datetime.now()

    # Call add_metadata
    metadata_manager.add_metadata(ast, user_id)

    timestamp_after = datetime.now()

    # Assert that metadata is added correctly
    assert hasattr(ast, "metadata"), "Metadata attribute should be added to the node"
    assert "user_id" in ast.metadata, "User ID should be part of metadata"
    assert ast.metadata["user_id"] == user_id, "User ID should match the passed value"
    assert "timestamp" in ast.metadata, "Timestamp should be part of metadata"
    assert timestamp_before <= ast.metadata["timestamp"] <= timestamp_after, "Timestamp should be within the expected range"
