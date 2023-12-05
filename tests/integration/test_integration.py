import pytest
from tests.integration.test_utils import process_and_merge_asts


def test_cell_range_modification():

    original_ast = "SUM(A1:A10)"
    user1_ast_str = "SUM(A1:A10)"
    user2_ast_str = "SUM(A2:A9)"

    expected_output = "SUM(A2:A9)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast,
        user1_ast_str,
        user2_ast_str,
        debug_changes=False,
        debug_new_asts=False,
        debug_merged_asts=False,
        debug_all=False,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output

def test_function_modification():

    original_ast = "SUM(A1:A10)"
    user1_ast_str = "AVERAGE(A1:A10)"
    user2_ast_str = "SUM(A1:A10)"

    expected_output = "AVERAGE(A1:A10)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast,
        user1_ast_str,
        user2_ast_str,
        debug_changes=False,
        debug_new_asts=False,
        debug_merged_asts=False,
        debug_all=False,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output

def test_function_outer_inner():

    original_ast = "SUM(A1:A10)"
    user1_ast_str = "AVERAGE(A1:A10)"
    user2_ast_str = "SUM(A2:A9)"

    expected_output = "AVERAGE(A2:A9)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast,
        user1_ast_str,
        user2_ast_str,
        debug_changes=False,
        debug_new_asts=False,
        debug_merged_asts=False,
        debug_all=False,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output

def test_multiple_non_conflicting_modifications():
    original_ast = "SUM(A1:A10) + AVERAGE(B1:B10)"
    user1_ast_str = "SUM(A1:A9) + AVERAGE(B1:B10)"
    user2_ast_str = "SUM(A1:A10) + AVERAGE(B2:B10)"

    expected_output = "SUM(A1:A9) + AVERAGE(B2:B10)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast,
        user1_ast_str,
        user2_ast_str,
        debug_changes=False,
        debug_new_asts=False,
        debug_merged_asts=False,
        debug_all=True,
    )
#
    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output

def test_conflicting_modification():

    original_ast = "SUM(A1:A10)"
    user1_ast_str = "AVERAGE(A2:A10)"
    user2_ast_str = "SUM(A1:A8)"

    expected_output = "AVERAGE(A1:A10)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast,
        user1_ast_str,
        user2_ast_str,
        debug_changes=False,
        debug_new_asts=False,
        debug_merged_asts=False,
        debug_all=True,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output

# def test_apply_additions():
#
#     original_ast = "SUM(A1:A10)"
#     user1_ast_str = "SUM(A1:A10, 5)"
#     user2_ast_str = "SUM(A1:A10)"
#
#     expected_output = "SUM(A1:A10, 5)"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast,
#         user1_ast_str,
#         user2_ast_str,
#         debug_changes=False,
#         debug_new_asts=False,
#         debug_merged_asts=False,
#         debug_all=True,
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


# def test_apply_deletions():
#     original_ast = "SUM(A1:A10, 5)"
#     user1_ast_str = "SUM(A1:A10, 5)"
#     user2_ast_str = "SUM(A1:A10)"
#
#     expected_output = "SUM(A1:A10)"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast,
#         user1_ast_str,
#         user2_ast_str,
#         debug_changes=False,
#         debug_new_asts=False,
#         debug_merged_asts=False,
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output

# def test_apply_complex_modifications():
#     original_ast = parse("SUM(A1:A10, 5)")
#     modified_ast = parse("SUM(A2:A9, 6)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "SUM(A2:A9, 6)"
#
#
# def test_nested_modification():
#     original_ast = parse("SUM(AVERAGE(A1:A5), A10)")
#     modified_ast = parse("SUM(AVERAGE(A1:A6), A10)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "SUM(AVERAGE(A1:A6), A10)"
#
#
# def test_apply_structural_changes():
#     original_ast = parse("SUM(A1:A10)")
#     modified_ast = parse("AVERAGE(A1:A10)")
#     changes = compare_asts(original_ast, modified_ast)
#     new_ast = apply_changes_to_ast(original_ast, changes)
#     assert str(new_ast) == "AVERAGE(A1:A10)"

# def test_conflicting_modifications():
#     original_ast = parse("SUM(A1:A10)")
#     user1_ast = parse("SUM(A1:A9)")
#     user2_ast = parse("SUM(A2:A10)")
#
#     print("User 1 Changes:")
#     user1_changes = compare_asts(original_ast, user1_ast)
#
#     print("User 2 Changes:")
#     user2_changes = compare_asts(original_ast, user2_ast)
#
#     merged_changes = merge_changes(user1_changes, user2_changes)
#     merged_ast = apply_changes_to_ast(original_ast, merged_changes)
#
#     print("merged_ast: ", merged_ast)  # outputs SUM(A1:A10)
#
#     assert str(merged_ast) == "SUM(A2:A9)"
#     # Assert based on the conflict resolution strategy implemented
#
#


# def test_non_conflicting_changes_outer():
#     original_ast = parse("SUM(A1:A10)")
#     user1_ast = parse("SUM(A1:A10)")  # User 1 makes a change
#     user2_ast = parse("SUM(A1:A10, 5)")  # User 2 makes a different change
#
#     user1_changes = compare_asts(original_ast, user1_ast)
#     user2_changes = compare_asts(original_ast, user2_ast)
#
#     # Merge changes and apply to original AST
#     merged_changes = merge_changes(
#         user1_changes, user2_changes
#     )  # Function to be implemented
#     merged_ast = apply_changes_to_ast(original_ast, merged_changes)
#
#     assert str(merged_ast) == "SUM(A1:A10, 5)"  # Combined changes from both users
#
#
#
# def test_mixed_changes():
#     original_ast = parse("SUM(A1:A10)")
#     user1_ast = parse("SUM(A1:A9)")
#     user2_ast = parse("SUM(A2:A10, 5)")
#
#     user1_changes = compare_asts(original_ast, user1_ast)
#     user2_changes = compare_asts(original_ast, user2_ast)
#
#     merged_changes = merge_change_sets(user1_changes, user2_changes)
#     merged_ast = apply_changes_to_ast(original_ast, merged_changes)
#
#     assert str(merged_ast) == "SUM(A1:A9, 5)"
#
