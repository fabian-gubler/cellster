import pytest  # pyright: ignore # noqa F401

from tests.utils.test_utils import process_and_merge_asts

######################
# Modification tests #
######################


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


##########################
# ADD FUNCTION ARGUMENTS #
##########################


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


#############################
# DELETE FUNCTION ARGUMENTS #
#############################


def test_integration_remove_argument_simple_function():
    original_ast = "SUM(A1:A10, B1:B10)"
    user1_ast_str = "SUM(A1:A10)"
    user2_ast_str = "SUM(A1:A10, B1:B10, C1:C10)"

    expected_output = "SUM(A1:A10, C1:C10)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


def test_integration_remove_argument_nested_function():
    original_ast = "SUM(AVERAGE(A1:A10), B1)"
    user1_ast_str = "SUM(AVERAGE(A1:A10))"
    user2_ast_str = "SUM(AVERAGE(A1:A10), B1, C1)"

    expected_output = "SUM(AVERAGE(A1:A10), C1)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


def test_integration_remove_multiple_arguments():
    original_ast = "SUM(A1:A10, B1, C1:C10)"
    user1_ast_str = "SUM(A1:A10)"
    user2_ast_str = "SUM(A1:A10, D1:D10)"

    expected_output = "SUM(A1:A10, D1:D10)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


#####################
# CHANGE TYPE TESTS #
#####################


def test_change_cell_to_range_in_function():
    original_ast_str = "SUM(A1)"
    user1_ast_str = "SUM(A1)"
    user2_ast_str = "SUM(A1:B1)"

    expected_output = "SUM(A1:B1)"  # NOTE: if both cell-range then two arguments

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str, user1_ast_str, user2_ast_str
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


######################
# ROOT LEVEL ADDITIONS
######################

# TODO: Binary already has two children

# def test_binary_right_addition_integration():
#     original_ast_str = "A1 + A2"
#     user1_ast_str = "A1 + A2 + A3"
#     user2_ast_str = "A1 + A2 - A4"
#
#     expected_output = "A1 + A2 + A3 - A4"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str, user1_ast_str, user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output

# TODO: Key error parent

# def test_add_outer_function_integration():
#     original_ast_str = "A1"
#     user1_ast_str = "SUM(A1)"
#     user2_ast_str = "AVERAGE(A1)"
#
#     expected_output = "SUM(AVERAGE(A1))"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str,
#         user1_ast_str,
#         user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


# TODO: Key error parent

# def test_unary_left_addition_integration():
#     original_ast_str = "A1"
#     user1_ast_str = "-A1"
#     user2_ast_str = "+A1"
#
#     expected_output = "-(+A1)"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str, user1_ast_str, user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


######################
# ROOT LEVEL Deletions
######################

# TODO: Remove of type NONE

# def test_delete_root_function_integration():
#     original_ast_str = "SUM(A1)"
#     user1_ast_str = "A1"
#     user2_ast_str = "SUM(A1 * 2)"
#
#     expected_output = "A1 * 2"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str,
#         user1_ast_str,
#         user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


#####################
# ORDER MATTERS #
#####################

# TODO: Original node not found

# def test_delete_root_binary_integration():
#     original_ast_str = "SUM(A1:A10) + 1"
#     user1_ast_str = "SUM(A1:A10)"
#     user2_ast_str = "SUM(A1:A10) - 1"
#
#     expected_output = "SUM(A1:A10) - 1"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str,
#         user1_ast_str,
#         user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


# TODO: First delete then add

# def test_change_cell_to_number():
#     original_ast_str = "A1 + 5"
#     user1_ast_str = "10 + 5"
#     user2_ast_str = "A1 + 10"
#
#     expected_output = "10 + 10"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str, user1_ast_str, user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


################
# NEEDS FIXING #
################


# TODO: Cannot add to a deleted node

# def test_root_type_modification():
#     original_ast_str = "A1"
#     user1_ast_str = "A1:A10"
#     user2_ast_str = "SUM(A1)"
#
#     expected_output = "SUM(A1:A10)"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str, user1_ast_str, user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output
