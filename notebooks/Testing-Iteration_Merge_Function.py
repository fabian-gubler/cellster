import re

class Cell:
  def __init__(self, col, row):
    self.col = col
    self.row = row
  def __repr__(self):
    return "Cell[%s%d]" % (self.col, self.row)

class CellRange:
  def __init__(self, start, end):
    self.start = start
    self.end   = end
  def __repr__(self):
    return "Range[%s][%s]" % (self.start, self.end)

class Name:
  def __init__(self, name):
    self.name = name
  def __repr__(self):
    return "Name[%s]" % self.name

class Function:
  def __init__(self, func_name, arguments):
    self.func_name = func_name
    self.arguments    = arguments
  def __repr__(self):
    return "Func[%s][%d][%s]" % (self.func_name, len(self.arguments), ", ".join(map(str, self.arguments)))

class Number:
  def __init__(self, value):
    self.value = value
  def __repr__(self):
    return "Num[%f]" % self.value

class Logical:
  def __init__(self, value):
    self.value = value
  def __repr__(self):
    return "Bool[%s]" % self.value

class Binary:
  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.right = right
  def __repr__(self):
    return "Binary[%s][%s][%s]" % (self.op, self.left, self.right)

class Unary:
  def __init__(self, op, expr):
    self.op = op
    self.expr = expr
  def __repr__(self):
    return "Unary[%s][%s]" % (self.op, self.expr)

def _tokenize(code):
  return code.replace(":", " : ").replace(",", " , ").replace("(", " ( ").replace(")", " ) ")\
             .replace("*", " * ").replace("+", " + ").replace("/", " / ").replace("-", " - ")\
             .replace("%", " % ").replace("^", " ^ ").replace("=", " = ").replace("<", " < ")\
             .replace("e - ", "e-").replace("e + ", "e+")\
             .replace("> =", " >= ").replace("< =", " <= ").replace("< >", " <> ")\
             .split()


class FormulaParseError(Exception): pass

def _parse(tokens):

  def _parse_logical():
    if tokens[0].lower() == "true":
      tokens.pop(0)
      return Logical(True)
    elif tokens[0].lower() == "false":
      tokens.pop(0)
      return Logical(False)

  def _parse_number():
    try:
      number = int(tokens[0])
      tokens.pop(0)
      return Number(number)
    except ValueError:
      try:
        number = float(tokens[0])
        tokens.pop(0)
        return Number(number)
      except:
        return None

  def col_name_to_number(col):
    """Converts an Excel column name to a number (e.g., 'A' -> 1, 'Z' -> 26, 'AA' -> 27)."""
    number = 0
    for char in col:
        number = number * 26 + (ord(char) - ord('A') + 1)
    return number

  def _parse_cell():
    # https://support.microsoft.com/en-us/office/overview-of-formulas-in-excel-ecfdc708-9162-49e8-b993-c311f47ca173
    cell_regex = '^([a-zA-Z]+)([0-9]+)$'
    matches = re.match(cell_regex, tokens[0])
    if matches is None:
        return None
    col = matches.group(1).upper()
    col_number = col_name_to_number(col)
    if col_number > 16384:  # 16384 is the column number for 'XFD'
        return None
    row = int(matches.group(2))
    if row > 1048576 or row == 0:
        return None
    return Cell(col, row)

  def _parse_cell_or_range():
    cell1 = _parse_cell()
    if cell1 is None:
      return None
    tokens.pop(0)
    if len(tokens) == 0 or tokens[0] != ':':
      return cell1
    tokens.pop(0)
    if len(tokens) == 0:
      raise FormulaParseError("Unexpected end-of-formula after colon")
    cell2 = _parse_cell()
    if cell2 is None:
      raise FormulaParseError("Expected cell after colon, found " + tokens[0])
    tokens.pop(0)
    return CellRange(cell1, cell2)

  def _parse_name_or_func():
    # https://support.microsoft.com/en-us/office/names-in-formulas-fc2935f9-115d-4bef-a370-3aa8bb4c91f1
    name_is_ok = re.match('^[a-zA-Z_][a-zA-Z0-9_.]+$', tokens[0])
    if name_is_ok is None:
      return None
    name = tokens.pop(0).upper()
    if len(tokens) == 0 or tokens[0] != "(":
      return Name(name)
    tokens.pop(0)
    arguments = []
    while True:
      if len(tokens) == 0:
        raise FormulaParseError("Unexpected end-of-formula while parsing arguments of " + name)
      arg = _parse_expr()
      if arg is None:
        return None
      arguments.append(arg)
      if len(tokens) == 0:
        raise FormulaParseError("Unexpected end-of-formula while parsing arguments of " + name)
      next = tokens.pop(0)
      if next == ")":
        break
      elif next == ",":
        continue
      else:
        raise FormulaParseError("Expected closed parenthesis or comma after argument of function " + name)
    return Function(name, arguments)

  def _parse_unary():
    if tokens[0] in ["+", "-"]:
      op = tokens.pop(0)
      if len(tokens) == 0:
        raise FormulaParseError("Unexpected end-of-formula after unary operator " + op)
      return Unary(op, _parse_expr())

  def _parse_op():
    if tokens[0] in ["+", "-", "*", "/", "%", "^", "=", "<>", "<", ">", "<=", ">="]:
      return tokens.pop(0)
    raise FormulaParseError("Unknown operator " + tokens.pop(0))

  def _parse_basic_expr():
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
        raise FormulaParseError("Unexpected end-of-formula after unary operator " + op)
      expr = _parse_basic_expr()
      return Unary(op, expr)

  def _parse_expr():
    if len(tokens) == 0:
      raise FormulaParseError("Expression cannot be empty")

    arithmetic = []

    while True:
      basic = _parse_basic_expr()
      if basic is not None:
        arithmetic.append(basic)
      else:
        raise FormulaParseError("Expected a number, a boolean, a cell, a range, or a function call")

      if len(tokens) == 0 or tokens[0] == "," or tokens[0] == ")":
        break

      arithmetic.append(_parse_op())

    # resolve precedence according to
    # https://support.microsoft.com/en-us/office/calculation-operators-and-precedence
    # -in-excel-48be406d-4975-4d31-b2b8-7af9e0e2878a

    level = { "%": 0, "^": 1, "*": 2, "/": 2, "+": 3, "-": 3, "=": 4, "<": 4, ">": 4,
              "<=": 4, ">=": 4, "<>": 4 }

    # Ugh, I don't want to think about this...
    while len(arithmetic) != 1:
      min_i = 1
      for i in range(1, len(arithmetic), 2):
        if level[arithmetic[i]] < level[arithmetic[min_i]]:
          min_i = i
      arithmetic = arithmetic[0:min_i-1] \
                   + [Binary(arithmetic[min_i-1], arithmetic[min_i], arithmetic[min_i+1])] \
                   + arithmetic[min_i+2:]

    return arithmetic[0]

  expr = _parse_expr()

  if len(tokens) > 0:
    raise FormulaParseError("Multiple formulas provided")

  return expr

