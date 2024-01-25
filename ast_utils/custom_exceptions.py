# custom_exceptions.py

"""
Define and reuse custom exceptions
"""

class NodeNotFoundError(Exception):
    """Exception raised when a node is not found in the AST."""
    def __init__(self, message: str = "Node not found"):
        self.message = message
        super().__init__(self.message)
