**Page 203**

Arithmetic operators (`Arithmetic`): These operators are used to perform various mathematical calculations. These operators are described in Table 16:

Table 16 JavaScript arithmetic operators

Operator

### Explanation

### Example

Addition, subtraction, multiplication, division, and remainder `x` = `y+z` , `a` = `a*2`, `n` = `n/10`

% , / , * , - , + --,++Increment and decrement by one unit`x++`, `y--`, `++z`, `--w` **Exponentiation`x` = `y**2`

Assignment operators (`Assignment`): These operators are used to assign a value to a variable. Some of these operators are simple and some are compound; that is, in addition to assignment, they also perform another operation on the operands. Table 17 shows this set of operators.

Table 17 Assignment operators in JavaScript

Operator

### Explanation

### Example

Equivalent expression

The value of the right-hand operand (`y`) is placed in the left-hand

`x` = `y`

`x` = `y`

=

operand (`x`).

The sum of the operands `x` and `y` is placed in the left-hand

`x` += `y`

`x` = `x` + `y`

+=

operand (`x`).

The difference of the operands `x` and `y` is placed in the left-hand

`x` -= `y`

`x` = `x` – `y`

-=

operand (`x`).

The product of the operands `x` and `y` is placed in the left-hand

`x` *= `y`

`x` = `x` * `y`

*=

operand (`x`).

The quotient of dividing operand `x` by operand `y` is placed in the

`x` /= `y`

`x` = `x` / `y`

/=

left-hand variable (`x`).

The remainder of dividing operand `x` by operand `y` is placed in

`x` %= `y`

`x` = `x` % `y`

%=

the left-hand variable (`x`).

Raises operand `x` to the power of operand `y` and places the result

`x` **= `y`

`x` = `x` ** `y`

**=

in the variable `x`.


---

**Page 204**

Comparison operators (`Comparison`): These operators are used to compare two operands.

This set of operators is shown in Table 18:

Table 18 Comparison operators

Operator

### Explanation

== to check equality of two operands by value, and === for equality of two operands by

== and ===

value and type != to check inequality of the values of two operands, and !== to check inequality of value and type

!= and !==

of the two operands

> , <

Whether the first operand is less than or greater than the second operand

<= , >=Less than or equal to, greater than or equal to

?

The ternary conditional operator, used to choose between two values based on a condition.

Boolean operators (`Boolean`): Logical operators are used to combine or reverse conditions. These operators make it possible to combine logical expressions in different situations. Table 19 introduces JavaScript’s logical operators:

Table 19 Logical operators

Operator

### Explanation

&&

The `AND` operator checks whether both operands are true.

||

The `OR` operator checks whether at least one of the conditions is true.

!

The `NOT` operator reverses whether a condition is true or false.


---

**Page 205**

Working with JavaScript’s different kinds of operators

### Workshop

Create a new file named `workshop3.html` and write the `<script>` tag in the `body` section. Then enter the following script in it and write the results you get in the blanks.

```
;"1 let x = 10, y = 2, z= 3, w=20, s="10", n = "sara", m="sina
```

;++2 `x`

.………………

;3 `y` += `x`

.………………

;4 `--z`

.………………

;5 `z` *= `y`

.………………

;6 `x` /= 2

.………………

;7 `w` %= `z`

.………………

```
……………………………… ;)x: "+x + " , y:" + y + " , z:" + z , " , w:" + w"(8 console.log
```

.……………… ;)`x` < `y`( = 9 `let` `a`

```
.……………… ;)y == z( && )x > y( = 10 Let b
.……………… ;)x === s( = 11 Let c
```

.……………… ;)`y` != `z`( || 12 `Let` `d` = `c` .……………… ;)`n` < `m`( = 13 `Let` `e`

```
;)a: "+a + " , b:" + b + " , c:" + c , " , d:" + d + " , e: "+e"(14 console.log
.……………… ;"x is equal to s": "x is not equal to s" ?)x === s( = 15 result
;(result)16 console.log
```

.………………

### Note

When comparing two operands with the == and != operators, the data type of the operands does not matter and only their values are checked; whereas the === and !== operators also take the data type of the operands into account.

### Note

The expression ?(`x===s`) checks whether the two variables `x` and `s` are equal. If the result of the comparison is `true`, the phrase before the ? mark is stored in the variable `result`, and if the result is `false`, the phrase after the : mark is stored.


---
