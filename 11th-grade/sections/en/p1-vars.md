**Page 8**

### Variable and data types

A variable is a location in `RAM` memory that is used for temporary storage of data. In Python, to create a variable you do not need to first declare it and then initialize it; the data type is recognized automatically (Figure 14).

![Book image](../images/p014-04.png)

`num` = 55

It is enough that on the left side of the assignment operator, that is "=", you write the variable name and on the right side its value

```
بنویسید. name="baran" , num = 55
```

**Figure 14**

![Book image](../images/p014-03.png)

Python supports different kinds of variables (Figure 15).

`list`

`str`

Python recognizes the type of a variable from the value assigned

`int`

`set`

to it.

```
f loat
```

`tuple`

Example: `num1=15` In this example Python sets the variable type to integer, and there is no need to state the type

`dict`

`bool`

of the variable either.

**Figure 15**

Common data types in Python String data type (`str`): Anything that is text—such as a name, a message, an email, a password, a phone number, or a description—is the string data type (`str`).

![Book image](../images/p014-01.png)

The `str` data type, which is short for the word `string`, can be defined using single, double,

**Figure 16**

or triple quotation marks (Figure 16).

Integer data type (`int`): Numbers that you calculate with and that have no decimal part are integers (`int`), or `integer` (Figure 17).

![Figure 17](../images/p014-02.png)

**Figure 17**


---

**Page 9**

Floating-point data type (`folat`): These data are numeric and are used in mathematical calculations and have a decimal value. For example:

```
height = 1.75
```

The ()`type` function: The output of the `type`() function is the data type of each variable (Figure 18).

![Figure 18](../images/p015-01.png)

**Figure 18**

From this stage on, write the codes in the `VS` `Code` environment. To do this, run the `VS` `Code` program and then, from the File menu, use the `new` `folder` command to create a new folder named `PyProg`, and then in that folder, from the File menu by choosing the `New` `File` option,

![Figure 19](../images/p015-02.png)

**Figure 19**

in the `EXPLORER` pane choose the `New` `File` button or the key combination `Ctrl+` `N` to create a new file named `prog01.py` in this folder (Figure 19). Now the code editor page opens and you can write your statements in it.

To run the statements, use the button

at the top right of the program window or the `Run` menu. The result

of running the program will be displayed at the bottom of the page (Figure 20).

![Figure 20](../images/p015-03.png)

**Figure 20**

The Python style guide (`PEP`) presents how to write Python code and coding conventions, and makes the codes more readable and cleaner (`clean`). To view it you can go to `pep8.ir`.


---

**Page 10**

### Try this

After viewing the principles of `pep8`, answer the following questions:

1 What is the maximum number of characters you can write on one line?

2 How many characters should indentations be?

3 Can you use a space character at the beginning of a line?

In `VSCode`, after coding, pressing the keys `Alt+Shift+F` automatically fixes most code formatting problems based on `pep8`, provided that one of the extensions `autopep8`, `Black` `formatter`, `Ruff`, or `yapf` is installed.

Rules for naming variables in Python A variable name cannot include a space character. For example, you cannot define a variable named `is` `valid`.

Naming variables in Python must begin with a letter or an underscore. For example (`_num` , `personl` ) A variable name can include letters, numbers, and underscores.

Variable names are case-sensitive. `Age`, `age`, and `AGE` are three different variables.

A variable name must not be any of the Python keywords. The names `import`, `var`, `const`, `if`, `for` are wrong as variable names, because these words are Python keywords.

### Note

A keyword (`Keyword`) in Python refers to words that the Python language itself has reserved for its statements and structures. These words have a predefined meaning, and for that reason you cannot use them as the name of a variable, function, or class.

### Try this

In Python there are different methods for naming multi-word variables. Research them and present them in class.

Operator (`operator`): Special symbols that perform a particular operation on values or variables.

In the expressions `a` + `b` or `c` * `d` or 4/2, +, *, and / are called operators (`operator`).

Operand (`operand`): The value or values that operators work on. For example, in the expression `b+` `a`, the "+" sign is the operator and `a` and `b` are the operands.


---

**Page 11**

The operands of the "+" operator in Python can both be numeric or both be strings; in the first case mathematical addition happens, and in the second case concatenation happens (Figure 21).

![Book image](../images/p017-04.png)

![Figure 21](../images/p017-03.png)

**Figure 21**

### Try this

If in the + operator one of the operands is numeric and the other is a string, what happens?

Project

Ashpazbashi project:

Write a program that randomly chooses one item from a list of foods.

![Book image](../images/p017-01.png)

On the first line, import the `random` library into the program so that on line 3 it can use the `choice` method for a random selection.

On the second line you can add your favorite foods to the list and at home help your mother choose a meal.

On the third line, one food is chosen at random from the `foods` list and stored in the `item` variable.

On the fourth line, the `item` variable, which now holds the name of a random food, is printed.

In your opinion, what change can you make to the code so that one food has a greater chance in the random selection?

Answer: In the code below, by repeating the name ash, the chance of choosing ash has increased.

![Book image](../images/p017-02.png)


---

**Page 12**

Some kinds of operators in Python:

Table 1 shows some of the arithmetic operators that you can use to perform mathematical calculations.

**Table 1**

![Book image](../images/p018-01.png)

Arithmetic operator Operator

### In practice

+ addition - subtraction

*

multiplication

/

division % remainder of division

**Figure 22**

### Try this

Research other kinds of operators and present them in class.

Input and output statements:

The ()`print` statement: Earlier it was said that the `print` statement is used to display output, and you also became familiar with some uses of this statement.

The ()`len` function: Sometimes you need to know how many characters a text has. This function calculates the number of characters in a text (Figure 23).

![Figure 23](../images/p018-02.png)

**Figure 23**

The ()`input` statement: To receive data from the user and store it in a variable, the `input` statement is used (Figure 24).

![Book image](../images/p018-03.png)

![Figure 24](../images/p018-04.png)

**Figure 24**


---
