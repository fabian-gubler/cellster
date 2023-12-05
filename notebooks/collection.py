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

# Rule 4: Varying Cell Range for General Functions - If the cell range of both users varies take the max of the start and end cell when defining the range.
user1_formula_4 = "MIN(A1:A9)" # Input 1
user2_formula_4 = "MIN(A2:A10)" # Input 2
merged_formula_4 = "MIN(A1:A10)" # Output

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
