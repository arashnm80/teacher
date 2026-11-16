<!-- page 8 -->

## Variables and data types

A variable is a place in RAM used to store data temporarily. In Python you do not need to declare a variable first and then initialize it; the data type is detected automatically (Figure 14). Just write the variable name on the left of the assignment operator " `=` " and its value on the right. `name="baran" , num = 55` Python supports several kinds of variables (Figure 15).

![Figure 15](../images/p014-03.png)
*Figure 15*

![Figure 14](../images/p014-04.png)
*Figure 14*

Python works out the type of a variable from the value assigned to it.

**Example**: `num1=15` in this example Python makes the variable an integer, and you do not have to state its type.

### Common data types in Python

![Figure 16](../images/p014-01.png)
*Figure 16*

**The string data type (str)**: anything that is **text**, such as a name, a message, an email, a password, a phone number or a description, is of the string data type (**str**).

The **str** type, short for **string**, can be defined with single, double, or triple quotation marks (Figure 16).

- **The integer data type (int)**: numbers that you calculate with and that have no decimal part are integers (**int**), or **integer** (Figure 17).

![Figure 17](../images/p014-02.png)
*Figure 17*

<!-- page 9 -->

- **The decimal number data type (float)**: these data are numbers, are used in mathematical calculations and have a decimal part. For example:

```
  height = 1.75
```

- **The `type()` function**: the output of the **`type()`** function is the **data type** of a variable (Figure 18).

![Figure 18](../images/p015-01.png)
*Figure 18*

From this step on, write the code in the VS Code environment. To do this, run the VS Code program, then from the File menu use the new folder command to create a new folder named PyProg, and then in that folder, from the File menu choose New File, or in the EXPLORER box press the New File button, or use the key combination Ctrl+N to create a new file named `prog01.py` in this folder (Figure 19). Now the code editor page opens and you can write your statements in it.

![Figure 19](../images/p015-02.png)
*Figure 19*

To run the statements, use the button at the top right of the program window or the Run menu. The result is shown at the bottom of the window (Figure 20).

![Figure 20](../images/p015-03.png)
*Figure 20*

**Python style guide** (PEP)

It gives the way of writing Python code and the coding conventions, and makes the code more readable and clean. To see it, you can visit `pep8.ir`.

<!-- page 10 -->

> **Curiosity**
>
> After reading the pep8 principles, answer these questions:
>
> 1. At most, how many characters can you write on one line?
>
> 2. How many characters should an indent be?
>
> 3. Can a line start with a space character?

In VSCode, after coding, pressing the keys Alt+Shift+F automatically fixes most of the code formatting problems according to pep8, provided that one of the extensions autopep8, Black formatter, Ruff or yapf is installed.

### Rules for naming variables in Python

- A variable name cannot contain a space. For example, you cannot define a variable named is valid.

- The name of a variable in Python must begin with a letter or an underscore. For example (`num`, `_personal`)

- A variable name can contain letters, digits, and underscores.

- Variable names are case-sensitive: Age, age and AGE are three different variables.

- A variable name must not be one of Python's keywords. The names var, import, const, if, and for are wrong as variable names, because these words are Python keywords.

> **Note**
>
> In Python, a keyword is a word that the language itself reserves for its statements and structures. These words have a predefined meaning, so they cannot be used as names of variables, functions, or classes.

> **Curiosity**
>
> Python has several ways to name variables made of more than one word. Research them and present them in class.

**Operator**: special symbols that do a certain operation on values or variables. In the expressions a + b or c \* d or 4/2, the symbols +, \* and / are called operators.

**Operand**: the value or values the operators work on. For example, in the expression a + b the sign "+" is the operator and a, b are the operands.

<!-- page 11 -->

The operands of the " +" operator in Python can both be numbers or both be strings. In the first case you get mathematical addition, and in the second case concatenation (**concatenation**) (Figure 21).

![Figure 21](../images/p017-03.png)
*Figure 21*

> **Curiosity**
>
> What happens if, with the + operator, one operand is a number and the other is a string?

> **Project**
>
> ### The cook project
>
> Write a program that picks one food at random from a list of foods.
>
> ![Book image](../images/p017-01.png)
>
> On the first line, bring (**import**) the **random** library into the program so that on line 3 it can use the **choice** method to pick at random.
>
> On the second line you can add your favorite foods to the list, and help your mother choose a meal at home.
>
> On the third line, one food is picked at random from the **foods** list and stored in the **item** variable. On the fourth line, the **item** variable, which now holds the name of a random food, is printed.
>
> - What change could you make to the code so that one food has a better chance of being picked?
>
> Answer: in the code below, repeating the name «ash» gives ash a better chance of being picked.
>
> ![Book image](../images/p017-02.png)

<!-- page 12 -->

### Some kinds of operators in Python

Table 1 shows some arithmetic operators you can use for math calculations.

*Table 1*

**Arithmetic operators**

| Operator | Use |
| --- | --- |
| + | Addition |
| - | Subtraction |
| \* | Multiplication |
| / | Division |
| % | Remainder of division |

![Figure 22](../images/p018-01.png)
*Figure 22*

> **Curiosity**
>
> Research other kinds of operators and present them in class.

### Input and output statements

- **The `print()` statement**: you learned earlier that **print** is used to show output, and you have seen some of its uses.

The **`len()`** function: sometimes you need to know how many characters a text has. This function counts the characters of a text (Figure 23).

![Figure 23](../images/p018-02.png)
*Figure 23*

- **The `input()` statement**: to receive data from the user and store it in a variable, the input statement is used (Figure 24).

![Figure 24](../images/p018-03.png)
*Figure 24*
