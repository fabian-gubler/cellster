from parser.nodes import BaseNode
from parser.parser import parse
from typing import List

from ast_processing.compare_asts import compare_asts
from ast_utils.change_classes import (
    Change,
    ChildAddition,
    ChildDeletion,
    NodeModification,
    RootAddition,
    RootDeletion,
)
from ast_utils.operations import (
    add_child,
    add_root,
    modify_node,
    remove_child,
    remove_root,
    replace_root_node,
)
from crdt.merge import merge_changes


class ASTManager:
    def __init__(self, original_ast: BaseNode):
        self.ast = original_ast

    def apply_changes(self, changes: List[Change], user_id: str):
        # empty list
        if not changes:
            return

        for change in changes:
            match change:
                case NodeModification():
                    modify_node(change, user_id)

                case ChildAddition():
                    add_child(change, user_id)

                case ChildDeletion():
                    remove_child(change)

                case RootAddition():
                    self.ast = add_root(change, user_id)

                # case RootDeletion():
                #     self.ast = remove_root(original_ast, change, user_id)

                case _:
                    raise Exception("Change type not found")

    def get_changes_to(self, modified_ast_str: str) -> List[Change]:
        modified_ast = parse(modified_ast_str)
        return compare_asts(self.ast, modified_ast)

    def merge_changes(self, other_changes: List[Change]) -> List[Change]:
        if other_changes:
            return merge_changes(self.ast, other_changes)
        else:
            return []

    def __str__(self):
        return str(self.ast)

    def __repr__(self):
        return str(self.ast)
