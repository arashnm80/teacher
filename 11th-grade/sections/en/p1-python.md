# Data modeling


---

**Page 2**

## Learning unit 1

## Data modeling

### Have you ever thought about this

If you want to store your information—such as your name, age, and favorite color—in a program, how would you organize that information?

How can you display a welcome message to the user and get their name from them?

If you want to build a program that only people who meet a certain age condition are allowed to use, what condition should you write?

Suppose you have a shopping cart that contains several products. How can you display all the products one by one?

How can you prepare a number that the user entered as a string so it is ready for mathematical calculations?

### By the end, the student is expected to

1 Explain what Python is and what it is used for, and be able to run simple programs in the `IDLE` environment.

2 Follow the rules for writing code in Python (`syntax`), apply indentation correctly, and be able to place several statements in one program.

3 Print strings and numbers in Python, receive data from the user, and convert data types when needed.

4 Define variables, recognize common data types, and choose suitable names for variables according to `PEP` rules and standard naming conventions.

5 Use different kinds of operators (arithmetic, logical, comparison) and create simple conditions with `if` so the program can make decisions.

6 Define and traverse lists, use `for` and `while` loops to repeat operations, traverse data in lists and strings, and use `break` and `continue` to control loops.

### Performance standard

The student should be able to define and manage data in Python, perform basic operations on data, use conditional structures and loops, and process data in an organized way.


---

**Page 3**

### Getting to know Python and the programming environment

Python works on different platforms (Windows, Mac, Linux, and so on). This programming language has a simple command structure (`syntax`) similar to English and lets developers write programs with fewer lines of code than some other programming languages.

![Book image](../images/p009-01.png)

Python is an interpreted programming language; that means the codes are translated and run line by line by the interpreter. This language supports procedural, object-oriented, and functional programming styles;

You can create Python programs as files with the `.py` extension in any text editor and then send them to the Python interpreter to run.

**Figure 1**

To start coding with Python (after installing the latest version of Python) using the `IDLE` environment, first open the `Start` menu, then type `IDLE` or `Python` `IDLE`, and click `IDLE` (`Python` `3.x`).

The interactive environment window (the `IDLE` `Shell` window) opens. In this window, from the `file` menu, create a new file. The Python text editor environment opens and you can enter your statements in it (Figure 2).

![Book image](../images/p009-02.png)

1

![Book image](../images/p009-03.png)

2

![Book image](../images/p009-04.png)

3

**Figure 2**


---

**Page 4**

To get started, enter the code shown in Figure 3 into the Python text editor and save the file with the key combination `ctrl` + `s` under the name `prog01`_`hello.py` in a folder. When saving, be careful that in addition to the file name, the save path must also be chosen carefully. It is recommended that you create a folder named `PyProg` in advance on one of the drives `D:` or `E:` and save your files in this folder.

It is better to save file names with a pattern of your choice. For example, the name of the first file that prints the word `hello` can be as follows:

```
prog01_hello.py
```

and the second file, which is for working with variables, can be as follows.

```
prog02_variable
```

### Note

Never use Persian letters in file and folder names, because you will face many problems later.

For example, this name is completely wrong: salam `.py`

![Figure 3](../images/p010-01.png)

**Figure 3**

### Note

Python supports the Persian language; but the letters are shown jumbled. It is better to use English characters in all cases.

Using the `Run` menu, choose the `Run` `Module` command, or press the `F5` key, to run the first program you created.

On some laptops, to run the program you need to press the key combination `Fn+F5`. (Figure 4)

![Figure 4](../images/p010-02.png)

**Figure 4**


---

**Page 5**

As you can see in Figure 4, the result of running this code is displayed in the `IDLE` `Shell` window. You can type simple codes in the `IDLE` `Shell` environment and run them by pressing the `Enter` key (Figure 5). To leave this environment, type `exit`() or `Ctrl+d`, or simply close the window by clicking the `Close` button at the top.

The command structure for writing code (`syntax`) in Python:

![Figure 5](../images/p011-01.png)

**Figure 5**

Python was designed for greater readability and has similarities to English. It has also been influenced by mathematical ideas. Unlike many programming languages that use a semicolon (;) and parentheses to end each statement, Python uses new lines to complete and separate statements.

Indentation (`indent`) in Python: Indentation refers to the spaces placed at the beginning of a line of code. While in other programming languages indentation in code is only for readability, in Python indentation is very important. Python uses indentation to show a block of code.

If you skip indentation, Python gives you an error. The number of spaces is up to you as a programmer; the most common use is four spaces, but there must be at least one. You must use an equal number of spaces in a block of code; otherwise Python gives you an error (Figure 6). On line 5 of the code, the block of the `if` statement, which you will read about later, must move forward by one `Tab`, or the same 4 spaces. As you can see, Python has stopped running the program with an error.

![Figure 6](../images/p011-02.png)

**Figure 6**


---

**Page 6**

In the code below you can see the correct way to space (Figure 7).

![Book image](../images/p012-01.png)

![Figure 7](../images/p012-02.png)

**Figure 7**

Statements in Python:

Every computer program is made up of a set of instructions that must be executed by the computer. In programming languages, these instructions are called a statement or `Statement`. For example, the following statement prints the text “`learning` `python` `is` `fun` ” on the screen:

```
print(“learning python is fun! “)
```

Having several statements in a program: Most Python programs are made up of several statements one after another.

The computer runs these statements one after another in the same order you wrote them. As a result, the order of writing statements in the program matters (Figure 8).

![Figure 8](../images/p012-05.png)

**Figure 8**

Printing text strings in Python: Earlier you saw that to display text in the program output, the ()`print` function is used. In the Python language, text must be placed inside quotation marks. For this purpose you can use single quotes (' ') or double quotes (" ") (Figure 9).

![Book image](../images/p012-03.png)

![Figure 9](../images/p012-04.png)

**Figure 9**


---

**Page 7**

In Python, triple quotes `Triple` `Quotes` (' ' ') or (" " ") are used to print multi-line text or text that includes quotation marks.

![Book image](../images/p013-01.png)

If you forget to place the text inside quotation marks, Python raises an error (Figure 10).

**Figure 10**

If you want to print several words on one line, you can use the `end` parameter (Figure 11).

![Figure 11](../images/p013-04.png)

**Figure 11**

Printing numbers in Python:

You can use the ()`print` function to display integers or floating-point numbers (Figure 12).

![Figure 12](../images/p013-02.png)

**Figure 12**

You can perform mathematical operations inside it.

Also, in the `print` statement you can combine numbers and text (Figure 13).

![Figure 13](../images/p013-03.png)

**Figure 13**


---
