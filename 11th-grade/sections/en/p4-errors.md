**Page 260**

Traversing the lines of a file with a `for` loop

![Book image](../images/p266-02.png)

![Figure 27](../images/p266-01.png)

**Figure 27**

### Activity

Change the program code so that a separator is placed after the name of each brand.

Writing to a file: Writing one line After you set the path, you can write to a text file using the `write_text`() method. To see how this function works, write a simple message and store it in a text file instead of printing it on the screen (Figure 72):

After writing the program and running it, you do not see output in the terminal. Now open the file `mobile_brands.txt`. You see that your text has been written in the file and its previous contents have been erased.

If the file already exists, `write_text`() clears the current contents of the file and writes the new content in the file.

The `write_text`() method does several things behind the scenes. If the file that the path points to does not exist, it creates that file.

Also, after writing the string to the file, it makes sure the file is closed correctly. Files that are not closed correctly can lead to data being lost or corrupted.

![Figure 28](../images/p266-03.png)

**Figure 28**

### Note

The two methods `read_text` and `write_text` handle closing the file internally. In these cases, `pathlib` itself guarantees that the file is opened and then closed safely.


---

**Page 261**

Adding a new brand To write more than one line to a file, you must build a string that includes the entire contents of the file and then call `write_text`() with that string.

![Book image](../images/p267-01.png)

![Figure 29](../images/p267-02.png)

**Figure 29**

### Activity

Add two more brands, `"LG"` and `"Motorola"`, to the file `"mobile_brands.txt"`.

### Activity

Write a program that, in a loop, asks the user for mobile phone models. When the user answers, write them to a file named `"mobile_model.txt"`. Each model should appear on one line of the file.

Managing exceptions (`Exceptions`) While a program is running, errors may occur that cause the program to stop. Python uses a mechanism called an exception (`Exception`) to deal with these errors.

![Book image](../images/p267-03.png)

Whenever Python faces a problem while running the program and does not know what to do, it creates an “exception object.”

If the programmer has written code to manage that exception, the program continues without stopping. But if the exception has not been managed, execution of the program stops and a message is displayed that includes the type of error and its location; this is called a traceback (`Traceback`).

**Figure 30**


---

**Page 262**

Managing a wrong data-type error: Sometimes the programmer mistakenly enters data of the wrong type. For example, when they want to convert a string (text) to a number but its value is only text, a `ValueError` occurs:

![Book image](../images/p268-01.png)

![Figure 31](../images/p268-02.png)

**Figure 31**

![Book image](../images/p268-03.png)

Managing a division-by-zero error: One of the common errors in programming is dividing a number by zero. This is not possible mathematically, and Python tries to continue the program but that is not possible, so the program stops and Python shows something called a traceback, or `Traceback`.

**Figure 32**

That is, when Python faces such a statement, it creates an exception named `ZeroDivisionError`.

That is: exactly which line the error occurred on. What type of error it was (for example, `ZeroDivisionError` or `ValueError`). And it shows the function or part of the code that caused the error.

![Figure 33](../images/p268-04.png)

**Figure 33**

You can use this information to fix the program. Tell Python what to do when this type of exception occurs. That way, if it happens again, you will be ready.

Managing errors with `try-except` blocks: To manage exceptions in Python, `try` and `except` blocks are used.

The `try` section contains the statement that may cause an error.

The `except` section specifies how the program should react if an error occurs.

Using this method, you can write programs that show understandable messages to the user instead of displaying complex and confusing messages.


---

**Page 263**

Managing a wrong data-type error: Here Python cannot convert the word `"Hello"` to a number, so an exception is produced, but the program takes control of the error using a `try-except` block.

![Figure 34](../images/p269-01.png)

**Figure 34**

Here Python cannot divide the number 5 by the number 0, so an exception is produced, but the program takes control of the error using a `try-except` block.

![Figure 35](../images/p269-02.png)

**Figure 35**

Using exceptions to prevent errors: Managing exceptions (errors) correctly becomes critically important when the program still has other work to do after an error occurs. This situation is especially common in programs that continually receive input from the user. If the program can respond to invalid input in an appropriate way, instead of stopping and breaking down, it can intelligently ask the user for more valid input and continue running.

To learn this topic, carefully read and carry out the explanations that follow.

This program asks the user to enter the first number and, if the user does not enter `q` to exit, enters the second number.

![Figure 36](../images/p269-03.png)

**Figure 36**


---

**Page 264**

Then it divides these two numbers by each other to reach the answer.

This program does nothing to manage errors; if the user enters zero as the second number, the request to divide by zero causes it to break down:

![Figure 37](../images/p270-01.png)

**Figure 37**

### Note

Although a sudden stop of the program (`crash`) is certainly bad, displaying the technical details of the error (`Traceback`) is also not a good idea. These details are confusing for ordinary users, and in hostile environments they give valuable information to attackers. By seeing a `Traceback`, an attacker not only learns the name of your program, but can also see part of the logic of the code that has a flaw. A professional attacker can use this information to understand exactly what kinds of attacks to use against your code.

Using The else Block: When you use `try` and `except` statements in Python, you are in fact telling the interpreter (the computer): “Try one action, and if it fails, do this alternative action.” Now, what exactly is the `else` block useful for?

![Book image](../images/p270-02.png)

`else` means: “Do this action if and only if the `try` block was completely successful, without any error.”

**Figure 38**


---

**Page 265**

If an error occurs in the `try` block (for example, dividing a number by zero), Python goes directly to the `except` block and the `else` block is completely ignored. This feature helps you separate code that should run only after complete success (for example, displaying the final result or saving to a file) from code written only to test for errors. This makes the program both cleaner and more logical.

![Book image](../images/p271-01.png)

![Figure 39](../images/p271-02.png)

**Figure 39**

![Book image](../images/p271-03.png)

Managing a File Not Found Error: This error is one of the most common exceptions programmers face when working with files. There are several reasons for this error: a wrong path, a wrong file name, or the file having been deleted.

A `try-except` block lets you run the code and, if this particular problem occurs, show an appropriate reaction instead of stopping the program.

**Figure 40**

![Book image](../images/p271-04.png)

In the example the program tries to read a file that does not exist at all.

**Figure 41**


---

**Page 266**

![Figure 42](../images/p272-01.png)

**Figure 42**

Note that the `read_text`() method is used a little differently from what you saw before. The `encoding` argument is necessary when your system’s default encoding does not match the encoding of the file you are reading. This situation is most likely to occur when reading a file that was not created on your system.

Python cannot read from a file that does not exist, so it creates an exception (`Exception`) (in other words, it raises an error).

So to manage the error that is created, the `try` block begins with the line that is identified in the `traceback` as the problematic one.

![Figure 43](../images/p272-02.png)

**Figure 43**

In the example code, line 4, which includes `read_text`(), causes the error.

In this example, the code in the `try` block produces a `FileNotFoundError`, so an `except` block that matches the error must be written. Then Python runs the code in that block when the file is not found, and the result, instead of a `traceback`, is a user-friendly error message:

![Figure 44](../images/p272-03.png)

**Figure 44**


---
