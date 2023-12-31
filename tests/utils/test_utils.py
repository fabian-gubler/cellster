from copy import deepcopy
from parser.parser import parse

from ast_processing.apply_changes import apply_changes_to_ast
from ast_processing.compare_asts import compare_asts
from crdt.merge import merge_ast


def process_and_merge_asts(
    original_ast_str,
    user1_ast_str,
    user2_ast_str,
    debug_changes=False,
    debug_new_asts=False,
    debug_merged_asts=False,
    debug_all=False,
):
    if debug_all:
        debug_changes = True
        debug_new_asts = True
        debug_merged_asts = True

    # Parse ASTs
    original_ast = parse(original_ast_str)
    user1_original_ast = deepcopy(original_ast)
    user2_original_ast = deepcopy(original_ast)

    user1_modified_ast = parse(user1_ast_str)
    user2_modified_ast = parse(user2_ast_str)

    # Compare ASTs
    user1_changes = compare_asts(user1_original_ast, user1_modified_ast)
    user2_changes = compare_asts(user2_original_ast, user2_modified_ast)

    # Proceed with the following steps once connection has been established ...

    # Apply changes
    user1_new_ast, user1_new_nodes = apply_changes_to_ast(
        user1_original_ast, user1_changes, user_id="user_1"
    )
    user2_new_ast, user2_new_nodes = apply_changes_to_ast(
        user2_original_ast, user2_changes, user_id="user_2"
    )

    if debug_new_asts:
        print("")
        print("User 1 New AST:", user1_new_ast)
        print("User 2 New AST:", user2_new_ast)

    # Merge changes
    user1_merged_ast = merge_ast(user1_new_ast, user2_new_nodes)
    user2_merged_ast = merge_ast(user2_new_ast, user1_new_nodes)

    if debug_merged_asts:
        print("")
        print("User 1 Merged AST:", user1_merged_ast)
        print("User 2 Merged AST:", user2_merged_ast)

    return str(user1_merged_ast), str(user2_merged_ast)
