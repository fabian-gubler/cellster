from parser.formula_parser import parse, FormulaParseError


class FormulaParserWrapper:
    def parse_formula(self, formula):
        try:
            return parse(formula)
        except FormulaParseError as error:
            # Handle the exception or re-raise with additional context
            raise Exception(f"Error parsing formula: {error}")