def parse(code):
  tokens = _tokenize(code)
  return _parse(tokens)

# Function that converts Abstract Syntax Tree (AST) back to String.
def ast_to_string(node, parent=None):

    if isinstance(node, Function):
        # If node is a Function, iterate through all arguments and convert them to a string. Joins these strings with commas.
        # The function name is then combined with these arguments enclosed in parentheses.
        args_string = ', '.join(ast_to_string(arg, node) for arg in node.arguments)
        return f"{node.func_name}({args_string})"

    elif isinstance(node, CellRange):
        # If the node is a CellRange, it converts the start and end cells of the range to their string representations and joins them with a colon like "A1:B2".
        return f"{ast_to_string(node.start, node)}:{ast_to_string(node.end, node)}"

    elif isinstance(node, Cell):
        # If the node is a Cell, it converts the cell to its string representation like "A1".
        return f"{node.col}{node.row}"

    elif isinstance(node, Name):
        # If the node is a Name/Identifier (like a named range or variable), it converts the Name/Identifier to a string.
        return node.name

    elif isinstance(node, Number):
        # If the node is a Number, it converts the number to a string.
        return str(node.value)

    elif isinstance(node, Logical):
        # If the node is a Logical (boolean value), it converts it to a string ("TRUE" or "FALSE").
        return "TRUE" if node.value else "FALSE"

    elif isinstance(node, Binary):
        # If the node is a Binary operation (like addition, subtraction), it converts both the left and right operands to strings and joins them with the operator (e.g., "A1 + B1").
        # If this binary operation is not the top-level operation (has a parent), it encloses the operation in parentheses.
        left = ast_to_string(node.left, node)
        right = ast_to_string(node.right, node)
        operation = f"{left}{node.op}{right}"
        if parent is None:
            return operation
        else:
            return f"({operation})"

    elif isinstance(node, Unary):
        # If the node is a Unary operation, it converts the operand to a string and precedes it with the unary operator (e.g., "-A1").
        return f"{node.op}{ast_to_string(node.expr, node)}"

    else:
        # If the node type is not recognized, it raises an error.
        raise ValueError(f"Unsupported AST node type: {type(node)}")


# Test function that tests various properties (merging, commutativity, idempotency, and associativity) of the merge_function to ensure its correctness.
def test_merge_function(user1_formula, user2_formula, expected_merged_formula):

    # Merging the two user formulas.
    actual_merged_formula = merge_function(user1_formula, user2_formula)

    # Test if the merging worked correctly.
    if actual_merged_formula != expected_merged_formula:
        print(f"Test failed: Merging {user1_formula} and {user2_formula} produced {actual_merged_formula}, expected {expected_merged_formula}")
        return False
    else:
        print("Merging test passed.")

    # Test Commutative Property: merge_function(a, b) == merge_function(b, a).
    # Meaning the order of the inputs should not affect the outcome.
    if merge_function(user1_formula, user2_formula) != merge_function(user2_formula, user1_formula):
        print("Test failed: Merge function is not commutative.")
        return False
    else:
        print("Commutative property test passed.")

    # Test Idempotent Property: merge_function(a, a) == a.
    # Meaning merging a formula with itself should yield the original formula.
    # Test Idempotent Property with user1_formula: merge_function(a, a) == a
    if merge_function(user1_formula, user1_formula) != user1_formula:
        print(f"Test failed: Merge function is not idempotent with {user1_formula}.")
        return False
    else:
        print(f"Idempotent property test passed with {user1_formula}.")

    # Test Idempotent Property with user2_formula: merge_function(b, b) == b
    if merge_function(user2_formula, user2_formula) != user2_formula:
        print(f"Test failed: Merge function is not idempotent with {user2_formula}.")
        return False
    else:
        print(f"Idempotent property test passed with {user2_formula}.")

    # Test Associative Property: merge_function(a, merge_function(b, c)) == merge_function(merge_function(a, b), c).
    # Meaning the grouping of operations does not change the result.
    # For simplicity, using the same formula for b and c.
    if merge_function(user1_formula, merge_function(user2_formula, user2_formula)) != merge_function(merge_function(user1_formula, user2_formula), user2_formula):
        print("Test failed: Merge function is not associative.")
        return False
    else:
        print("Associative property test passed.")

    # If all tests are passed, the function returns True.
    return True

