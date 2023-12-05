import uuid
import datetime


class BaseNode:
    def __init__(self, node_content, user_id):
        self.id_history = [str(uuid.uuid4())]
        self.node_content = node_content
        self.user_id = user_id
        self.timestamp = datetime.datetime.now()
        self.parent = None
        self.node_type = self.__class__.__name__

    def generate_new_id(self):
        new_id = str(uuid.uuid4())
        self.id_history.append(new_id)

    def refresh_node(self, user_id):
        self.generate_new_id()
        self.timestamp = datetime.datetime.now()
        self.user_id = user_id

    def tie_breaker_value(self):
        # Value is a combination of content and user ID
        return hash((self.node_content, self.user_id))


class Function(BaseNode):
    def __init__(self, func_name, arguments, user_id):
        super().__init__(f"Func[{func_name}]", user_id)
        self.func_name = func_name
        self.arguments = arguments
        for i, arg in enumerate(self.arguments):
            arg.parent = self
            arg.position = i

    def __str__(self):
        arg_strs = [str(arg) for arg in self.arguments]
        return f"{self.func_name}({', '.join(arg_strs)})"

    def compare_content(self, other_node):
        return self.func_name == other_node.func_name


class Cell(BaseNode):
    def __init__(self, col, row, user_id):
        super().__init__(f"Cell[{col}{row}]", user_id)
        self.col = col
        self.row = row

    def __str__(self):
        return f"{self.col}{self.row}"

    def compare_content(self, other_node):
        return self.col == other_node.col and self.row == other_node.row


class CellRange(BaseNode):
    def __init__(self, start, end, user_id):
        super().__init__(f"Range[{start}][{end}]", user_id)
        self.start = start
        self.end = end

    def __str__(self):
        return f"{str(self.start)}:{str(self.end)}"

    def compare_content(self, other_node):
        return self.start.compare_content(
            other_node.start
        ) and self.end.compare_content(other_node.end)


class Name(BaseNode):
    def __init__(self, name, user_id):
        super().__init__(f"Name[{name}]", user_id)
        self.name = name

    def __str__(self):
        return str(self.name)

    def compare_content(self, other_node):
        return self.name == other_node.name


class Number(BaseNode):
    def __init__(self, value, user_id):
        super().__init__(f"Num[{value}]", user_id)
        self.value = value

    def __str__(self):
        return str(self.value)

    def compare_content(self, other_node):
        return self.value == other_node.value


class Logical(BaseNode):
    def __init__(self, value, user_id):
        super().__init__(f"Bool[{value}]", user_id)
        self.value = value

    def __str__(self):
        return str(self.value)

    def compare_content(self, other_node):
        return self.value == other_node.value


class Binary(BaseNode):
    def __init__(self, left, op, right, user_id):
        super().__init__(f"Binary[{op}]", user_id)
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"{str(self.left)} {self.op} {str(self.right)}"

    def compare_content(self, other_node):
        return self.op == other_node.op


class Unary(BaseNode):
    def __init__(self, op, expr, user_id):
        super().__init__(f"Unary[{op}]", user_id)
        self.op = op
        self.expr = expr

    def __str__(self):
        return f"{self.op}{str(self.expr)}"

    def compare_content(self, other_node):
        return self.op == other_node.op
