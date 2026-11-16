<!-- page 260 -->

**Going over the lines of the file with a for loop**

![Figure 27](../images/p266-01.png)
*Figure 27*

> **Activity**
>
> Change the code of the program so that a separator is put after the name of each brand.

### Writing to a file: writing one line

After specifying the path, you can write in a text file with the method `write_text()`. To see how this function works, write a simple message and, instead of printing it on the screen, save it in the text file (Figure 27):

- After writing the program and running it, you do not see the output in the terminal. Now open the file `mobile_brands.txt`. You see that your text has been written in the file and its earlier content has been erased.

- If the file already exists, `write_text()` erases the current content of the file and writes the new content in the file.

- The method `write_text()` does several jobs behind the scenes. If the file that the path points to does not exist, it creates that file.

- Also, after writing the string to the file, it makes sure the file is closed correctly. Files that are not closed correctly can lead to loss or damage of data.

![Figure 28](../images/p266-02.png)
*Figure 28*

> **Note**
>
> The two methods `read_text` and `write_text` handle closing the file internally. In these cases, pathlib itself guarantees that the file is opened and then closed safely.

<!-- page 261 -->

### Adding a new brand

To write more than one line in a file, you must build a string that includes the whole content of the file and then call `write_text()` with that string.

![Figure 29](../images/p267-01.png)
*Figure 29*

> **Activity**
>
> Add two more brands, "LG" and "Motorola", to the file "`mobile_brands.txt`".

> **Activity**
>
> Write a program that in a loop asks the user for mobile phone models. When they answer, it writes them in a file named "`mobile_model.txt`". Each model must appear on one line of the file.

### Managing exceptions

![Figure 30](../images/p267-02.png)
*Figure 30*

While a program runs, errors may happen that cause the program to stop. To deal with these errors, Python uses a mechanism called an exception.

Whenever Python meets a problem while running the program and does not know what to do, it creates an "exception object". If the programmer has written code to manage that exception, the program goes on without stopping. But if the exception is not managed, the running of the program stops and a message including the type of the error and its place is shown, which is called a Traceback.

<!-- page 262 -->

**Handling the error of a wrong data type**: sometimes a programmer mistakenly enters data of the wrong type. For example when they want to convert a string (text) to a number but its value

![Figure 31](../images/p268-01.png)
*Figure 31*

is only text, a ValueError happens:

![Figure 32](../images/p268-02.png)
*Figure 32*

**Handling the divide-by-zero error**: one of the common errors in programming is dividing a number by zero. This is not possible mathematically and Python tries to continue the program but this is not possible, so the program stops and Python shows something called a traceback.

That is, when Python meets such a statement, it creates an exception called ZeroDivisionError. That is: it shows exactly in which line the error happened, what kind of error it was (for example ZeroDivisionError or ValueError), and the function or part of the code that caused the error.

![Figure 33](../images/p268-03.png)
*Figure 33*

You can use this information to fix the program. Tell Python what to do when this kind of exception happens. In this way, if it happens again, you will be ready.

**Handling errors with try-except blocks**: to manage exceptions in Python, try and except blocks are used.

- The try part contains the statement that may cause an error.

- The except part specifies how the program should react if an error happens.

Using this method, you can write programs that, instead of showing complex and confusing messages, show understandable messages to the user.

<!-- page 263 -->

**Handling the error of a wrong data type**: here Python cannot convert the word "Hello" to a number, so an exception is produced, but the program takes control of the error with a try-except block.

![Figure 34](../images/p269-01.png)
*Figure 34*

Here Python cannot divide the number 5 by the number 0, so an exception is produced, but the program takes control of the error with a try-except block.

![Figure 35](../images/p269-02.png)
*Figure 35*

**Using exceptions to prevent errors**: correct management of exceptions (errors) becomes vitally important when the program still has other things to do after an error happens. This situation is especially common in programs that continuously take input from the user. If the program can respond to invalid input in a suitable way, instead of stopping and crashing, it can intelligently ask the user for more valid inputs and carry on running.

To learn this topic, read and do the explanations that follow carefully.

- This program asks the user to enter the first number and, if the user does not enter q to quit, they enter the second number.

![Figure 36](../images/p269-03.png)
*Figure 36*

<!-- page 264 -->

- Then it divides these two numbers by each other to get the answer.

- This program does nothing to manage errors; if the user enters zero as the second number, the request to divide by zero makes it crash:

![Figure 37](../images/p270-01.png)
*Figure 37*

> **Note**
>
> Although a sudden stop of the program (crash) is certainly bad, showing the technical details of the error (Traceback) is not a good idea either. These details are confusing for ordinary users and, in malicious environments, give valuable information to attackers. By seeing a Traceback, an attacker not only learns the name of your program, but can see the part of the code's logic that has a flaw. A professional attacker can use this information to understand exactly what kind of attacks should be used against your code.

**The use of the else block**: when you use the try and except statements in Python, you are in fact telling the interpreter (the computer): "try one job, and if it breaks, do this alternative job." Now, what exactly is the else block good for? else means: "do this only and only if the try block was completely successful, without any error."

![Figure 38](../images/p270-02.png)
*Figure 38*

<!-- page 265 -->

If an error happens in the try block (for example dividing a number by zero), Python goes directly to the except block and the else block is completely ignored. This feature helps you separate the code that must run only after complete success (for example showing the final result or saving to a file) from the code written only to test for errors. This makes the program both cleaner and more logical.

![Figure 39](../images/p271-01.png)
*Figure 39*

![Figure 40](../images/p271-02.png)
*Figure 40*

**Handling the File Not Found Error**: this error is one of the most common exceptions that programmers meet when working with files. There are several reasons for this error: a wrong path, a wrong file name, or the file being deleted.

The try-except block lets you run the code and, if this specific problem happens, show a suitable reaction instead of the program stopping.

![Figure 41](../images/p271-03.png)
*Figure 41*

In the example, the program tries to read a file that does not exist at all.

<!-- page 266 -->

![Figure 42](../images/p272-01.png)
*Figure 42*

Note that the method `read_text()` is used a bit differently from what you saw before. The encoding argument is necessary when the default encoding of your system does not match the encoding of the file you are reading. This situation most probably happens when reading a file that was not created on your system.

Python cannot read from a file that does not exist, so it creates an exception (in other words, it raises an error).

So to manage the error that is created, the try block starts with the line that is identified in the traceback as the troublemaker.

![Figure 43](../images/p272-02.png)
*Figure 43*

In the code example, line 4, which contains `read_text()`, has caused the error.

In this example, the code in the try block produces the error FileNotFoundError, so an except block that matches the error must be written. Then Python runs the code in that block when the file is not found, and the result, instead of a traceback, is a user-friendly error message:

![Figure 44](../images/p272-03.png)
*Figure 44*