def test_all_merge_functions(test_cases):
    # Takes a list of test cases, each as a tuple of (user1_formula, user2_formula, merged_formula)

    all_tests_passed = True

    for user1_formula, user2_formula, expected_merged_formula in test_cases:
        # Basic Merge Test
        actual_merged_formula = merge_function(user1_formula, user2_formula)
        if actual_merged_formula != expected_merged_formula:
            print(f"Test failed for formulas '{user1_formula}' and '{user2_formula}'. Expected '{expected_merged_formula}', got '{actual_merged_formula}'.")
            all_tests_passed = False
            break

        # Commutative Property Test
        if merge_function(user1_formula, user2_formula) != merge_function(user2_formula, user1_formula):
            print(f"Commutative test failed for formulas '{user1_formula}' and '{user2_formula}'.")
            all_tests_passed = False
            break

        # Idempotent Property Test
        if merge_function(user1_formula, user1_formula) != user1_formula or merge_function(user2_formula, user2_formula) != user2_formula:
            print(f"Idempotent test failed for formulas '{user1_formula}' or '{user2_formula}'.")
            all_tests_passed = False
            break

        # Associative Property Test
        # This is a simplified version and might need adjustment depending on the complexity of your merge function
        if merge_function(user1_formula, merge_function(user2_formula, user2_formula)) != merge_function(merge_function(user1_formula, user2_formula), user2_formula):
            print(f"Associative test failed for formulas '{user1_formula}', '{user2_formula}'.")
            all_tests_passed = False
            break

    if all_tests_passed:
        print("All merge function tests passed successfully for all test cases.")

