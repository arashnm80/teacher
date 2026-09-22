**Page 22**

The `if` statement:

In Python, the `if` statement is the simplest and most widely used tool for implementing a conditional structure. This statement evaluates a logical expression whose result can be `True` or `False`. If the result of the condition is `True`, the related block of code is executed; otherwise, that block of code is not executed.

### Note

The statements that belong to a conditional structure must be written one `tab` (or an equivalent number of spaces) farther in than the `if` line. This indentation shows which statements belong to the condition.

First type of the `if` conditional structure:

```
:if condition
statement
```

**Table 2**

Condition (`condition`): a logical expression whose result

```
True یا False است.
```

Comparison operator Operator

### Application

Statements (`statements`): statements that are executed only when

==

the condition is true.

is equal

!=

is not equal

Indentation (`Indentation`): these statements must be written one `tab` farther in than the `if` statement.

<

greater than

Comparison operators (`Comparison` `Operators`): these

less than

>

operators are used to compare two values or two variables

>= greater than or equal

and their result is always one of the two values `True` or

<= less than or equal

`False` (Table 2).

The equality operator (==): is used to compare two values or two variables to determine whether they are equal or not.

Example: Write a program that receives the user's name. If the entered name equals the value `admin`, display the message "!`welcome` `admin`" (Figure 51).

![Book image](../images/p028-01.png)

![Figure 51](../images/p028-02.png)

**Figure 51**


---

**Page 23**

The operator (`!=`): compares whether two values are unequal or not.

In the program below, at first `price` = 120, and the condition is satisfied when its value is not equal to 100, and the message `"price` `is` `not` `true"` is printed (Figure 52).

![Book image](../images/p029-01.png)

![Figure 52](../images/p029-02.png)

**Figure 52**

Logical operators (`Logical` `Operators`)

**Table 2**

In programming, to check several conditions at the same time and make more precise decisions,

Logical operators

logical operators are used. These operators

Operator

### Application

let you combine several conditional expressions, and their result is usually one of the two values true (`True`) or false (`False`)

`and` and

(Table 3).

`or` or

Logical operators are usually used together with conditional statements such as `if` and

`not` negation

help the programmer check more complex conditions.

1 The `and` operator: this operator returns true (`True`) only when all conditions are true.

Example: In this example, using the logical operator `and`, the two conditions `"username` == `"admin` and `"password` == "1234 are checked at the same time, and if the user enters both correctly, the message `login` `successful` is displayed. Write and run the program (Figure 53).

![Book image](../images/p029-03.png)

![Figure 53](../images/p029-04.png)

**Figure 53**


---

**Page 24**

2 The `or` operator: this operator returns true (`True`) when at least one of the conditions is true.

If both conditions are false, the result will be false.

Example: In this program the condition is checked with the `or` operator; that is, if the user enters the day name `Friday` or `Thursday`, the message `Holiday` is displayed (Figure 54).

![Book image](../images/p030-02.png)

![Book image](../images/p030-01.png)

![Figure 54](../images/p030-03.png)

**Figure 54**

### Activity

With guidance from your instructor, explain the code below.

![Book image](../images/p030-04.png)

Second type of the conditional structure `if` – `else`:

```
: if condition
statements_if
```

`:else`

```
statements_else
```

The `if-else` structure is used when you want to do one thing if the condition is true and something else otherwise.

`condition:` a logical expression whose result is `True` or `False`.

`statements_if:` statements that are executed when the condition is true.

`else:` means otherwise. When the condition is not true, the program enters the `else` section and its code is executed.

`statements_else:` statements that are executed when the condition is false.


---

**Page 25**

Example: Write a program that receives the days of the week and, if it is Friday, displays the message " `you` `are` `off"` and otherwise displays `"you` `have` `to` `go` `to` `school"`.

What do you think is wrong with the code in Figure 55? If the user enters something other than the days of the week, what message is printed?

![Book image](../images/p031-01.png)

![Book image](../images/p031-02.png)

![Figure 55](../images/p031-03.png)

**Figure 55**

Example: Write a program that receives numbers between 0 and 10; if the received number is in this range, display the message `"The` `number` `is` `valid"` and otherwise display the message `"The` `number` `is` `not` `valid"`.

In this example two conditions are checked at the same time (Figure 56).

![Figure 56](../images/p031-04.png)

**Figure 56**

### Activity

Write a program that receives the user's math and language grades and, if both are greater than or equal to 17, displays the message "You can register in the Network and Software major" and otherwise displays the message "You are not allowed to choose this major".

### Activity

Write a program that receives the user's age and membership status. If the user's age is greater than or equal to 18 and the user is a member of the site, display the message " `Access` `allowed"`; otherwise display the message " `Access` `denied"`.


---

**Page 26**

Example: Write a program in which the user enters the internet connection status and internet speed; if the connection status is `"yes"` and the speed entered is "greater than or equal to 3", print the message " `Internet` `is` `connected` " and otherwise print the message `"Internet` `is` `disconnect"` (Figure 57).

![Book image](../images/p032-01.png)

![Book image](../images/p032-02.png)

![Figure 57](../images/p032-03.png)

**Figure 57**

Example: Write a program that if the user is not a guest `"guest"`, displays the message "!`Welcome"` and in that case displays the message `"Access` `denied"`.

`not` negates the `Boolean` value of the condition (Figure 58).

![Figure 58](../images/p032-04.png)

**Figure 58**

Combining the two operators `and` and `or:` In programming you sometimes need to check more than one condition together.

To do this, you can combine the logical operators `and` and `or`.

Example: Write a program that receives a username and password and, if the user's role is `"teacher"` or `"admin"` and the entered password equals "1234", prints the message `"Access` `allowed"` and otherwise prints the message `"Access` `denied"` (Figure 59).

![Figure 59](../images/p032-05.png)

**Figure 59**


---
