# Excel Functions

The following provides a quick reference tot he supported excel functions, their argument boundaries and common usage:

## Basic Functionality

### Logical Functions:

| Function                                            | Boundary | Uses                                                                           |
| --------------------------------------------------- | -------- | ------------------------------------------------------------------------------ |
| IF(logical_test, [value_if_true], [value_if_false]) | 1:3      | 3 arguments (the last two are optional but generally used).                    |
| AND(logical1, [logical2], ...)                      | 1:N      | Requires at least one argument, but typically uses two or more for comparison. |
| OR(logical1, [logical2], ...)                       | 1:N      | Requires at least one argument, typically used with two or more.               |
| NOT(logical)                                        | 1        | Inverts the value of its argument.                                             |


### Statistical Functions:

| Function                         | Boundary | Uses                                                       |
| -----------                      | -------- | ---------------------                                      |
| SUM(number1, [number2], ...)     | 1:N      | Adds all the numbers in a range of cells.                  |
| AVERAGE(number1, [number2], ...) | 1:N      | Calculates the average of the numbers in a range of cells. |
| MIN(number1, [number2], ...)     | 1:N      | Returns the smallest number in a set of values.            |
| MAX(number1, [number2], ...)     | 1:N      | Returns the largest number in a set of values.             |
| PRODUCT(number1, [number2], ...) | 1:N      | Multiplies all the numbers given as arguments.             |

## Extended Functionality

### Lookup and Reference Functions:

| Function                                                          | Boundary | Uses                  |
| -----------                                                       | -------- | --------------------- |
| VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup]) | 3:4      |                       |
| HLOOKUP(lookup_value, table_array, row_index_num, [range_lookup]) | 3:4      |                       |
| INDEX(array, row_num, [column_num])                               | 2:3      |                       |
| MATCH(lookup_value, lookup_array, [match_type])                   | 2:3      |                       |

### Text Functions:

| Function                         | Boundary | Uses                                                                                   |
| ------------                     | -------- | --------------------------------------------                                           |
| CONCATENATE(text1, [text2], ...) | 1:N      | Concatenates a set number of text items. Replaced by `CONCAT` in newer Excel versions. |
| LEFT(text, [num_chars])          | 1:2      | Requires text and an optional number of characters to extract from the left.           |
| RIGHT(text, [num_chars])         | 1:2      | Requires text and an optional number of characters to extract from the right.          |

### Date and Time Functions:

| Function                   | Boundary | Uses                                           |
| -----------                | -------- | ---------------------                          |
| DATE(year, month, day)     | 3        | Requires exactly 3 arguments to create a date. |
| TIME(hour, minute, second) | 3        | Requires exactly 3 arguments to create a time. |


### Mathematical Functions:

| Function                  | Boundary | Uses                       |
| -----------               | -------- | ---------------------      |
| POWER(number, power)      | 2        | Takes exactly 2 arguments. |
| ROUND(number, num_digits) | 2        | Also takes 2 arguments.    |
