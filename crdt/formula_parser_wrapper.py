from parser.formula_parser import parse, FormulaParseError
from datetime import datetime
from crdt.custom_ast_node import CustomASTNode

class FormulaParserWrapper:
    def parse_formula(self, formula, user_id=None):
        try:
            ast_node = parse(formula)
            return CustomASTNode(ast_node, user_id)
        except FormulaParseError as error:
            raise Exception(f"Error parsing formula: {error}")

    def reconstruct_formula(self, ast):
        # Recursive function to convert AST back to formula string
        pass
