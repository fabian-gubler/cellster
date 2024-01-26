from copy import deepcopy
from parser.parser import parse

import pytest  # pyright: ignore # noqa F401

from crdt.ast_manager import ASTManager

###################
# Helper function #
###################


def process_and_merge_asts(original_ast_str, user1_ast_str, user2_ast_str):
    # Parse the original AST once, important for id_history
    original_ast = parse(original_ast_str)

    # Initialize AST managers with deep copies of the original AST
    user1_ast_manager = ASTManager(deepcopy(original_ast))
    user2_ast_manager = ASTManager(deepcopy(original_ast))

    # Create changes
    user1_changes = user1_ast_manager.get_changes_to(user1_ast_str)
    user2_changes = user2_ast_manager.get_changes_to(user2_ast_str)

    # Apply changes
    user1_ast_manager.apply_changes(user1_changes, user_id="user_1")
    user2_ast_manager.apply_changes(user2_changes, user_id="user_2")

    # Merge changes
    user1_merged_changes = user1_ast_manager.merge_changes(user2_changes)
    user2_merged_changes = user2_ast_manager.merge_changes(user1_changes)

    # Apply merged changes
    user1_ast_manager.apply_changes(user1_merged_changes, user_id="user_1")
    user2_ast_manager.apply_changes(user2_merged_changes, user_id="user_2")

    return str(user1_ast_manager), str(user2_ast_manager)


######################
# Modification tests #
######################


def test_function_modification():
    original_ast_str = "SUM(A1)"
    user1_ast_str = "AVERAGE(A1)"
    user2_ast_str = "SUM(A1)"
    expected_output = "AVERAGE(A1)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


def test_rule_based_modification():
    original_ast_str = "SUM(A2:A8)"
    user1_ast_str = "SUM(A3:A10)"
    user2_ast_str = "SUM(A1:A8)"

    expected_output = "SUM(A1:A10)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


def test_function_outer_inner():
    original_ast_str = "SUM(A2:A9)"
    user1_ast_str = "AVERAGE(A2:A9)"
    user2_ast_str = "SUM(A1:A10)"

    expected_output = "AVERAGE(A1:A10)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output

#############################
# Conflict Resolution Tests #
#############################

def test_conflict_resolution_simple():
    original_ast_str = "A1"
    user1_ast_str = "A2"
    user2_ast_str = "A3"

    expected_output = "A3"  

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


def test_conflict_resolution_complex():
    original_ast_str = "SUM(A1) + A3"
    user1_ast_str = "SUM(A2) + A4"
    user2_ast_str = "AVERAGE(A1) + A5"

    expected_output = "AVERAGE(A2) + A5"  

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output

############################
# IMP Presentation example #
############################


def test_presentation_example():
    original_ast_str = "SUM(A2:A9)"
    user1_ast_str = "SUM(A3:A10)"
    user2_ast_str = "SUM(A2:A9) / B5"

    expected_output = "SUM(A3:A10) / B5"  # Caveat: A2 min not submited change

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


#
#
# ##########################
# # ADD FUNCTION ARGUMENTS #
# ##########################


def test_function_change_add_args():
    original_ast_str = "SUM(A2:A9)"
    user1_ast_str = "SUM(A2:A9, 5)"
    user2_ast_str = "SUM(A1:A10)"

    expected_output = "SUM(A1:A10, 5)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


# Note: A solution to this problem is to use the 'rule based' approach
# Time-based approach commented in add_child function

# def test_function_two_add_args():
#     original_ast_str = "SUM(A1:A10)"
#     user1_ast_str = "SUM(A1:A10, 5)"
#     user2_ast_str = "SUM(A1:A10, 7)"
#
#     expected_output = (
#         "SUM(A1:A10, 5, 7)"
#     )
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str,
#         user1_ast_str,
#         user2_ast_str,
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


# #############################
# # DELETE FUNCTION ARGUMENTS #
# #############################


def test_integration_remove_argument_simple_function():
    original_ast_str = "SUM(A1:A10, B1:B10)"
    user1_ast_str = "SUM(A1:A10)"
    user2_ast_str = "SUM(A1:A10, B1:B10, C1:C10)"

    expected_output = "SUM(A1:A10, C1:C10)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


def test_integration_remove_argument_nested_function():
    original_ast_str = "SUM(AVERAGE(A1:A10), B1)"
    user1_ast_str = "SUM(AVERAGE(A1:A10))"
    user2_ast_str = "SUM(AVERAGE(A1:A10), B1, C1)"

    expected_output = "SUM(AVERAGE(A1:A10), C1)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


def test_integration_remove_multiple_arguments():
    original_ast_str = "SUM(A1:A10, B1, C1:C10)"
    user1_ast_str = "SUM(A1:A10)"
    user2_ast_str = "SUM(A1:A10, D1:D10)"

    expected_output = "SUM(A1:A10, D1:D10)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
    )

    assert user1_merged_ast_str == expected_output
    assert user2_merged_ast_str == expected_output


# #####################
# # CHANGE TYPE TESTS #
# #####################
#
#
def test_change_cell_to_range_in_function():
    original_ast_str = "SUM(A1)"
    user1_ast_str = "SUM(A1)"
    user2_ast_str = "SUM(A1:B1)"

    expected_output = "SUM(A1:B1)"

    user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
        original_ast_str,
        user1_ast_str,
        user2_ast_str,
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
#         original_ast_str,
#         user1_ast_str,
#         user2_ast_str,
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output

# TODO: Key error parent

# def test_add_outer_function_integration():
#     original_ast_str_str = "A1"
#     user1_ast_str = "SUM(A1)"
#     user2_ast_str = "AVERAGE(A1)"
#
#     expected_output = "SUM(AVERAGE(A1))"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str_str,
#         user1_ast_str,
#         user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


# TODO: Key error parent

# def test_unary_left_addition_integration():
#     original_ast_str_str = "A1"
#     user1_ast_str = "-A1"
#     user2_ast_str = "+A1"
#
#     expected_output = "-(+A1)"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str_str, user1_ast_str, user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


######################
# ROOT LEVEL Deletions
######################

# TODO: Remove of type NONE

# def test_delete_root_function_integration():
#     original_ast_str_str = "SUM(A1)"
#     user1_ast_str = "A1"
#     user2_ast_str = "SUM(A1 * 2)"
#
#     expected_output = "A1 * 2"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str_str,
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
#     original_ast_str_str = "SUM(A1:A10) + 1"
#     user1_ast_str = "SUM(A1:A10)"
#     user2_ast_str = "SUM(A1:A10) - 1"
#
#     expected_output = "SUM(A1:A10) - 1"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str_str,
#         user1_ast_str,
#         user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


# TODO: First delete then add

# def test_change_cell_to_number():
#     original_ast_str_str = "A1 + 5"
#     user1_ast_str = "10 + 5"
#     user2_ast_str = "A1 + 10"
#
#     expected_output = "10 + 10"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str_str, user1_ast_str, user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output


################
# NEEDS FIXING #
################


# TODO: Cannot add to a deleted node

# def test_root_type_modification():
#     original_ast_str_str = "A1"
#     user1_ast_str = "A1:A10"
#     user2_ast_str = "SUM(A1)"
#
#     expected_output = "SUM(A1:A10)"
#
#     user1_merged_ast_str, user2_merged_ast_str = process_and_merge_asts(
#         original_ast_str_str, user1_ast_str, user2_ast_str
#     )
#
#     assert user1_merged_ast_str == expected_output
#     assert user2_merged_ast_str == expected_output