# Function that merges two Excel String Formulas.
def merge_function(user1_formula, user2_formula):
    # Direct Return for Identical Formulas:
    # If both input formulas are exactly the same, return one of them immediately.
    # This prevents unnecessary processing and keeps the formula unchanged.
    if user1_formula == user2_formula:
        return user1_formula

    # Check if one formula is a superset of the other.
    # If user2_formula contains user1_formula as a subset, return user2_formula.
    if user1_formula in user2_formula:
        return user2_formula

    # Similarly, if user1_formula contains user2_formula as a subset, return user1_formula.
    if user2_formula in user1_formula:
        return user1_formula

    # Commutativity Support:
    # If the first formula is longer than the second, they are swapped.
    # This ensures that the function works the same regardless of the order of the inputs.
    if len(user1_formula) > len(user2_formula):
        user1_formula, user2_formula = user2_formula, user1_formula

    # Parsing:
    # Both formulas are parsed into Abstrac Styntax Trees (ASTs).
    user1_ast = parse(user1_formula)
    user2_ast = parse(user2_formula)

    def col_name_to_number(col):
      """Converts an Excel column name to a number (e.g., 'A' -> 1, 'Z' -> 26, 'AA' -> 27)."""
      number = 0
      for char in col:
          number = number * 26 + (ord(char.upper()) - ord('A') + 1)
      return number

    def merge_sum_ranges(ast1, ast2):
    # Check if both AST nodes are functions
      if isinstance(ast1, Function) and isinstance(ast2, Function):
        # Combine all arguments (ranges) from both functions, ensuring they are cell ranges
        all_ranges = [arg for arg in ast1.arguments if isinstance(arg, CellRange)] + \
                     [arg for arg in ast2.arguments if isinstance(arg, CellRange)]

        # Check if there are multiple ranges
        if len(all_ranges) > 1:
            # Sort ranges based on column and row
            sorted_ranges = sorted(all_ranges, key=lambda x: (col_name_to_number(x.start.col), x.start.row))

            # Merge adjacent or overlapping ranges
            merged_ranges = []
            current_range = sorted_ranges[0]
            for next_range in sorted_ranges[1:]:
                if current_range.end.col == next_range.start.col and current_range.end.row + 1 >= next_range.start.row:
                    # Extend the current range
                    current_range = CellRange(current_range.start, Cell(current_range.end.col, max(current_range.end.row, next_range.end.row)))
                else:
                    # Add the current range and move to the next one
                    merged_ranges.append(current_range)
                    current_range = next_range
            merged_ranges.append(current_range)  # Add the last range

            # Check if multiple ranges still exist after merging
            if len(merged_ranges) > 1:
                return Function(ast1.func_name, merged_ranges)
            else:
                # Only one merged range, return it
                return Function(ast1.func_name, [merged_ranges[0]])

        # If only one range present or ranges are the same, handle as before
        range1 = ast1.arguments[0]
        range2 = ast2.arguments[0]
        start_row = min(range1.start.row, range2.start.row)
        end_row = max(range1.end.row, range2.end.row)
        start_col = min(range1.start.col, range2.start.col, key=lambda x: col_name_to_number(x))
        end_col = max(range1.end.col, range2.end.col, key=lambda x: col_name_to_number(x))

        # Creating the merged range
        merged_range = CellRange(Cell(start_col, start_row), Cell(end_col, end_row))
        return Function(ast1.func_name, [merged_range])

      return None

    def is_same_operation(ast1, ast2):
        # Checks if the same operation (like division) is applied on both ASTs to redundant application of the same operation.
        return isinstance(ast1, Binary) and isinstance(ast2, Binary) and ast1.op == ast2.op

    def apply_additional_operation(merged_ast, original_ast):
        # Applies additional operations (like division) found in the original ASTs to the merged SUM.
        # It ensures not to duplicate an operation if it's already applied.
        if isinstance(original_ast, Binary) and isinstance(original_ast.left, Function) and original_ast.left.func_name == 'SUM':
            if is_same_operation(merged_ast, original_ast):
                # If the same operation is already applied, don't apply it again.
                return merged_ast
            return Binary(merged_ast, original_ast.op, original_ast.right)
        return merged_ast

    def merge_operations(ast1, ast2):
        # Checks if both ast1 and ast2 are Binary nodes (like A + B, C - D) and have the same operator (e.g., both '+'). If so, it attempts to merge these binary operations.
        if isinstance(ast1, Binary) and isinstance(ast2, Binary) and ast1.op == ast2.op:
            # It calls merge_ast on the left children (operands) of both ASTs.This recursively merges the left side of the binary operations.
            merged_left = merge_ast(ast1.left, ast2.left)
            # It calls merge_ast on the right children (operands) of both ASTs. This merges the right side of the binary operations.
            merged_right = merge_ast(ast1.right, ast2.right)
            # After merging the left and right operands, it creates a new Binary node with these merged operands
            return Binary(merged_left, ast1.op, merged_right)
        # If the ASTs don't represent the same binary operation, the function returns the first AST (ast1).
        return ast1

    def merge_ast(ast1, ast2):
        # Core function to merge two ASTs using merge_ast and merge_operations. It first merges the SUM ranges and then applies any additional operations.
        # Check and merge function ranges if present
        # First, try merging function ranges (e.g., SUM ranges)
        merged_sum = merge_sum_ranges(ast1, ast2) or ast1
        merged_ast = apply_additional_operation(merged_sum, ast1)
        return apply_additional_operation(merged_ast, ast2)

    # Performing the merge operation (commutativity & associativity)
    user1_ast_merged = merge_ast(user1_ast, user2_ast) # merge_ast is called with user1_ast and user2_ast as arguments.
    user2_ast_merged = merge_ast(user2_ast, user1_ast) # merge_ast is called again, but this time the order of the ASTs is reversed.
    merged_ast = merge_operations(user1_ast_merged, user2_ast_merged) # Finally, merge_operations is called with the two merged ASTs (user1_ast_merged and user2_ast_merged).

    # Convert the merged AST back to a string representation of the formula.
    return ast_to_string(merged_ast)

#PARSER ERRORS
error1 = "SUM(A2:A9)+SUM(SUM(B1:B5):C1)"
error2 = "SUM(A2:A9)+(B1-B2)*C3"
error3 = "SUM($A$2:A9)"
error4 = "SUM($A2:A9)"
error5 = "SUM(Z50:Z211)"

# Check Parser
parse("SUM(XFD55:XFD65)")

# Rule 5: Different Cell References - If the cell reference of  the letters of both users varies take both references and combine them.
user1_formula_5a = "SUM(A1:A5, B1:B5)" # Input 1
user2_formula_5a = "SUM(C1:C5)" # Input 2
merged_formula_5a = "SUM(A1:A5, B1:B5, C1:C5)" # Output
current_output_5a = "SUM(A1:A5, C1:C5)" # Wrong output at the moment

user1_formula_5b = "SUM(D1:D10)" # Input 1
user2_formula_5b = "SUM(E1:E10, F1:F10)" # Input 2
merged_formula_5b = "SUM(D1:D10, E1:E10, F1:F10)" # Output
current_output_5b = "SUM(D1:D10, E1:E10)" # Wrong output at the moment

user1_formula_5c = "SUM(B10:B15)" # Input 1
user2_formula_5c = "SUM(B20:B25)" # Input 2
merged_formula_5c = "SUM(B10:B15, B20:B25)" # Output
current_output_5c = "SUM(B10:B25)" # Wrong output at the moment


# Apply the merge function on the two user formulas
merge_function(user1_formula_5a, user2_formula_5a)

# Apply the merge function commutatively on the two user formulas
merge_function(user2_formula_5a, user1_formula_5a)

