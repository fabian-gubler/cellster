import pytest
from tests.integration.test_utils import process_and_merge_asts


def test_equal_asts():
    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        "SUM(A1:A10)",
        "SUM(A1:A10)",
        "SUM(A1:A10)",
        debug_changes=True,
        debug_new_asts=True,
        debug_merged_asts=True,
    )

    assert user1_merged_ast_str == "SUM(A1:A10)"
    assert user2_merged_ast_str == "SUM(A1:A10)"


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
# def test_non_conflicting_modifications():
#     original_ast = parse("SUM(A1:A10) + AVERAGE(B1:B10)")
#     user1_ast = parse("SUM(A1:A9) + AVERAGE(B1:B10)")
#     user2_ast = parse("SUM(A1:A10) + AVERAGE(B2:B10)")
#
#     user1_changes = compare_asts(original_ast, user1_ast)
#     user2_changes = compare_asts(original_ast, user2_ast)
#
#     merged_changes = merge_changes(user1_changes, user2_changes)
#     merged_ast = apply_changes_to_ast(original_ast, merged_changes)
#
#     print("merged_ast: ", merged_ast)
#     assert str(merged_ast) == "(SUM(A1:A9) + AVERAGE(B2:B10))"


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
