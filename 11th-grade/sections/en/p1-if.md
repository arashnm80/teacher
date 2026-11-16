<!-- page 22 -->

### The if statement

In Python, the if statement is the simplest and most widely used tool for building a conditional structure. It evaluates a logical expression whose result can be True or False. If the result of the condition is True, its block of code runs; otherwise that block does not run.

> **Note**
>
> The statements that belong to a conditional structure must be written one tab (a few equivalent spaces) further in than the if line. This indentation shows which statements belong to the condition.

### The first type of the if conditional structure

```
if condition:
      statement
```

*Table 2*

**Comparison operators**

| Operator | Use |
| --- | --- |
| `==` | Is equal to |
| `!=` | Is not equal to |
| `<` | Less than |
| `>` | Greater than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

**Condition**: a logical expression whose result is True or False.

**Statements**: statements that run only if the condition is true.

**Indentation**: these statements must be written one tab further in than the if statement.

Comparison operators (Comparison Operators): these operators are used to **compare two values or two variables**, and their result is **always either True or False** (Table 2).

**The equality operator** (`==`): used to compare two values or two variables to find out whether they are equal.

**Example**: write a program that receives the **user's name**. If the entered name equals the value admin, it displays the message "welcome admin!" (Figure 51).

![Figure 51](../images/p028-01.png)
*Figure 51*

<!-- page 23 -->

The (`!=`) operator: checks whether two values are not equal.

In the program below, `price = 120` at first, and the condition «its value is **not equal** to 100» holds, so it prints the message "price is not true" (Figure 52).

![Figure 52](../images/p029-01.png)
*Figure 52*

### Logical operators

*Table 2*

**Logical operators**

| Operator | Use |
| --- | --- |
| **and** | and |
| **or** | or |
| **not** | not |

In programming, **logical operators** are used to check several conditions at the same time and to make more exact decisions. These operators make it possible to combine several conditional expressions, and their result is usually one of two values: **true (True)** or **false (False)** (Table 3).

Logical operators are usually used together with **conditional statements** such as if, and help the programmer check more complex conditions.

1. **The and operator**: gives a true (**True**) result when **all the conditions are true**.

**Example**: in this example the logical and operator checks two conditions at once, **`username == "admin"`** and **`password == "1234"`**, and if the user enters both correctly the message **login successful** is shown. Write and run the program (Figure 53).

![Figure 53](../images/p029-02.png)
*Figure 53*

<!-- page 24 -->

2. **The or operator**: gives a true (**True**) result when **at least one of the conditions is true**. If both conditions are false, the result is false.

**Example**: in this program the condition is checked with the **or** operator; that is, if the user enters the day **Friday** or **Thursday**, the message **Holiday** is shown (Figure 54).

![Figure 54](../images/p030-01.png)
*Figure 54*

![Book image](../images/p030-02.png)

> **Activity**
>
> With your teacher's guidance, explain the code below.
>
> ![Book image](../images/p030-03.png)

**The second form of the conditional structure: if – else**:

```
if condition :
       statements_if
else:
      statements_else
```

The if-else structure is used when you want to do one thing if the condition is true and something else otherwise.

**condition**: a logical expression whose result is True or False.

**`statements_if`**: the statements that run when the condition is true.

**else**: means «otherwise». When the condition is not true, the program goes to the **else** part and runs its code.

**`statements_else`**: the statements that run when the condition is false.

<!-- page 25 -->

**Example**: write a program that gets a day of the week and shows " you are off" if it is Friday, and "you have to go to school" otherwise.

What do you think is wrong with the code in Figure 55? What message is printed if the user types something that is not a day of the week?

![Figure 55](../images/p031-01.png)
*Figure 55*

![Book image](../images/p031-02.png)

**Example**: write a program that gets a number between 0 and 10. If the number is in this range, show the message "**The number is valid**"; otherwise show "**The number is not valid**". In this example two conditions are checked at the same time (Figure 56).

![Figure 56](../images/p031-03.png)
*Figure 56*

> **Activity**
>
> Write a program that gets **the user's math and English grades** and, **if both are greater than or equal to 17**, shows the message " You can enroll in the network and software field "; otherwise it shows " You are not allowed to choose this field ".

> **Activity**
>
> Write a program that gets **the user's age** and **membership status**. If the user's age is **greater than or equal to 18 and they are a site member**, show the message " Access allowed"; otherwise show " Access denied".

<!-- page 26 -->

**Example**: write a program in which the user enters the internet connection status and the internet speed. If the status is "**yes**" and the speed is " greater than or equal to 3 ", print " Internet is connected "; otherwise print "Internet is disconnect" (Figure 57).

![Figure 57](../images/p032-01.png)
*Figure 57*

![Book image](../images/p032-02.png)

**Example**: write a program that, if the user is not the guest "guest", displays the message "Welcome!", and otherwise displays the message "Access denied".

**not** reverses the Boolean value of the condition (Figure 58).

![Figure 58](../images/p032-03.png)
*Figure 58*

**Combining the and and or operators**: in programming you sometimes need to check more than one condition together. For this you can **combine the logical operators and and or**.

**Example**: write a program that gets a username and a password and, if the user's role is "teacher" **or** "admin" **and** the password entered equals "1234", prints "Access allowed"; otherwise it prints "Access denied" (Figure 59).

![Figure 59](../images/p032-04.png)
*Figure 59*