output_merge_function = merge_function(user1_formula_5a, user2_formula_5a)
output_merge_function_commutative = merge_function(user2_formula_5a, user1_formula_5a)

merged_formula_5a==output_merge_function==output_merge_function_commutative

print(merged_formula_5a)
print(output_merge_function)
print(output_merge_function_commutative)

# Test function that tests various properties (merging, commutativity, idempotency, and associativity) of the merge_function to ensure its correctness.
def test_merge_function(user1_formula, user2_formula, expected_merged_formula):

    # Merging the two user formulas.
    actual_merged_formula = merge_function(user1_formula, user2_formula)

    # Test if the merging worked correctly.
    if actual_merged_formula != expected_merged_formula:
        print(f"Test failed: Merging {user1_formula} and {user2_formula} produced {actual_merged_formula}, expected {expected_merged_formula}")
        return False
    else:
        print("Merging test passed.")

    # Test Commutative Property: merge_function(a, b) == merge_function(b, a).
    # Meaning the order of the inputs should not affect the outcome.
    if merge_function(user1_formula, user2_formula) != merge_function(user2_formula, user1_formula):
        print("Test failed: Merge function is not commutative.")
        return False
    else:
        print("Commutative property test passed.")

    # Test Idempotent Property: merge_function(a, a) == a.
    # Meaning merging a formula with itself should yield the original formula.
    # Test Idempotent Property with user1_formula: merge_function(a, a) == a
    if merge_function(user1_formula, user1_formula) != user1_formula:
        print(f"Test failed: Merge function is not idempotent with {user1_formula}.")
        return False
    else:
        print(f"Idempotent property test passed with {user1_formula}.")

    # Test Idempotent Property with user2_formula: merge_function(b, b) == b
    if merge_function(user2_formula, user2_formula) != user2_formula:
        print(f"Test failed: Merge function is not idempotent with {user2_formula}.")
        return False
    else:
        print(f"Idempotent property test passed with {user2_formula}.")

    # Test Associative Property: merge_function(a, merge_function(b, c)) == merge_function(merge_function(a, b), c).
    # Meaning the grouping of operations does not change the result.
    # For simplicity, using the same formula for b and c.
    if merge_function(user1_formula, merge_function(user2_formula, user2_formula)) != merge_function(merge_function(user1_formula, user2_formula), user2_formula):
        print("Test failed: Merge function is not associative.")
        return False
    else:
        print("Associative property test passed.")

    # If all tests are passed, the function returns True.
    return True

def test_all_merge_functions(test_cases):
    # Takes a list of test cases, each as a tuple of (user1_formula, user2_formula, merged_formula)

    all_tests_passed = True

    for user1_formula, user2_formula, expected_merged_formula in test_cases:
        # Basic Merge Test
        actual_merged_formula = merge_function(user1_formula, user2_formula)
        if actual_merged_formula != expected_merged_formula:
            print(f"Test failed for formulas '{user1_formula}' and '{user2_formula}'. Expected '{expected_merged_formula}', got '{actual_merged_formula}'.")
            all_tests_passed = False
            break

        # Commutative Property Test
        if merge_function(user1_formula, user2_formula) != merge_function(user2_formula, user1_formula):
            print(f"Commutative test failed for formulas '{user1_formula}' and '{user2_formula}'.")
            all_tests_passed = False
            break

        # Idempotent Property Test
        if merge_function(user1_formula, user1_formula) != user1_formula or merge_function(user2_formula, user2_formula) != user2_formula:
            print(f"Idempotent test failed for formulas '{user1_formula}' or '{user2_formula}'.")
            all_tests_passed = False
            break

        # Associative Property Test
        # This is a simplified version and might need adjustment depending on the complexity of your merge function
        if merge_function(user1_formula, merge_function(user2_formula, user2_formula)) != merge_function(merge_function(user1_formula, user2_formula), user2_formula):
            print(f"Associative test failed for formulas '{user1_formula}', '{user2_formula}'.")
            all_tests_passed = False
            break

    if all_tests_passed:
        print("All merge function tests passed successfully for all test cases.")


error_1 = ("SUM(A2:A9)", "SUM(A2:A9)+SUM(SUM(B1:B5):C1)", "SUM(A2:A9)+SUM(SUM(B1:B5):C1)")
error_2 = ("SUM(A2:A9)", "SUM(A2:A9)+(B1-B2)*C3", "SUM(A2:A9)+(B1-B2)*C3")

# Rule 1: Identical Formulas - If both users have the same formula, the merged output should be the formula.
user1_formula_1 = "SUM(A2:A9)*5" # Input 1
user2_formula_1 = "SUM(A2:A9)*5" # Input 2
merged_formula_1 = "SUM(A2:A9)*5" # Output

test_cases = [
        ("SUM(A2:A9)*5", "SUM(A2:A9)*5", "SUM(A2:A9)*5"),
        ('1+2+3', '1+2+3', '1+2+3'),
        ('A1+B2+A3', 'A1+B2+A3', 'A1+B2+A3'),
        ('3-2+6', '3-2+6', '3-2+6'),
        ('3-2+6*2', '3-2+6*2', '3-2+6*2'),
        ('3/2+6*2', '3/2+6*2', '3/2+6*2'),
        ('3/2+6*2-2+5+3-1', '3/2+6*2-2+5+3-1', '3/2+6*2-2+5+3-1'),
        ('A1/B2+C6*A2-E2+D5+B3-A1', 'A1/B2+C6*A2-E2+D5+B3-A1', 'A1/B2+C6*A2-E2+D5+B3-A1')
    ]

