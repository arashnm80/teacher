<!-- page 203 -->

**Arithmetic operators**: these operators are used to do all kinds of mathematical calculation operations. The description of these operators is given in Table 16:

*Table 16: JavaScript arithmetic operators*

| Operator | Description | Example |
| --- | --- | --- |
| + , - , \* , / , % | Addition, subtraction, multiplication, division and remainder | `x = y+z , a = a*2, n = n/10` |
| ++,-- | Increasing and decreasing by one unit | `x++, y--, ++z, --w` |
| \*\* | Power | `x = y**2` |

**Assignment operators**: these operators are used to assign a value to a variable. Some of these operators are simple and some are compound; that is, besides assignment they do another operation on the operands too. Table 17 shows the set of these operators.

*Table 17: Assignment operators in JavaScript*

| Operator | Description | Example | Equivalent expression |
| --- | --- | --- | --- |
| `=` | The value of the right operand (y) is put in the left operand (x). | `x = y` | `x = y` |
| `+=` | The sum of the operands x and y is put in the left operand (x). | `x += y` | `x = x + y` |
| `-=` | The difference of the operands x and y is put in the left operand (x). | `x -= y` | `x = x – y` |
| `*=` | The product of the operands x and y is put in the left operand (x). | `x *= y` | `x = x * y` |
| `/=` | The quotient of dividing the operand x by the operand y is put in the left variable (x). | `x /= y` | `x = x / y` |
| `% =` | The remainder of dividing the operand x by the operand y is put in the left variable (x). | `x %= y` | `x = x % y` |
| `**=` | Raises the operand x to the power of the operand y and puts the result in the variable x. | `x **= y` | `x = x ** y` |

<!-- page 204 -->

**Comparison operators**: these operators are used to compare two operands.

The set of these operators is given in Table 18:

*Table 18: Comparison operators*

| Operator | Description |
| --- | --- |
| `==` and `===` | `==` checks the equality of two operands in terms of value and `===` checks the equality of two operands in terms of value and type |
| `!=` and `!==` | `!=` checks that the values of two operands are not equal and `!==` checks that the value and the type of two operands are not equal |
| `< , >` | Whether the first operand is smaller or larger than the second operand |
| `>= , <=` | Smaller than or equal, larger than or equal |
| ? | The ternary conditional operator, used to choose between two values based on a condition. |

**Logical operators (Boolean)**: logical operators are used to combine or reverse conditions. These operators make it possible to combine logical expressions in different conditions. Table 19 introduces JavaScript's logical operators:

*Table 19: Logical operators*

| Operator | Description |
| --- | --- |
| && | The AND operator checks whether both operands are true or not. |
| \|\| | The OR operator checks whether at least one of the conditions is true or not. |
| `!` | The NOT operator reverses the true or false state of a condition. |

<!-- page 205 -->

> **Workshop**
>
> **Working with the types of JavaScript operators**
>
> Create a new file named `workshop3.html` and write the `<script>` tag in the body section. Then enter the following script in it and write the results you get in the blanks.
>
> ```
> 1 let x = 10, y = 2, z= 3, w=20, s="10", n = "sara", m="sina";
> 2 x++;
>                                  ……………….
> 3 y += x;
>                                                     ……………….
> 4 --z;
>                                    ……………….
> 5 z *= y;
>                                    ……………….
> 6 x /= 2;
>                                    ……………….
> 7 w %= z;
>                                    ……………….
> 8 console.log("x: "+x + " , y:" + y + " , z:" + z , " , w:" + w);  ………………………………
> 9 let a = (x < y);                           ……………….
> 10 Let b = (x > y) && (y == z);     ……………….
> 11 Let c = (x === s);                      ……………….
> 12 Let d = c || (y != z);                   ……………….
> 13 Let e = (n < m);                       ……………….
> 14 console.log("a: "+a + " , b:" + b + " , c:" + c , " , d:" + d + " , e: "+e);
> 15 result = (x === s)? "x is equal to s": "x is not equal to s";          ……………….
> 16 console.log(result);
>                              ……………….
> ```

> **Note**
>
> When two operands are compared with the operators `==` and `!=`, the data type of the operands does not matter and only their values are checked, whereas the operators `===` and `!==` take the data type of the operands into account too.

> **Note**
>
> The expression (`x===s`)? checks the equality of the two variables x and s. If the result of the comparison is true, the expression before the ? sign is stored in the variable result, and if it is false, the expression after the : sign is stored.
