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

  def _parse_cell():
    # https://support.microsoft.com/en-us/office/overview-of-formulas-in-excel-ecfdc708-9162-49e8-b993-c311f47ca173
    cell_regex = '^([a-zA-Z]+)([0-9]+)$'
    matches = re.match(cell_regex, tokens[0])
    if matches is None:
      return None
    col = matches.group(1).upper()
    if len(col) > 3 or col > 'XFD':
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