# Test if this rule works
test_merge_function(user1_formula_1, user2_formula_1, merged_formula_1)

# Call the test function
test_all_merge_functions(test_cases)

# Rule 2: Varying Cell Range - If the cell range of both users varies take the max of the start and end cell when defining the range.
user1_formula_2 = "SUM(A1:A9)" # Input 1
user2_formula_2 = "SUM(A2:A10)" # Input 2
merged_formula_2 = "SUM(A1:A10)" # Output

test_cases = [
    # Test cases with varying ranges in the SUM function
    ("SUM(A1:A9)", "SUM(A2:A10)", "SUM(A1:A10)"),
    ("SUM(B1:B5)", "SUM(B3:B8)", "SUM(B1:B8)"),
    ("SUM(C10:C20)", "SUM(C15:C25)", "SUM(C10:C25)"),
    ("SUM(D50:D60)", "SUM(D55:D65)", "SUM(D50:D65)"),

    # Test cases with varying ranges in multi-letter column names
    ("SUM(Z100:Z211)", "SUM(Z50:Z111)", "SUM(Z50:Z211)"),
    ("SUM(AA1:AA5)", "SUM(AA4:AA10)", "SUM(AA1:AA10)"),
    ("SUM(BC10:BC20)", "SUM(BC15:BC25)", "SUM(BC10:BC25)"),
    ("SUM(XFD50:XFD60)", "SUM(XFD55:XFD65)", "SUM(XFD50:XFD65)"),

    # Test cases with varying ranges and additional operations
    ("SUM(E1:E5)*2", "SUM(E3:E10)", "SUM(E1:E10)*2"),
    ("SUM(F1:F10)+SUM(Z11:Z20)", "SUM(F2:F12)+SUM(Z9:Z18)", "SUM(F1:F12)+SUM(Z9:Z20)"),
    ("SUM(G10:G20)-5", "SUM(G15:G25)", "SUM(G10:G25)-5"),
]

# Test if this rule works
test_merge_function(user1_formula_2, user2_formula_2, merged_formula_2)

# Run the test function with the defined test cases
test_all_merge_functions(test_cases)

# Rule 3: Node Appendage - If one user has appended something additional or new to the formula, add evrything that is additional and new.
user1_formula_3 = "SUM(A2:A9)" # Input 1
user2_formula_3 = "SUM(A2:A9)*5" # Input 2
merged_formula_3 = "SUM(A2:A9)*5" # Output

test_cases = [
    # Simple appendages
    ("SUM(A2:A9)", "SUM(A2:A9)*5", "SUM(A2:A9)*5"),
    ("SUM(A2:A9)", "SUM(A2:A9)+5", "SUM(A2:A9)+5"),
    ("SUM(A2:A9)", "SUM(A2:A9)-5", "SUM(A2:A9)-5"),
    ("SUM(A2:A9)", "SUM(A2:A9)/5", "SUM(A2:A9)/5"),
    ("SUM(A2:A9)", "SUM(A2:A9)+5-1", "SUM(A2:A9)+5-1"),
    ("SUM(A2:A9)", "SUM(A2:A9)*2-1", "SUM(A2:A9)*2-1"),
    ("SUM(A2:A9)", "SUM(A2:A9)-1+3+4", "SUM(A2:A9)-1+3+4"),

    # Combining functions with different operations
    ("SUM(A2:A9)", "SUM(A2:A9)*SUM(B2:B9)", "SUM(A2:A9)*SUM(B2:B9)"),
    ("A1+B1", "A1+B1-C1/D1", "A1+B1-C1/D1"),
    ("2*3", "2*3+4/5-6", "2*3+4/5-6"),
    ("SUM(A2:A9)", "SUM(A2:A9)+SUM(B1:B5)-C1", "SUM(A2:A9)+SUM(B1:B5)-C1"),
    ("SUM(A1:A10)", "SUM(A1:A10)+A1", "SUM(A1:A10)+A1"),
    ('SUM(A2:A9)', 'SUM(A2:A9) + COUNT(A2:A9)', 'SUM(A2:A9) + COUNT(A2:A9)'),

    # Nested functions
    ("MAX(A1:A10)", "MAX(A1:A10)+MIN(B1:B10)", "MAX(A1:A10)+MIN(B1:B10)"),

    # Complex appendages
    ("SUM(A2:A9)", "SUM(A2:A9)/SUM(B1:B10)", "SUM(A2:A9)/SUM(B1:B10)"),
    ("1+2+3", "1+2+3+4*5/6", "1+2+3+4*5/6"),
    ('4*3+2-4', '4*3+2-4+3*5', '4*3+2-4+3*5'),
    ("A1+B1", "A1+B1+C1*D1-E1", "A1+B1+C1*D1-E1"),
    ("SUM(X1:X10)", "SUM(X1:X10)-AVG(Y1:Y10)+MAX(Z1:Z10)", "SUM(X1:X10)-AVG(Y1:Y10)+MAX(Z1:Z10)"),

    # Combination Rule 2 & Rule 3: Node Appendage
    ('SUM(A2:A10)', 'SUM(A2:A9)/B5', 'SUM(A2:A10)/B5')
]

