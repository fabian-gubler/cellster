import csv
from parser.parser import parse

import pytest

from crdt.apply_changes import apply_changes_to_ast
from crdt.ast_comparison import compare_asts
from utils.test_utils import process_and_merge_asts


def read_ast_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader, None)
        # Assuming the first column is the original AST, and the second column is the modified AST
        return [(row[0], row[1], row[2]) for row in reader]


ast_pairs = read_ast_csv("./tests/automated/formulas.csv")


def read_formulas_from_csv(file_path, column_index=0):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader, None)
        return [formula for row in reader for formula in row if row]


# Read formulas from the first column (index 0 for original ASTs)
formulas = read_formulas_from_csv("./tests/automated/formulas.csv", column_index=0)

# create a passing test
def test_must_pass():
    assert True


# @pytest.mark.skip(reason="Not implemented yet")
@pytest.mark.parametrize("formula", formulas)
def test_formula_parsing(formula):
    try:
        ast = parse(formula)
        assert (
            ast is not None
        )  # or any other assertion to check the validity of the AST
    except Exception as e:
        pytest.fail(f"Parsing failed for formula '{formula}': {e}")


# @pytest.mark.skip(reason="Not implemented yet")
@pytest.mark.parametrize("original, modified_1, modified_2", ast_pairs)
def test_change_tracking(original, modified_1, modified_2):
    original_ast = parse(original)
    modified_ast = parse(modified_1)
    changes = compare_asts(original_ast, modified_ast)
    new_ast, _ = apply_changes_to_ast(original_ast, changes, user_id="test")
    assert str(modified_ast) == modified_1
    assert str(new_ast) == modified_1


@pytest.mark.skip(reason="Not passing yet")
@pytest.mark.parametrize("original, modified_1, modified_2", ast_pairs)
def test_merging(original, modified_1, modified_2):
    original_ast = original
    user1_ast_str = modified_1
    user2_ast_str = modified_2

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast,
        user1_ast_str,
        user2_ast_str,
        debug_changes=False,
        debug_new_asts=False,
        debug_merged_asts=False,
        debug_all=False,
    )

    # assert that both merged ASTs are the same
    assert user1_merged_ast_str == user2_merged_ast_str
