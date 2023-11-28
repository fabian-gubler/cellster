from my_parser import parse, Cell, CellRange, Name, Function, Number, Logical, Binary, Unary
from ast_to_string import ast_to_string


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