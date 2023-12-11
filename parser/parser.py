import re

from parser.ast_nodes import (
    Cell,
    CellRange,
    Name,
    Function,
    Number,
    Logical,
    Binary,
    Unary,
)


def _tokenize(code):
    return (
        code.replace(":", " : ")
        .replace(",", " , ")
        .replace("(", " ( ")
        .replace(")", " ) ")
        .replace("*", " * ")
        .replace("+", " + ")
        .replace("/", " / ")
        .replace("-", " - ")
        .replace("%", " % ")
        .replace("^", " ^ ")
        .replace("=", " = ")
        .replace("<", " < ")
        .replace("e - ", "e-")
        .replace("e + ", "e+")
        .replace("> =", " >= ")
        .replace("< =", " <= ")
        .replace("< >", " <> ")
        .split()
    )


class FormulaParseError(Exception):
    pass


def _parse(tokens):
    # print("In_parse")  # Debugging print

    def _parse_logical():
        if tokens[0].lower() == "true":
            tokens.pop(0)
            return Logical(True, "default_user")
        elif tokens[0].lower() == "false":
            tokens.pop(0)
            return Logical(False, "default_user")

    def _parse_number():
        try:
            number = int(tokens[0])
            tokens.pop(0)
            # print(f"Parsed int: {number}")  # Debugging print
            return Number(number, "default_user")
        except ValueError:
            try:
                number = float(tokens[0])
                tokens.pop(0)
                # print(f"Parsed float: {number}")  # Debugging print
                return Number(number, "default_user")
            except ValueError:
                # print("Failed to parse number")  # Debugging print
                return None

    def _parse_cell():
        cell_regex = "^([a-zA-Z]+)([0-9]+)$"
        matches = re.match(cell_regex, tokens[0])
        if matches is None:
            return None
        col = matches.group(1).upper()
        if len(col) > 3 or col > "XFD":
            return None
        row = int(matches.group(2))
        if row > 1048576 or row == 0:
            return None
        return Cell(col, row, "default_user")

    def _parse_cell_or_range():
        cell1 = _parse_cell()
        if cell1 is None:
            return None
        tokens.pop(0)
        if len(tokens) == 0 or tokens[0] != ":":
            return cell1
        tokens.pop(0)
        if len(tokens) == 0:
            raise FormulaParseError("Unexpected end-of-formula after colon")
        cell2 = _parse_cell()
        if cell2 is None:
            raise FormulaParseError("Expected cell after colon, found " + tokens[0])
        tokens.pop(0)
        return CellRange(cell1, cell2, "default_user")

    def _parse_name_or_func():
        name_is_ok = re.match("^[a-zA-Z_][a-zA-Z0-9_.]+$", tokens[0])
        if name_is_ok is None:
            return None
        name = tokens.pop(0).upper()
        if len(tokens) == 0 or tokens[0] != "(":
            return Name(name, "default_user")
        tokens.pop(0)
        arguments = []
        while True:
            if len(tokens) == 0:
                raise FormulaParseError(
                    "Unexpected end-of-formula while parsing arguments of " + name
                )
            arg = _parse_expr()
            if arg is None:
                return None
            arguments.append(arg)
            if len(tokens) == 0:
                raise FormulaParseError(
                    "Unexpected end-of-formula while parsing arguments of " + name
                )
            next_token = tokens.pop(0)
            if next_token == ")":
                break
            elif next_token == ",":
                continue
            else:
                raise FormulaParseError(
                    "Expected closed parenthesis or comma after argument of function "
                    + name
                )
        return Function(name, arguments, "default_user")

    def _parse_unary():
        if tokens[0] in ["+", "-"]:
            op = tokens.pop(0)
            if len(tokens) == 0:
                raise FormulaParseError(
                    "Unexpected end-of-formula after unary operator " + op
                )
            return Unary(op, _parse_expr(), "default_user")

    def _parse_op():
        if tokens[0] in ["+", "-", "*", "/", "%", "^", "=", "<>", "<", ">", "<=", ">="]:
            return tokens.pop(0)
        raise FormulaParseError("Unknown operator " + tokens.pop(0))

    def _parse_basic_expr():
        if len(tokens) == 0:
            raise FormulaParseError("Incomplete expression")
        # print("Current token:", tokens[0])  # Debugging print
        logical = _parse_logical()
        if logical is not None:
            return logical
        number = _parse_number()
        if number is not None:
            return number
        cell_or_range = _parse_cell_or_range()
        if cell_or_range is not None:
            return cell_or_range
        func_or_name = _parse_name_or_func()
        if func_or_name is not None:
            return func_or_name
        if tokens[0] == "(":
            tokens.pop(0)
            expr = _parse_expr()
            if len(tokens) == 0 or tokens[0] != ")":
                raise FormulaParseError("Closed parenthesis expected")
            return expr
        if tokens[0] == "+" or tokens[0] == "-":
            op = tokens.pop(0)
            if len(tokens) == 0:
                raise FormulaParseError(
                    "Unexpected end-of-formula after unary operator " + op
                )
            expr = _parse_basic_expr()
            return Unary(op, expr, "default_user")

    def _parse_expr():
        if len(tokens) == 0:
            raise FormulaParseError("Expression cannot be empty or incomplete")
        # print("In_parse_expr")  # Debugging print
        if len(tokens) == 0:
            raise FormulaParseError("Expression cannot be empty")

        # print("Parsing expression, current tokens:", tokens)  # Debugging print

        arithmetic = []

        while True:
            basic = _parse_basic_expr()
            if basic is not None:
                arithmetic.append(basic)
            else:
                raise FormulaParseError(
                    "Expected a number, a boolean, a cell, a range, or a function call"
                )

            if len(tokens) == 0 or tokens[0] == "," or tokens[0] == ")":
                break

            arithmetic.append(_parse_op())

        # resolve precedence according to Excel rules

        level = {
            "%": 0,
            "^": 1,
            "*": 2,
            "/": 2,
            "+": 3,
            "-": 3,
            "=": 4,
            "<": 4,
            ">": 4,
            "<=": 4,
            ">=": 4,
            "<>": 4,
        }

        while len(arithmetic) != 1:
            min_i = 1
            for i in range(1, len(arithmetic), 2):
                if level[arithmetic[i]] < level[arithmetic[min_i]]:
                    min_i = i
            arithmetic = (
                arithmetic[0: min_i - 1]
                + [
                    Binary(
                        arithmetic[min_i - 1],
                        arithmetic[min_i],
                        arithmetic[min_i + 1],
                        "default_user",
                    )
                ]
                + arithmetic[min_i + 2:]
            )

        return arithmetic[0]

    expr = _parse_expr()

    if len(tokens) > 0:
        raise FormulaParseError("Multiple formulas provided")

    return expr


def parse(code):
    tokens = _tokenize(code)
    # print("Tokens: ", tokens) # Debugging Print
    return _parse(tokens)