# Test if this rule works
test_merge_function(user1_formula_3, user2_formula_3, merged_formula_3)

# Run the test function with the defined test cases
test_all_merge_functions(test_cases)

# Rule 4: Varying Cell Range for General Functions - If the cell range of both users varies take the max of the start and end cell when defining the range.
user1_formula_4 = "MIN(A1:A9)" # Input 1
user2_formula_4 = "MIN(A2:A10)" # Input 2
merged_formula_4 = "MIN(A1:A10)" # Output

test_cases = [
    # Test cases for the MIN function with varying ranges
    ("MIN(H1:H9)", "MIN(H2:H10)", "MIN(H1:H10)"),
    ("MIN(I1:I5)", "MIN(I3:I8)", "MIN(I1:I8)"),
    ("MIN(J10:J20)", "MIN(J15:J25)", "MIN(J10:J25)"),
    ("MIN(K50:K60)", "MIN(K55:K65)", "MIN(K50:K65)"),

    # Test cases for the MAX function with varying ranges
    ("MAX(L1:L9)", "MAX(L2:L10)", "MAX(L1:L10)"),
    ("MAX(M1:M5)", "MAX(M3:M8)", "MAX(M1:M8)"),
    ("MAX(N10:N20)", "MAX(N15:N25)", "MAX(N10:N25)"),
    ("MAX(O50:O60)", "MAX(O55:O65)", "MAX(O50:O65)"),

    # Test cases for the COUNT function with varying ranges
    ("COUNT(P1:P9)", "COUNT(P2:P10)", "COUNT(P1:P10)"),
    ("COUNT(Q1:Q5)", "COUNT(Q3:Q8)", "COUNT(Q1:Q8)"),
    ("COUNT(R10:R20)", "COUNT(R15:R25)", "COUNT(R10:R25)"),
    ("COUNT(S50:S60)", "COUNT(S55:S65)", "COUNT(S50:S65)"),

    # Test cases with varying ranges and multiple functions
    ("MIN(T1:T5)+MAX(T6:T10)", "MIN(T3:T8)+MAX(T6:T11)", "MIN(T1:T8)+MAX(T6:T11)"),
    ("COUNT(U1:U10)-SUM(U11:U20)", "COUNT(U1:U10)-SUM(U5:U15)", "COUNT(U1:U10)-SUM(U5:U20)"),
    ("MAX(V10:V20)/MIN(V21:V30)", "MAX(V10:V20)/MIN(V15:V25)", "MAX(V10:V20)/MIN(V15:V30)"),
    ("SUM(W50:W60)*COUNT(W61:W70)", "SUM(W50:W60)*COUNT(W55:W65)", "SUM(W50:W60)*COUNT(W55:W70)"),
]

# Test if this rule works
test_merge_function(user1_formula_3, user2_formula_3, merged_formula_3)

# Run the test function with the defined test cases
test_all_merge_functions(test_cases)

# Rule 5: Different Cell References - If the cell reference of  the letters of both users varies take both references and combine them.
user1_formula_5 = "SUM(A1:A9)" # Input 1
user2_formula_5 = "SUM(C1:C9)" # Input 2
merged_formula_5 = "SUM(A1:A9, C1:C9)" # Output

test_cases = [
    # Test cases for different column references
    ("SUM(A1:A9)", "SUM(C1:C9)", "SUM(A1:A9, C1:C9)"),
    ("SUM(B1:B10)", "SUM(D1:D5)", "SUM(B1:B10, D1:D5)"),
    ("SUM(E10:E20)", "SUM(G10:G20)", "SUM(E10:E20, G10:G20)"),
    #("SUM(Z1:Z5)", "SUM(X1:X5)", "SUM(X1:X5, Z1:Z5)"), # Note the order change due to sorting

    # Test cases for different row references
    ("SUM(A1:A5)", "SUM(A6:A10)", "SUM(A1:A10)"),

    # Test cases for mixed references
    ("SUM(C1:C9)", "SUM(D10:D19)", "SUM(C1:C9, D10:D19)"),
    ("SUM(B10:B15)", "SUM(B20:B25)", "SUM(B10:B15, B20:B25)"),

    # Test cases involving multiple cell ranges
    ("SUM(A1:A5, B1:B5)", "SUM(C1:C5)", "SUM(A1:A5, B1:B5, C1:C5)"),
    ("SUM(D1:D10)", "SUM(E1:E10, F1:F10)", "SUM(D1:D10, E1:E10, F1:F10)")

]

# Test if this rule works
test_merge_function(user1_formula_5, user2_formula_5, merged_formula_5)

# Run the test function with the defined test cases
test_all_merge_functions(test_cases)

### NOT SOLVED YET
# Rule 5: If a user inserts something to the cell, also insert it.
user1_formula_4 = "1+2+3" # Input 1
user2_formula_4 = "1+2+4+3" # Input 2
merged_formula_4 = "1+2+4+3" # Output

