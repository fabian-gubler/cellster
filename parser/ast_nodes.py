
import uuid
import datetime

class BaseNode:
    def __init__(self, node_content, user_id):
        self.id = str(uuid.uuid4())
        self.id_history = [self.id]
        self.node_content = node_content
        self.user_id = user_id
        self.timestamp = datetime.datetime.now()

    def update_content(self, new_content, user_id):
        self.node_content = new_content
        self.user_id = user_id
        self.timestamp = datetime.datetime.now()

    # Add more common methods here

class Cell(BaseNode):
    def __init__(self, col, row, user_id):
        super().__init__(f"Cell[{col}{row}]", user_id)
        self.col = col
        self.row = row


class CellRange(BaseNode):
    def __init__(self, start, end, user_id):
        super().__init__(f"Range[{start}][{end}]", user_id)
        self.start = start
        self.end = end


class Name(BaseNode):
    def __init__(self, name, user_id):
        super().__init__(f"Name[{name}]", user_id)
        self.name = name


class Function(BaseNode):
    def __init__(self, func_name, arguments, user_id):
        super().__init__(f"Func[{func_name}]", user_id)
        self.func_name = func_name
        self.arguments = arguments

class Number(BaseNode):
    def __init__(self, value, user_id):
        super().__init__(f"Num[{value}]", user_id)
        self.value = value

class Logical(BaseNode):
    def __init__(self, value, user_id):
        super().__init__(f"Bool[{value}]", user_id)
        self.value = value

class Binary(BaseNode):
    def __init__(self, left, op, right, user_id):
        super().__init__(f"Binary[{op}]", user_id)
        self.left = left
        self.op = op
        self.right = right

class Unary(BaseNode):
    def __init__(self, op, expr, user_id):
        super().__init__(f"Unary[{op}]", user_id)
        self.op = op
        self.expr = expr
