import pytest  # pyright: ignore # noqa F401

from utils.test_utils import process_and_merge_asts


def test_rule_based_modification():
    original_ast = "SUM(A2:A8)"
    user1_ast_str = "SUM(A3:A10)"
    user2_ast_str = "SUM(A1:A8)"

    expected_output = "SUM(A1:A10)"

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
    original_ast = "SUM(A2:A9)"
    user1_ast_str = "AVERAGE(A2:A9)"
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


def test_function_change_add_args():
    original_ast = "SUM(A2:A9)"
    user1_ast_str = "SUM(A2:A9, 5)"
    user2_ast_str = "SUM(A1:A10)"

    expected_output = "SUM(A1:A10, 5)"

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


def test_function_two_add_args():
    original_ast = "SUM(A1:A10)"
    user1_ast_str = "SUM(A1:A10, 5)"
    user2_ast_str = "SUM(A1:A10, 5)"

    expected_output = (
        "SUM(A1:A10, 5, 5)"  # TODO: rule-based range approach (order matters)
    )

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


# def test_function_nested_outer_inner():
#     original_ast = "SUM(A1:A10)"
#     user1_ast_str = "SUM(A1:A11)"
#     user2_ast_str = "SUM(Average(A1:A10))"
#
#     expected_output = "SUM(AVERAGE(A1:A10))"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast,
#         user1_ast_str,
#         user2_ast_str,
#         debug_changes=False,
#         debug_new_asts=False,
#         debug_merged_asts=False,
#         debug_all=False,
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output

# def test_conflicting_modification():
#
#     original_ast = "A1 + A2"
#     user1_ast_str = "A1 + A3" # commited earlier (winner)
#     user2_ast_str = "A1 + A4"
#
#     expected_output = "A1 + A3"
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
