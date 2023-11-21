from datetime import datetime
from utils.ast_comparison import compare_ast_nodes

class CustomASTNode:
    def __init__(self, ast_node, user_id=None, timestamp=None):
        self.ast_node = ast_node
        self.metadata = {
            'user_id': user_id,
            'timestamp': timestamp if timestamp is not None else datetime.now()
        }

    def is_equal_to(self, other):
        if not isinstance(other, CustomASTNode):
            return False
        return compare_ast_nodes(self.ast_node, other.ast_node)

    def __getattr__(self, name):
        # Delegate attribute access to the wrapped ast_node
        return getattr(self.ast_node, name)
