from parser.nodes import BaseNode
from parser.parser import parse
from typing import List

from ast_processing.apply_changes import apply_changes_to_ast
from ast_processing.compare_asts import compare_asts
from ast_utils.change_classes import Change
from crdt.merge import merge_changes


class ASTManager:
    def __init__(self, original_ast: BaseNode):
        self.ast = original_ast

    def apply_changes(self, changes: List[Change], user_id: str):
        # empty list
        if not changes:
            return
        apply_changes_to_ast(self.ast, changes, user_id)

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
