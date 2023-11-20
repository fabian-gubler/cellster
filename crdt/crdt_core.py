# crdt_core.py
from .formula_parser_wrapper import FormulaParserWrapper

class CRDTCore:
    def __init__(self):
        self.parser = FormulaParserWrapper()

    def merge_asts(self, formula1, formula2):
        ast1 = self.parser.parse_formula(formula1)
        ast2 = self.parser.parse_formula(formula2)
        # CRDT merging logic goes here
        # ...
