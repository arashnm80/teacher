<!-- page 2 -->

## Learning unit 1

## Have you ever thought about this

- If you wanted to store information about yourself, such as your name, age, and favorite color, in a program, how would you organize that information?

- How can you show a welcome message to the user and get their name from them?

- If you want to build a program that only people of a certain age may use, what condition should you write?

- Suppose you have a shopping cart with several products in it. How can you show all the products one by one?

- How can you prepare a number that the user typed in as a string for mathematical calculations?

## By the end, the student is expected to

1. Explain what Python is and what it is used for, and be able to run simple programs in the IDLE environment.

2. Follow the rules for writing code in Python (syntax), apply indentation correctly, and be able to put several statements in one program.

3. Print strings and numbers in Python, get data from the user, and convert data types when needed.

4. Define variables, know the common data types, and choose suitable variable names according to the PEP rules and standard naming.

5. Use the different kinds of operators (arithmetic, logical, comparison) and write simple conditions with if so that the program can make decisions.

6. Define lists and go through them, use for and while loops to repeat operations, go through the data in lists and strings, and use the break and continue statements to control loops.

## Performance standard

The student can define and manage data in Python, perform basic operations on data, use conditional structures and loops, and process data in an organized way.

<!-- page 3 -->

## Getting to know Python and the programming environment

Python runs on different platforms (Windows, Mac, Linux, and so on). Its syntax is simple and similar to English, and it lets developers write programs with fewer lines than some other programming languages. Python is an interpreted language: the code is translated and run line by line by the interpreter. It supports procedural, object-oriented, and functional programming. You can create Python programs as files with the `.py` extension in any text editor and then send them to the Python interpreter to run.

![Figure 1](../images/p009-01.png)
*Figure 1*

To start coding with Python (after installing the latest version of Python) using the IDLE environment, first open the Start menu, then type IDLE or Python IDLE and click `IDLE (Python 3.x)`. The interactive window (the IDLE Shell window) opens. In this window, create a new file from the File menu. The Python text editor opens and you can enter your statements in it (Figure 2).

![Figure 2](../images/p009-02.png)
*Figure 2*

<!-- page 4 -->

To begin, type the code shown in Figure 3 into the Python text editor and save the file with the key combination ctrl + s under the name `prog01_hello.py` in a folder. When saving, be careful to choose not only the file name but also the folder where the file is saved. It is a good idea to create a folder named PyProg in advance on one of the drives D: or E: and save your files in it.

It is better to name your files with a pattern of your choice. For example, the first file, which prints the word hello, can be named like this:

`prog01_hello.py` and the second file, which is about variables, like this:

`prog02_variable`

> **Note**
>
> Never use Persian letters in file and folder names, because you will run into many problems later.
>
> For example, this name is completely wrong: `سلام.py`

![Figure 3](../images/p010-01.png)
*Figure 3*

> **Note**
>
> Python supports Persian, but the letters may be shown jumbled. It is better to use English characters everywhere.

Run your first program with the Run Module command in the Run menu, or by pressing the F5 key. On some laptops you need to press the key combination Fn+F5 to run the program. (Figure 4)

![Figure 4](../images/p010-02.png)
*Figure 4*

<!-- page 5 -->

As you can see in Figure 4, the result of running this code is shown in the IDLE Shell window. You can type simple code in the IDLE Shell and run it by pressing Enter (Figure 5). To leave this environment, type `exit()` or Ctrl+d, or simply close the window with the Close button at the top.

### The syntax of Python code

![Figure 5](../images/p011-01.png)
*Figure 5*

Python was designed to be readable and has similarities with English. It is also influenced by mathematics. Unlike many programming languages that use a semicolon (;) and parentheses to end each statement, Python uses new lines to complete and separate statements.

**Indentation (indent) in Python**: indentation means the spaces at the beginning of a line of code. In other programming languages, indentation is only for readability, but in Python indentation is **very important**. Python uses indentation to mark a block of code.

If you skip the indentation, Python gives you an error. The number of spaces is up to you as the programmer; the most common choice is four spaces, but there must be at least one. You must use the same number of spaces within a block of code, otherwise Python gives you an error (Figure 6). On line 5 of the code, the block of the if statement, which you will learn about later, must move forward by one Tab, which is 4 spaces. As you can see, Python stopped the program with an error.

![Figure 6](../images/p011-02.png)
*Figure 6*

<!-- page 6 -->

The code below shows the correct way to indent (Figure 7).

![Figure 7](../images/p012-01.png)
*Figure 7*

### Statements in Python

Every computer program is made of a set of instructions that the computer must carry out. In programming languages these instructions are called statements. For example, the statement below prints the text «learning python is fun» on the screen:

```
 print(“learning python is fun! “)
```

**Several statements in a program**: most Python programs are made of several statements one after another. The computer runs these statements one by one, in the order you wrote them. So the order of the statements in a program matters (Figure 8).

![Figure 8](../images/p012-03.png)
*Figure 8*

**Printing text strings in Python**: you saw earlier that the `print()` function is used to show text in the program's output. In Python, text must be put inside quotation marks. You can use single quotes (' ') or double quotes (" ") for this (Figure 9).

![Figure 9](../images/p012-02.png)
*Figure 9*

<!-- page 7 -->

![Figure 10](../images/p013-01.png)
*Figure 10*

- In Python, triple quotes (' ' ') or (" " ") are used to print text that spans several lines or text that contains quotation marks.

- If you forget to put the text inside quotation marks, Python reports an error (Figure 10).

- If you want to print several words on one line, you can use the end parameter (Figure 11).

![Figure 11](../images/p013-04.png)
*Figure 11*

### Printing numbers in Python

- You can use the **`print()`** function to show integers or decimal numbers (Figure 12).

![Figure 12](../images/p013-02.png)
*Figure 12*

- You can do math operations inside it.

- In the **print** statement you can also combine numbers and text (Figure 13).

![Figure 13](../images/p013-03.png)
*Figure 13*
