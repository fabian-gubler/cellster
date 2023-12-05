from parser.parser import parse
from crdt.ast_comparison import compare_asts
from crdt.apply_changes import apply_changes_to_ast
from crdt.merge import merge_ast


def print_detected_changes(changes):
    if not changes:
        print("No changes detected")
    else:
        for change in changes:
            # if empty print no changes
            if change["type"] == "modification":
                print(
                    f"Modification: Original: {change['original']}, Modified: {change['modified']}"
                )
            elif change["type"] == "addition":
                print(f"Addition: {change['node']}")
            elif change["type"] == "deletion":
                print(f"Deletion: {change['node']}")
            elif change["type"] == "root_change":
                print(f"Root Change: {change['node']}")
            elif change["type"] == "root_modification":
                print(f"Root Modification: {change['node']}")


def process_and_merge_asts(
    original_ast_str,
    user1_ast_str,
    user2_ast_str,
    debug_changes=False,
    debug_new_asts=False,
    debug_merged_asts=False,
):
    # Parse ASTs
    original_ast = parse(original_ast_str)
    user1_modified_ast = parse(user1_ast_str)
    user2_modified_ast = parse(user2_ast_str)

    # Compare ASTs
    user1_changes = compare_asts(original_ast, user1_modified_ast)
    user2_changes = compare_asts(original_ast, user2_modified_ast)

    if debug_changes:
        print("")
        print("")
        print("User 1 Changes:")
        print_detected_changes(user1_changes)
        print("")
        print("User 2 Changes:")
        print_detected_changes(user2_changes)

    # Apply changes
    user1_new_ast = apply_changes_to_ast(original_ast, user1_changes)
    user2_new_ast = apply_changes_to_ast(original_ast, user2_changes)

    if debug_new_asts:
        print("")
        print("User 1 New AST:", user1_new_ast)
        print("User 2 New AST:", user2_new_ast)

    # Merge changes
    user1_merged_ast = merge_ast(user1_new_ast, user2_changes)
    user2_merged_ast = merge_ast(user2_new_ast, user1_changes)

    if debug_merged_asts:
        print("")
        print("User 1 Merged AST:", user1_merged_ast)
        print("User 2 Merged AST:", user2_merged_ast)

    return str(user1_merged_ast), str(user2_merged_ast)