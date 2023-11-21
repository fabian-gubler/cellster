from crdt.custom_ast_node import CustomASTNode
from parser.formula_parser import Function
from utils.ast_comparison import compare_ast_nodes
from datetime import datetime

# crdt_core.py
class CRDTCore:
    def merge_asts(self, original_ast, modified_ast1, modified_ast2):
        return self.merge_nodes(original_ast, modified_ast1, modified_ast2)

    def merge_nodes(self, original_node, node1, node2):
        # Base case: if both nodes are the same as the original, return the original
        if node1.is_equal_to(original_node) and node2.is_equal_to(original_node):
            return original_node

        # If both nodes are different, resolve using conflict resolution
        if not node1.is_equal_to(original_node) and not node2.is_equal_to(original_node):
            return self.resolve_conflict(node1, node2)

        # If one node is different, return the modified one
        if not node1.is_equal_to(original_node):
            return node1
        if not node2.is_equal_to(original_node):
            return node2

        # Recursively merge child nodes if present
        if isinstance(node1.ast_node, Function):
            merged_arguments = [self.merge_nodes(original_node.ast_node.arguments[i], node1.ast_node.arguments[i], node2.ast_node.arguments[i]) for i in range(len(node1.ast_node.arguments))]
            # Construct a new Function node with merged arguments
            return CustomASTNode(Function(node1.ast_node.func_name, merged_arguments), node1.metadata['user_id'])

        # Add similar logic for other types of nodes like Binary, Unary, etc.
        
        # Default case: if no changes detected, return the original node
        return original_node

    def resolve_conflict(self, node1, node2):
        timestamp1 = node1.metadata.get('timestamp', datetime.min)
        timestamp2 = node2.metadata.get('timestamp', datetime.min)

        # Use timestamp for conflict resolution, with tie-breaking towards the first node
        if timestamp1 > timestamp2:
            return node1
        elif timestamp2 > timestamp1:
            return node2
        else:
            return node1  # Tie-breaking towards the first node