test_cases = [
    # Simple insertions
    ("1+2+3", "1+2+4+3", "1+2+4+3"),
    ("A1+B1+C1", "A1+B1+D1+C1", "A1+B1+D1+C1"),
    ("SUM(A1:A10)", "SUM(A1:A5)+SUM(A6:A10)", "SUM(A1:A5)+SUM(A6:A10)"),
    ("MAX(B1:B10)", "MAX(B1:B5)+MAX(B6:B10)", "MAX(B1:B5)+MAX(B6:B10)"),

    # Insertions with multiple elements
    ("1+2+3", "1+5+2+6+3+4", "1+5+2+6+3+4"),
    ("A1+B1", "A1+X1+B1+Y1", "A1+X1+B1+Y1"),
    ("SUM(C1:C10)", "SUM(C1:C5)+X1+SUM(C6:C10)+Y1", "SUM(C1:C5)+X1+SUM(C6:C10)+Y1"),

    # Insertions in complex expressions
    ("(A1+B1)*C1", "(A1+X1+B1)*C1", "(A1+X1+B1)*C1"),
    ("2*3+4", "2*5*3+6+4", "2*5*3+6+4"),
    ("SUM(D1:D10)/10", "SUM(D1:D5)+X1+SUM(D6:D10)/10", "SUM(D1:D5)+X1+SUM(D6:D10)/10"),

    # Nested functions with insertions
    ("SUM(SUM(E1:E5):E10)", "SUM(SUM(E1:E3)+X1:SUM(E4:E5):E10)", "SUM(SUM(E1:E3)+X1:SUM(E4:E5):E10)"),
    ("MAX(F1:F10)-MIN(F1:F10)", "MAX(F1:F5)+X1-MAX(F6:F10)-MIN(F1:F5)-Y1-MIN(F6:F10)", "MAX(F1:F5)+X1-MAX(F6:F10)-MIN(F1:F5)-Y1-MIN(F6:F10)"),

    # Insertions with functions
    ("AVG(G1:G10)", "AVG(G1:G5)+X1+AVG(G6:G10)", "AVG(G1:G5)+X1+AVG(G6:G10)"),
    ("1+SUM(H1:H10)", "1+SUM(H1:H5)+X1+SUM(H6:H10)", "1+SUM(H1:H5)+X1+SUM(H6:H10)"),
]

# Test if this rule works
test_merge_function(user1_formula_4, user2_formula_4, merged_formula_4)

# Run the test function with the defined test cases
test_all_merge_functions(test_cases)

# Rule 5: Conditional Addition - If you have two different Sumifs add them up.
user1_formula_5 = 'SUMIF(A2:A9, ">5")' # Input 1
user2_formula_5 = 'SUMIF(B1:B6;"<10")' # Input 2
merged_formula_5 = 'SUMIF(A2:A9;">5") + SUMIF(B1:B6;"<10")' # Output

# Rule 8: Nested Functions - If one user adds nesting use the nesting.
user1_formula_8 = 'SUM(A2:A9)' # Input 1
user2_formula_8 = 'SUM(SUM(A2:A9), 10)' # Input 2
merged_formula_8 = 'SUM(SUM(A2:A9), 10)' # Output

# Rule 10: Different Criteria in SUMIF - Combine both criteria within a specified range.
user1_formula_10 = 'SUMIF(A2:A9, ">5")' # Input 1
user2_formula_10 = 'SUMIF(A2:A9, "<10")' # Input 2
merged_formula_10 = 'SUMIF(A2:A9, ">5", A2:A9) - SUMIF(A2:A9, ">=10", A2:A9)' # Output

# Rule 12: Add Brackets - Use brackets in the output.
user1_formula_12 = "2 + 3" # Input 1
user2_formula_12 = "(2 * 3) * 4" # Input 2
merged_formula_12 = "(2 + 3) * 4" # Output

# Rule 13: Merging IF Statements - Combine different IF statements.
user1_formula_13 = 'IF(A2 > 5, "Yes", "No")' # Input 1
user2_formula_13 = 'IF(B2 < 3, "True", "False")' # Input 2
merged_formula_13 = 'IF(A2 > 5, "Yes", "No") & IF(B2 < 3, "True", "False")' # Output

# Rule 14: Combining Different Date Functions - Merge different date-related functions.
user1_formula_14 = 'YEAR(A2)' # Input 1
user2_formula_14 = 'MONTH(A2)' # Input 2
merged_formula_14 = 'YEAR(A2) & MONTH(A2)' # Output


### PARSER CAN NOT HANDLE THESE
# Rule 15: Combining Absolute and Relative References - If one user uses absolut and the other relativ references use the absolut reference.
user1_formula_7 = 'SUM($A$2:A9)' # Input 1
user2_formula_7 = 'SUM(A2:A9)' # Input 2
merged_formula_7 = 'SUM($A$2:A9)' # Output

# Rule 16: Mixed References - If one formula uses mixed references, use the mixed reference.
user1_formula_9 = "SUM($A2:A9)" # Input 1
user2_formula_9 = "SUM(A2:A9)" # Input 2
merged_formula_9 = "SUM($A2:A9)" # Output
